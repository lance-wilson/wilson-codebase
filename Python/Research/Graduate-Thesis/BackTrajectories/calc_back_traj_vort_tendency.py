#!/usr/bin/env python3
#
# Name:
#   calc_back_traj_vort_tendency.py
#
# Purpose:  Interpolate values of terms of the 3D vorticity equation and values
#           of CM1-calculated vorticity budget variables to the positions of
#           backward trajectories. Separate files are created for trajectories
#           that have usable data for their entire integration and trajectories
#           that have usable data for a certain period of time (set by user).
#
# Syntax: python3 calc_back_traj_vort_tendency.py model_version parcel_label
#
#   Input: A back trajectory numpy archive, named "backtraj_(parcel_label).npz",
#           and netCDF files named "(model_version)_direct_vort_equation.nc"
#           and "(model_version)_direct_vort_equation.nc".
#
# Execution Example:
#   python3  calc_back_traj_vort_tendency.py v5 v5_meso_tornadogenesis
#
# Temporary Execution Example (Run local script on server):
#   ssh vortex python < calc_back_traj_vort_tendency.py - v5 v5_meso_tornadogenesis
#
# Modification History:
#   2021/09/15 - Lance Wilson:  Created, partially from unstaggered_trajectory_test.py,
#                               some pieces from code written by Tom Gowan, using
#                               trajectories_CM1.ipynb from: https://github.com/tomgowan/trajectories/blob/master/trajectories_CM1.ipynb
#

