#!/usr/bin/env python3
#
# Name:
#   calc_forward_traj_vort_tendency.py
#
# Purpose:  Interpolate values of terms of the 3D vorticity equation and values
#           of CM1-calculated vorticity budget variables to the positions of
#           forward trajectories.
#
# Syntax: python3 calc_forward_traj_vort_tendency.py model_version parcel_label
#
#   Input: A CM1 parcel data netCDF file ("cm1out_pdata_{parcel_label}.nc")
#           The namelist ("namelist_{parcel_label}.input") used to initialize
#           the model run that generated the parcel data file,
#           NetCDF files named "(model_version)_direct_vort_equation.nc"
#           and "(model_version)_direct_vort_equation.nc" containing vorticity
#           budget terms calculated at thermodynamic grid points.
#
# Execution Example:
#   python3  calc_forward_traj_vort_tendency.py v5 v5_meso_tornadogenesis
#
# Temporary Execution Example (Run local script on server):
#   ssh vortex python < calc_forward_traj_vort_tendency.py - v5 v5_meso_tornadogenesis
#
# Modification History:
#   2021/09/15 - Lance Wilson:  Created, partially from unstaggered_trajectory_test.py,
#                               some pieces from code written by Tom Gowan, using
#                               trajectories_CM1.ipynb from: https://github.com/tomgowan/trajectories/blob/master/trajectories_CM1.ipynb
#   2021/02/24 - Lance Wilson:  Created forward trajectory version from
#                               calc_back_traj_vort_tendency.
#

from forward_traj_interp_class import Forward_traj_ds
from calc_file_num_offset import calc_parcel_start_time, calc_parcel_end_time, calc_file_offset

