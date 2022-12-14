#!/usr/bin/env python3
#
# Name:
#   calc_back_trajectory.py
#
# Purpose:  Calculate backwards for trajectories for CM1 model data.
#
# Syntax: python3 calc_back_trajectory.py version_number parcel_label
#
#   Input:
#
# Execution Example:
#   python3 calc_back_trajectory.py v3 downdraft
#
# Modification History:
#   2019/09/13 - Lance Wilson:  Modified from code written by Tom Gowan, using
#                               trajectories_CM1.ipynb from: https://github.com/tomgowan/trajectories/blob/master/trajectories_CM1.ipynb
#   2019/10/07 - Lance Wilson:  Splitting attempt at using the directly
#                               calculated wind values into separate file.
#   2021/08/25 - Lance Wilson:  Values to use for starting position and model
#                               file to start calculation from are now imported
#                               from a separate file containing dictionaries of
#                               values for each parcel label.
#   2021/10/14 - Lance Wilson:  Corrected error causing interpolated wind values
#                               to be one grid point off from the desired value.
#   2021/12/18 - Lance Wilson:  Renamed from calc_back_traj_meters_corrected.py
#                               to calc_back_trajectory.py.
#

from netCDF4 import Dataset
from netCDF4 import MFDataset

import back_trajectory_start_pos
import itertools
import numpy as np
import os
from scipy import interpolate
import sys
import time

if len(sys.argv) > 2:
    # Model run used to calculate trajectories.
    version_number = sys.argv[1]
    # Label for output file name.
    parcel_label = sys.argv[2]
else:
    print('Parcel label or version number was not specified.')
    print('Syntax: python3 calc_back_trajectory.py version_number parcel_label')
    print('Example: python3 calc_back_trajectory.py v3 downdraft')
    print('Currently supported version numbers: v3, 10s, v4, v5')
    sys.exit()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# User-defined values and constants.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Number of time steps to run trajectories back (set by user)
time_steps = 120

# Directory containing CM1 model netCDF files.
model_dir = '75m_100p_{:s}/'.format(version_number)

# Set as 'Y' or 'N' for 'yes' or 'no' if the u, v, and w model output is on the staggered grid 
# (unless you have interpolated u, v, and w to the scalar grid, they are most likely on the staggered grid (set by user)
staggered = 'Y'

# Directory to store the output file
output_dir = 'back_traj_npz_{:s}/'.format(version_number)
# Name of the output numpy archive.
output_file_name = output_dir + 'backtraj_{:s}'.format(parcel_label)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Get starting positions from dictionary in back_trajectory_start_pos.
start_pos = back_trajectory_start_pos.get_start_pos(parcel_label)
file_calc_start = start_pos['file_calc_start']

if version_number.startswith('v'):
    run_number = int(version_number[-1])
else:
    run_number = 3

# Number to subtract from start_time_step if not using entire dataset.
start_file_num = file_calc_start - time_steps

# List of CM1 files in the time span that is going to be used to calculate trajectories.
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(start_file_num,file_calc_start+1)]
ds = MFDataset(file_list)

# Unstaggered coordinates (converted to meters) in each dimension.
x = np.copy(ds.variables['xh'])*1000.
y = np.copy(ds.variables['yh'])*1000.
z = np.copy(ds.variables['z'])*1000.

# To use the staggered wind values, the main grid used for interpolation must
#   use the staggered coordinates.
if staggered == 'Y':
    x_stag = np.copy(ds.variables['xf'])*1000.
    y_stag = np.copy(ds.variables['yf'])*1000.
    z_stag = np.copy(ds.variables['zf'])*1000.
# If the wind data is not staggered, then the regular grid points can be used.
else:
    x_stag = x
    y_stag = y
    z_stag = z

# Number starting values in each dimension.
num_start_x = start_pos['num_start_x']
num_start_y = start_pos['num_start_y']
num_start_z = start_pos['num_start_z']

# Number of parcels (from user-specified dimensions)
num_parcels = num_start_x * num_start_y * num_start_z

# Time step to start backward trajectories at (set by user) 
# Start in downdraft at time 7200: file_calc_start = 221
# Start in SVC at time 7560: file_calc_start = 257
start_time_step = file_calc_start - start_file_num

# Model output time step length (seconds)
time_step_lengths = ds.variables['time'][1:] - ds.variables['time'][:-1]

# Trajectory locations (meters from center of model grid).
xpos = np.zeros((time_steps, num_parcels))
ypos = np.zeros((time_steps, num_parcels))
zpos = np.zeros((time_steps, num_parcels))

# Setup the starting trajectory positions (based on grid defined in
#   back_trajectory_start_pos).
for i,j,k in itertools.product(range(num_start_x), range(num_start_y), range(num_start_z)):
    cur_parcel_num = i*num_start_y*num_start_z + j*num_start_z + k
    xpos[0,cur_parcel_num] = start_pos['x_start'] + start_pos['x_increment'] * i
    ypos[0,cur_parcel_num] = start_pos['y_start'] + start_pos['y_increment'] * j
    zpos[0,cur_parcel_num] = start_pos['z_start'] + start_pos['z_increment'] * k

###################################################################
##################### Calculate Trajectories ######################
###################################################################

# Loop over all time steps and compute trajectory
for t in range(time_steps-1):

    start = time.time() #Timer
    
    # Get model data (set by user)
    u = ds.variables['u'][start_time_step-t,:,:,:]
    v = ds.variables['v'][start_time_step-t,:,:,:]
    w = ds.variables['w'][start_time_step-t,:,:,:]

    ############## Generate coordinates for interpolations ###############

    # x, y, and z locations on scalar grids
    xloc = np.copy(xpos[t,:])
    yloc = np.copy(ypos[t,:])
    zloc = np.copy(zpos[t,:])

    coord = np.column_stack((zloc, yloc, xloc))

    ############# Integrate to determine parcel's new location ############

    # Interpolate.interpn: take values in u, which are at locations (z,y,x),
    #   and get values for it via interpolation at locations coord.

    ########   Calc new xpos in meters from model center ###########
    xpos[t+1,:] = xpos[t,:] - interpolate.interpn((z,y,x_stag), u, coord, method='linear', bounds_error=False, fill_value=np.nan)*time_step_lengths[start_time_step-t-1]

    #########   Calc new ypos in meters from model center  ##########
    ypos[t+1,:] = ypos[t,:] - interpolate.interpn((z,y_stag,x), v, coord, method='linear', bounds_error=False, fill_value=np.nan)*time_step_lengths[start_time_step-t-1]

    ########   Calc new zpos in meters above ground level #########
    zpos[t+1,:] = zpos[t,:] - interpolate.interpn((z_stag,y,x), w, coord, method='linear', bounds_error=False, fill_value=np.nan)*time_step_lengths[start_time_step-t-1]
    
    # Prevent parcels from going into the ground
    zpos = zpos.clip(min=0)
    
    # Timer
    stop = time.time()
    print("Integration {:01d} took {:.2f} seconds".format(t, stop-start))

# Save to numpy uncompressed archive for the plotting script.
np.savez(output_file_name, xpos=xpos, ypos=ypos, zpos=zpos, offset=file_calc_start-time_steps, parcel_dimension=np.array((num_start_x, num_start_y, num_start_z)))