from netCDF4 import Dataset
import atexit
import numpy as np
from scipy import interpolate
import sys
import time

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def create_nc_out(version_number, parcel_label, subset, traj_num, xpos, ypos, zpos, file_num_offset, model_dir):
    # Set name for output netCDF file.
    if version_number in parcel_label:
        ds_out_name = 'back_traj_analysis/parcel_interpolation/{:s}_{:s}_valid_back_trajectory.nc'.format(parcel_label, subset)
    else:
        ds_out_name = 'back_traj_analysis/parcel_interpolation/{:s}_{:s}_{:s}_valid_back_trajectory.nc'.format(version_number, parcel_label, subset)

    # Open the output netCDF file.
    ds_out = Dataset(model_dir + ds_out_name, mode='w')

    # Create netCDF variable dimensions.
    parcel_dim = ds_out.createDimension('number_parcels', traj_num)
    time_dim = ds_out.createDimension('time', None)
    offset_dim = ds_out.createDimension('offset', 1)

    # Create variable containing the subset of x coordinate data used in the output.
    xpos_var = ds_out.createVariable('xpos', np.float32, ('time', 'number_parcels'))
    xpos_var.units = 'm'
    xpos_var.definition = 'X-Direction Parcel Positions'
    xpos_var[:,:] = xpos

    # Create variable containing the subset of y coordinate data used in the output.
    ypos_var = ds_out.createVariable('ypos', np.float32, ('time', 'number_parcels'))
    ypos_var.units = 'm'
    ypos_var.definition = 'Y-Direction Parcel Positions'
    ypos_var[:,:] = ypos

    # Create variable containing the subset of z coordinate data used in the output.
    zpos_var = ds_out.createVariable('zpos', np.float32, ('time', 'number_parcels'))
    zpos_var.units = 'm'
    zpos_var.definition = 'Z-Direction Parcel Positions'
    zpos_var[:,:] = zpos

    # Create variable to store file_num_offset.
    offset_var = ds_out.createVariable('file_num_offset', np.int, ('offset'))
    offset_var.definition = 'Number of model files earlier than the earliest back trajectory time'
    offset_var[:] = file_num_offset

    return ds_out

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def create_time_var(ds_in, ds_out, file_num_offset, parcel_time_steps):
    # Create variable to store time.
    time_var = ds_out.createVariable('time', np.float32, ('time'))
    time_var.units = 'seconds'
    time_var.definition = ds_in.variables['time'].definition
    time_var[:] = ds_in.variables['time'][file_num_offset:file_num_offset+parcel_time_steps][::-1]

    return

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def interpolate_budget(ds_in, ds_out, xpos, ypos, zpos, file_num_offset, parcel_time_steps):
    # Coordinates (in meters) in each dimension (already converted to meters
    #   in ds_in netCDF file).
    x_coord = np.copy(ds_in.variables['xh'])
    y_coord = np.copy(ds_in.variables['yh'])
    z_coord = np.copy(ds_in.variables['z'])

    # Create a tuple of the coordinates that is passed to the interpn function
    #   to be used as the regular grid.
    grid_coord = (z_coord,y_coord,x_coord)

    #for var_name in variables:
    for var_name in ds_in.variables.keys():
        if len(ds_in.variables[var_name].dimensions) == 4:
            # Timer
            start = time.time()

            # Create netCDF variable to store the interpolated values for this variable.
            vort_var = ds_out.createVariable(var_name, np.float32, ('time', 'number_parcels'))
            vort_var.units = ds_in.variables[var_name].units
            vort_var.definition = ds_in.variables[var_name].definition

            # Loop over the model files that are in the range of the parcel data.
            for model_time_step in range(file_num_offset+1, file_num_offset+parcel_time_steps+1):
                # Calculate the array index for the back trajectories, which go
                #   backward in time with increasing index.
                parcel_time_step = file_num_offset + parcel_time_steps - model_time_step

                # Get values of this budget variable at this time step.
                variable = np.copy(ds_in.variables[var_name][model_time_step,:,:,:])

                # Get back trajectory coordinates at this time step.
                x_traj_coord = xpos[parcel_time_step]
                y_traj_coord = ypos[parcel_time_step]
                z_traj_coord = zpos[parcel_time_step]

                # Create array representing the points that the budget variable is
                #   going to be sampled at.
                ##traj_points = np.stack((z_coord, y_coord, x_coord), axis = 1)
                traj_points = np.column_stack((z_traj_coord, y_traj_coord, x_traj_coord))

                # Interpolate the budget variable to the back trajectory points and
                #   output to the netCDF file.
                vort_var[parcel_time_step,:] = interpolate.interpn(grid_coord, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

            end = time.time()
            print('Variable {:s} took {:.2f} seconds'.format(var_name, end-start))

    return

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def closeNCfile(ds):
    ds.close()
    return

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if len(sys.argv) > 2:
    # Model run that is being used.
    version_number = sys.argv[1]
    # Set of back trajectories to analyze.
    parcel_label = sys.argv[2]
else:
    print('Parcel label or version number was not specified.')
    print('Syntax: python3 calc_back_traj_vort_tendency.py model_version parcel_label')
    print('Example: python3 calc_back_traj_vort_tendency.py v5 v5_meso_tornadogenesis')
    print('Currently supported version numbers: 4, 5')
    sys.exit()

if version_number == '3' or version_number =='10s':
    print('Version number is not valid.')
    print('Currently supported version numbers: 4, 5')
    sys.exit()

# Directory containing back trajectory data (in numpy archive format).
back_traj_dir = 'back_traj_npz_{:s}/'.format(version_number)
# Directory containing CM1 model netCDF files.
model_dir = '75m_100p_{:s}/'.format(version_number)

# Model height level below which trajectory data is no longer safe to use
#   (generally the height of the lowest non-boundary w point).
min_usable_z_height = 30.

# Set a minimum number of valid values (time steps) that a trajectory must
#   have to be used in analysis.
#   Value of 108 is equivalent to having 18 minutes of good data for this
#   output frequency (10 seconds).
time_length_requirement = 108

# Load data from uncompressed numpy archive.
traj_data = np.load(back_traj_dir + 'backtraj_{:s}.npz'.format(parcel_label))
xpos = traj_data['xpos']
ypos = traj_data['ypos']
zpos = traj_data['zpos']
parcel_dimensions = traj_data['parcel_dimension']
total_parcel_num = np.prod(parcel_dimensions)
# Adding 0 to the file value to make sure that the output is an integer.
file_num_offset = traj_data['offset'] + 0

# Number of back trajectory parcel output times.
parcel_time_steps = len(xpos)

# Counter for the number of trajectories that have a full set of usable data.
fully_valid_traj_num = 0
# Counter for the number of trajectories that are valid up to the specified time length requirement.
partially_valid_traj_num = 0
# Array for the first index with an unusable parcel position.
first_invalid = np.zeros((total_parcel_num))

for i in range(total_parcel_num):
    # Check for indices with nan in a given trajectory. 
    x_nan = np.argwhere(np.isnan(xpos[:,i]))
    y_nan = np.argwhere(np.isnan(ypos[:,i]))
    z_nan = np.argwhere(np.isnan(zpos[:,i]))
    # Check for indices where the trajectory is below the minimum usable threshold
    z_less = np.argwhere(zpos[:,i] < min_usable_z_height)

    # If size of all check arrays is 0, then there is no unusable data, so
    #   trajectory is fully valid.  First invalid index is set to -1 to be
    #   easily identifiable later.
    if x_nan.size == 0 and y_nan.size == 0 and z_nan.size == 0 and z_less.size == 0:
        fully_valid_traj_num += 1
        first_invalid[i] = -1
    # Otherwise, find the minimum index from each check, and set the first
    #   invalid index to that value (Comparison with time_length_requirement
    #   done later).
    else:
        # If only some of the check arrays have a size of 0, just taking
        #   np.min() will return an error. For these cases, set the min at a
        #   value greater than the number of parcel time steps so that it does
        #   not get selected as the first invalid index. 
        x_nan_min = parcel_time_steps + 1 if x_nan.size == 0 else np.min(x_nan)
        y_nan_min = parcel_time_steps + 1 if y_nan.size == 0 else np.min(y_nan)
        z_nan_min = parcel_time_steps + 1 if z_nan.size == 0 else np.min(z_nan)
        z_less_min = parcel_time_steps + 1 if z_less.size == 0 else np.min(z_less)
        first_invalid[i] = np.min([x_nan_min, y_nan_min, z_nan_min, z_less_min])
        if first_invalid[i] >= time_length_requirement:
            partially_valid_traj_num += 1

# Arrays for back trajectories that have a full set of usable data.
xpos_fully_valid = np.zeros((parcel_time_steps, fully_valid_traj_num))
ypos_fully_valid = np.zeros((parcel_time_steps, fully_valid_traj_num))
zpos_fully_valid = np.zeros((parcel_time_steps, fully_valid_traj_num))

# Arrays for back trajectories that are valid up to the specified time length requirement.
xpos_partially_valid = np.zeros((time_length_requirement, partially_valid_traj_num))
ypos_partially_valid = np.zeros((time_length_requirement, partially_valid_traj_num))
zpos_partially_valid = np.zeros((time_length_requirement, partially_valid_traj_num))

# Fully Valid Counter
j = 0
# Partially Valid Counter
k = 0
# Store back trajectories with all usable data or selected amount of partially
#   usable data into different arrays. 
for i in range(total_parcel_num):
    if first_invalid[i] == -1:
        xpos_fully_valid[:,j] = xpos[:,i]
        ypos_fully_valid[:,j] = ypos[:,i]
        zpos_fully_valid[:,j] = zpos[:,i]
        j += 1
    elif first_invalid[i] >= time_length_requirement:
        xpos_partially_valid[:,k] = xpos[:,i][:time_length_requirement]
        ypos_partially_valid[:,k] = ypos[:,i][:time_length_requirement]
        zpos_partially_valid[:,k] = zpos[:,i][:time_length_requirement]
        k += 1

# Open the netCDF file with values from direct calculation of terms from the vorticity equation.
ds_equation = Dataset(model_dir + 'back_traj_analysis/{:s}_direct_vort_equation.nc'.format(version_number))
# Close the netCDF file when the program exits.
atexit.register(closeNCfile, ds_equation)

# Open the netCDF file with values from CM1 calculations of vorticity budgets.
ds_budget = Dataset(model_dir + 'back_traj_analysis/{:s}_model_vort_budget.nc'.format(version_number))
# Close the netCDF file when the program exits.
atexit.register(closeNCfile, ds_budget)

# Only attempt to calculate fully valid trajectory data if there are fully
#   valid trajectories.
if fully_valid_traj_num > 0:
    # Open an output netCDF file for values interpolated to trajectories that have
    #   a full set of usable data.
    ds_out_full = create_nc_out(version_number, parcel_label, 'fully', fully_valid_traj_num, xpos_fully_valid, ypos_fully_valid, zpos_fully_valid, file_num_offset, model_dir)

    create_time_var(ds_equation, ds_out_full, file_num_offset, parcel_time_steps)

    print('Interpolating vorticity equation to fully valid values.')
    # Interpolate values of the vorticity equation to trajectory positions that
    #   have a full set of usable data.
    interpolate_budget(ds_equation, ds_out_full, xpos_fully_valid, ypos_fully_valid, zpos_fully_valid, file_num_offset, parcel_time_steps)

    print('Interpolating model vorticity budget to fully valid values.')
    # Interpolate values of CM1-calculated vorticity budget variables to trajectory
    #   positions that have a full set of usable data.
    interpolate_budget(ds_budget, ds_out_full, xpos_fully_valid, ypos_fully_valid, zpos_fully_valid, file_num_offset, parcel_time_steps)

    ds_out_full.close()
else:
    print('No fully valid trajectories for this dataset.')

# Only calculate and output the partially valid trajectory data if there are
#   partially valid trajectories.
if partially_valid_traj_num > 0:
    # Open an output netCDF file for values interpolated to trajectories that
    #   are valid up to the specified time length requirement.
    ds_out_partial = create_nc_out(version_number, parcel_label, 'partially', partially_valid_traj_num, xpos_partially_valid, ypos_partially_valid, zpos_partially_valid, file_num_offset, model_dir)

    create_time_var(ds_equation, ds_out_partial, file_num_offset, time_length_requirement)

    print('Interpolating vorticity equation to partially valid values.')
    # Interpolate values of the vorticity equation to trajectory positions that
    #   are valid up to the specified time length requirement.
    interpolate_budget(ds_equation, ds_out_partial, xpos_partially_valid, ypos_partially_valid, zpos_partially_valid, file_num_offset, time_length_requirement)

    print('Interpolating model vorticity budget to partially valid values.')
    # Interpolate values of CM1-calculated vorticity budget variables to trajectory
    #   positions that are valid up to the specified time length requirement.
    interpolate_budget(ds_budget, ds_out_partial, xpos_partially_valid, ypos_partially_valid, zpos_partially_valid, file_num_offset, time_length_requirement)

    ds_out_partial.close()
else:
    print('No partially valid trajectories for this dataset.')