from netCDF4 import Dataset
from scipy import interpolate
import atexit
import numpy as np
import sys
import time

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Interpolate vorticity budget data to forward trajectory positions.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def interpolate_budget(ds_in, ds_out_obj, xpos, ypos, zpos, file_num_offset, parcel_time_steps, valid_traj_num):
    # Coordinates (in meters) in each dimension (already converted to meters
    #   in ds_in netCDF file).
    x_coord = np.copy(ds_in.variables['xh'])
    y_coord = np.copy(ds_in.variables['yh'])
    z_coord = np.copy(ds_in.variables['z'])

    # Create a tuple of the coordinates that is passed to the interpn function
    #   to be used as the regular grid.
    grid_coord = (z_coord,y_coord,x_coord)

    for var_name in ds_in.variables.keys():
        if len(ds_in.variables[var_name].dimensions) == 4:
            # Timer
            start = time.time()

            vort_var_out = np.zeros((parcel_time_steps, valid_traj_num))

            # Loop over the model files that are in the range of the parcel data.
            for model_time_step in range(file_num_offset, file_num_offset+parcel_time_steps):
                # Calculate the array index for the forward trajectories.
                parcel_time_step = model_time_step - file_num_offset

                # Get values of this budget variable at this time step.
                variable = np.copy(ds_in.variables[var_name][model_time_step,:,:,:])

                # Get forward trajectory coordinates at this time step.
                x_traj_coord = xpos[parcel_time_step]
                y_traj_coord = ypos[parcel_time_step]
                z_traj_coord = zpos[parcel_time_step]

                # Create array representing the points that the budget variable is
                #   going to be sampled at.
                ##traj_points = np.stack((z_coord, y_coord, x_coord), axis = 1)
                traj_points = np.column_stack((z_traj_coord, y_traj_coord, x_traj_coord))

                # Interpolate the budget variable to the forward trajectory points.
                vort_var_out[parcel_time_step,:] = interpolate.interpn(grid_coord, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

            # Output the interpolated data to the netCDF file.
            ds_out_obj.create_vort_var(ds_in, var_name, vort_var_out)

            end = time.time()
            print('Variable {:s} took {:.2f} seconds'.format(var_name, end-start))

    return

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Close a netCDF dataset (called at end of program when registered with atexit).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def closeNCfile(ds):
    ds.close()
    return

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Start of main program.
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

model_dir = '75m_100p_{:s}/'.format(version_number)
forward_traj_dir = model_dir + 'parcel_files/'
namelist_dir = model_dir + 'namelists/'
output_dir = model_dir + 'forward_traj_analysis/parcel_interpolation/'

parcel_file_name = forward_traj_dir + 'cm1out_pdata_{:s}.nc'.format(parcel_label)
namelist_filename = namelist_dir + 'namelist_{:s}.input'.format(parcel_label)

# Model height level below which trajectory data is no longer safe to use
#   (generally the height of the lowest non-boundary w point).
min_usable_z_height = 30.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load forward trajectory data from the cm1out_pdata netCDF file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parcel_start_time = calc_parcel_start_time(parcel_label, namelist_filename)
parcel_end_time = calc_parcel_end_time(parcel_label, namelist_filename)
file_num_offset = calc_file_offset(version_number, parcel_start_time)

ds_parcel = Dataset(parcel_file_name, "r")
parcel_times = np.copy(ds_parcel.variables['time'][:])

parcel_start_diff = np.abs(parcel_times - parcel_start_time)
parcel_end_diff = np.abs(parcel_times - parcel_end_time)

parcel_start_index = np.argwhere(parcel_start_diff == np.min(parcel_start_diff))[0,0]
parcel_end_index = np.argwhere(parcel_end_diff == np.min(parcel_end_diff))[0,0]

xpos = np.copy(ds_parcel.variables['x'][parcel_start_index:parcel_end_index])
ypos = np.copy(ds_parcel.variables['y'][parcel_start_index:parcel_end_index])
zpos = np.copy(ds_parcel.variables['z'][parcel_start_index:parcel_end_index])
parcel_out_times = np.copy(ds_parcel.variables['time'][parcel_start_index:parcel_end_index])
ds_parcel.close()

# Number of parcel output times in the model run.
parcel_time_steps = len(xpos)

# Total number of parcels.
total_parcel_num = xpos[0].size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Determine which trajectories are able to be used.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get indices of values that are above the minimum usable z height threshold.
valid_height_indices = np.argwhere(np.min(zpos, axis=0) >= min_usable_z_height)[:,0]

# Get indices that have non-duplicated starting positions.
unique_x, valid_x_indices = np.unique(xpos, return_index=True, axis=1)
unique_y, valid_y_indices = np.unique(ypos, return_index=True, axis=1)
unique_z, valid_z_indices = np.unique(zpos, return_index=True, axis=1)

# Find indices that are part of all of these groups.
part1 = np.intersect1d(valid_height_indices, valid_x_indices)
part2 = np.intersect1d(valid_y_indices, valid_z_indices)

valid_indices = np.intersect1d(part1, part2)

# New arrays containing the values at the set of sampled indices.
xpos_valid = xpos[:,valid_indices]
ypos_valid = ypos[:,valid_indices]
zpos_valid = zpos[:,valid_indices]

valid_traj_num = len(valid_indices)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open the vorticity budget datasets.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open the netCDF file with values from direct calculation of terms from the
#   vorticity equation.
ds_equation = Dataset(model_dir + 'back_traj_analysis/{:s}_direct_vort_equation.nc'.format(version_number))
# Close the netCDF file when the program exits.
atexit.register(closeNCfile, ds_equation)

# Open the netCDF file with values from CM1 calculations of vorticity budgets.
ds_budget = Dataset(model_dir + 'back_traj_analysis/{:s}_model_vort_budget.nc'.format(version_number))
# Close the netCDF file when the program exits.
atexit.register(closeNCfile, ds_budget)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Interpolate the vorticity budget data to trajectory positions and output to
#   a netCDF file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Only attempt to calculate trajectory data if there are valid trajectories.
if valid_traj_num > 0:
    ds_out_obj = Forward_traj_ds(version_number, output_dir, parcel_label)
    # Open an output netCDF file for values interpolated to trajectories that
    #   have usable data.
    ds_out_obj.create_new_nc(version_number, parcel_label, valid_traj_num, xpos_valid, ypos_valid, zpos_valid, parcel_out_times, file_num_offset)

    print('Interpolating vorticity equation to fully valid values.')
    # Interpolate values of the vorticity equation to trajectory positions that
    #   have usable data.
    interpolate_budget(ds_equation, ds_out_obj, xpos_valid, ypos_valid, zpos_valid, file_num_offset, parcel_time_steps, valid_traj_num)

    print('Interpolating model vorticity budget to fully valid values.')
    # Interpolate values of CM1-calculated vorticity budget variables to
    #   trajectory positions that have usable data.
    interpolate_budget(ds_budget, ds_out_obj, xpos_valid, ypos_valid, zpos_valid, file_num_offset, parcel_time_steps, valid_traj_num)

else:
    print('No valid trajectories for this dataset.')

