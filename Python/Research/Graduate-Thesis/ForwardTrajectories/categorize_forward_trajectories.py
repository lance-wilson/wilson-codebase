#!/usr/bin/env python3
#
# Name:
#   categorize_forward_trajectories.py
#
# Purpose:  Determine which CM1 forward trajectories come from a certain
#           region of the storm.
#
# Syntax: python3 categorize_forward_trajectories.py version_number parcel_label
#
#   Input: CM1 netCDF model files
#          netCDF file containing vorticity budgets interpolated to forward
#               trajectory positions accessed via Forward_traj_ds in
#               forward_traj_interp_class.py
#
# Execution Example:
#   python3 categorize_forward_trajectories.py v5 1000parcel_tornadogenesis
#
# Modification History:
#   2019/09/19 - Lance Wilson:  Modified from code written by Tom Gowan, using
#                               trajectories_plot.ipynb from:
# https://github.com/tomgowan/trajectories/blob/master/trajectories_plot.ipynb
#   2019/10/01 - Lance Wilson:  Split 3D plot into separate file, as that is
#                               likely what will be used going forward.
#   2020/11/23 - Lance Wilson:  New file to plot trajectory positions from a
#                               cm1out_pdata.nc file.
#   2020/12/18 - Lance Wilson:  Attempting to combine
#                               plot_trajectory_3d_20191001.py and
#                               plot_output_trajectory_3d_test.py.
#   2021/02/23 - Lance Wilson:  Plot script to go with 1D array version of
#                               calc_back_trajectory_meters.
#   2021/09/17 - Lance Wilson:  Simplified for loop in plotting section.
#   2021/10/26 - Lance Wilson:  Split from plot_back_traj_simpler_loop to
#                               accommodate vorticity budget data.
#   2021/11/09 - Lance Wilson:  Modified to calculate the file numbers to plot
#                               before the plotting loop (eliminates the need
#                               for the time loop).
#   2021/11/23 - Lance Wilson:  Implemented use of Back_traj_ds object for
#                               accessing data.
#   2021/12/14 - Lance Wilson:  Split from plot_back_traj_budgets to determine
#                               which trajectories are in the forward flank.
#   2022/01/27 - Lance Wilson:  Adjusted access of catergorized trajectory
#                               object to accommodate new method of setting up
#                               the netCDF file.
#   2022/04/14 - Lance Wilson:  Modified categorize_trajectories to work with
#                               CM1 forward trajectories and automate some of
#                               the categorization.
#

from netCDF4 import Dataset
from netCDF4 import MFDataset
from scipy import interpolate

import atexit
import itertools
import numpy as np
import operator
import sys

from categorize_forward_traj_class import Cat_forward_traj
from forward_traj_interp_class import Forward_traj_ds
from trajectory_category_parameters import termination_parameters, category_parameters

# Close the main CM1 model data netCDF file.
def closeNCfile(ds):
    ds.close()

# Determine what valid indices remain (valid_traj_indices) after calculating
#   the valid trajectories based on a specific condition (valid_this_case).
def eval_valid_indices(valid_traj_indices, valid_this_case):
    # If both arrays have indices, find the intersection of the two arrays.
    if valid_traj_indices.size != 0 and valid_this_case.size != 0:
        valid_traj_indices = np.intersect1d(valid_traj_indices, valid_this_case)
    # Otherwise, the valid indices are whatever is valid for this condition.
    #   Note: If valid_this_case is empty, then valid_traj_indices should
    #   remain empty after the else block.
    else:
        valid_traj_indices = np.copy(valid_this_case)
    return valid_traj_indices

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Command-line arguments.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mandatory_arg_num = 2

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
else:
    print('Model version number and parcel label must be specified.')
    print('Syntax: python3 categorize_trajectories.py version_number parcel_label')
    print('Example: python3 categorize_trajectories.py v5 1000parcel_tornadogenesis')
    print('Currently supported version numbers: v4, v5')
    print('Set budget_variable to \'all\' to plot all variables.')
    sys.exit()

if version_number == '3' or version_number =='10s':
    print('Version number is not valid.')
    print('Currently supported version numbers: 4, 5')
    sys.exit()

if version_number.startswith('v'):
    run_number = int(version_number[-1])
else:
    run_number = 3

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# User-Defined Input/Output Directories and Constants
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Directory with CM1 model output.
model_dir = '75m_100p_{:s}/'.format(version_number)
# Directory where forward trajectory analysis data is stored.
analysis_dir = model_dir + 'forward_traj_analysis/'
# Directory with netCDF files of vorticity budget data interpolated to trajectory locations.
interp_dir = analysis_dir + 'parcel_interpolation/'
# Directory for output images.
output_dir = analysis_dir + 'categorized_trajectories/'

termination_region = 'mesocyclone'

# Dictionary storing mathmatical operators from the operator module so that
#   operators can be determined on a case-by-case basis.
# Examples: ops['<'](a,b) is equivalent to: operator.lt(a,b); a < b
ops =  {'<=' : operator.le,
        '>=' : operator.ge,
        '<'  : operator.lt,
        '>'  : operator.gt,
    }

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create object that opens netCDF files containing vorticity budget data
#   interpolated to forward trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
traj_ds_obj = Forward_traj_ds(version_number, interp_dir, parcel_label)
traj_ds_obj.read_data()

# Position data for the forward trajectories.
xpos = traj_ds_obj.xpos
ypos = traj_ds_obj.ypos
zpos = traj_ds_obj.zpos

# Total number of parcels for this set of data.
total_parcel_num = traj_ds_obj.total_parcel_num

# Model file at the earliest time of the trajectory dataset (zero-indexed,
#   add one to get the correct CM1 model file).
file_num_offset = traj_ds_obj.file_num_offset

# Get the number of time steps in the full set of parcel data.
parcel_time_step_num = traj_ds_obj.parcel_time_step_num

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset over the time period where forward trajectories are calculated.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset, file_num_offset+parcel_time_step_num)]
ds = MFDataset(file_list)

# Close the main CM1 data netCDF file when the program exits.
atexit.register(closeNCfile, ds)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Regular grid coordinates to use for interpolation.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Coordinates in each dimension (converted to meters).
x_coord = np.copy(ds.variables['xh'])*1000.
y_coord = np.copy(ds.variables['yh'])*1000.
z_coord = np.copy(ds.variables['z'])*1000.

# Staggered coordinates in each dimension (converted to meters).
x_coord_stag = np.copy(ds.variables['xf'])*1000.
y_coord_stag = np.copy(ds.variables['yf'])*1000.
z_coord_stag = np.copy(ds.variables['zf'])*1000.

# Times in the simulation for this data range.
time_coord = np.copy(ds.variables['time'][:])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Categorize trajectories.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
print('Valid starting trajectories:\t{:d}'.format(total_parcel_num))

print('---------------------------------------------------------------')

# Dictionaries of parameters for all termination regions.
end_point_dict = termination_parameters()
# Dictionaries of parameters for all categories.
category_dict = category_parameters()

for end_point_param_key, category_param_key in itertools.product(end_point_dict.keys(), category_dict.keys()):

    print('Calculating trajectories for termination region \'{:s}\', category \'{:s}\''.format(end_point_param_key, category_param_key))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Find trajectories that terminate in the mesocyclone
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Parameters used for determining if the trajectory ends in the correct place.
    end_point_params = end_point_dict[end_point_param_key]

    valid_traj_indices = np.empty((0,))

    # List of keys that do not have a value of None for the this set of
    #   trajectory end points.
    defined_end_point_keys = [key for key in end_point_params.keys() if end_point_params[key]]

    for key in defined_end_point_keys:
        if key.startswith('x'):
            positions = xpos[-1]
        if key.startswith('y'):
            positions = ypos[-1]
        if key.startswith('z'):
            positions = zpos[-1]

        if key.endswith('max'):
            # Determine which trajectories remain below the required limit over
            #   the prescribed time period.
            valid_this_case = np.argwhere(positions <= end_point_params[key])[:,0]
            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After mesocyclone {:s}:\t{:d}'.format(key, valid_traj_indices.size))

        elif key.endswith('min'):
            # Determine which trajectories remain above the required limit over
            #   the prescribed time period.
            valid_this_case = np.argwhere(positions >= end_point_params[key])[:,0]
            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After mesocyclone {:s}:\t{:d}'.format(key, valid_traj_indices.size))

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If looking at the threshold criteria, make a list of the model fields
        #   needed for comparision.
        if key == 'thresholds':
            model_fields = [threshold for threshold in end_point_params[key].keys()]
        # If the key is not 'thresholds', create an empty list so the for loop
        #   does not run.
        else:
            model_fields = []

        for model_field in model_fields:
            # Array index of model height.
            model_level = end_point_params[key][model_field][0]
            # Value to compare the model variable data against.
            field_value = end_point_params[key][model_field][1]
            # Whether the values along the trajectory should be e.g. less than
            #   or greater than the comparison value.
            operator = end_point_params[key][model_field][2]

            # Determine which model coordinates to use (must use staggered
            #   grids if interpolating velocity values).
            x_coord_field = x_coord_stag if model_field == 'u' else x_coord
            y_coord_field = y_coord_stag if model_field == 'v' else y_coord

            # Regular grid points for one model level at one time.
            grid_coord_2D = (y_coord_field,x_coord_field)

            # Get values of this budget variable at this time step.
            variable = np.copy(ds.variables[model_field][-1,model_level,:,:])

            # Get forward trajectory coordinates at this time step.
            x_traj_coord = xpos[-1]
            y_traj_coord = ypos[-1]

            # Create array representing the points that the model variable is
            #   going to be sampled at.
            traj_points = np.column_stack((y_traj_coord, x_traj_coord))

            # Interpolate the model variable to the forward trajectory points.
            interpolated_values = interpolate.interpn(grid_coord_2D, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

            # Find trajectories that meet the criterion at this time.
            valid_this_case = np.argwhere(ops[operator](interpolated_values, field_value))[:,0]

            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After mesocyclone {:s}:\t{:d}'.format(model_field, valid_traj_indices.size))

    #print('Remaining trajectories after {:s} termination region:\t{:d}'.format(end_point_param_key, valid_traj_indices.size))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if valid_traj_indices.size == 0:
        print('No trajectories terminate within the {:s} termination region for this dataset.'.format(end_point_param_key))
        sys.exit()

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Find trajectories that are part of this category.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Parameters to be used to determine if the forward trajectory belongs to a
    # certain category.
    category_params = category_dict[category_param_key]

    # List of keys that do not have a value of None for this category.
    defined_category_keys = [key for key in category_params.keys() if category_params[key]]

    for key in defined_category_keys:
        # First and last index of data to collect (based on percentage of data).
        if key.startswith('x') or key.startswith('y') or key.startswith('z'):
            start_time_limit_index = int(parcel_time_step_num * category_params[key][1] / 100.)
            end_time_limit_index =  int(parcel_time_step_num * category_params[key][2] / 100.)

        if key.startswith('x'):
            traj_points = xpos[start_time_limit_index:end_time_limit_index]

        if key.startswith('y'):
            traj_points = ypos[start_time_limit_index:end_time_limit_index]

        if key.startswith('z'):
            traj_points = zpos[start_time_limit_index:end_time_limit_index]

        if key.endswith('max'):
            max_values = np.max(traj_points, axis=0)

            # Determine which trajectories remain below the limit over the
            #   prescribed time period.
            valid_this_case = np.argwhere(max_values <= category_params[key][0])[:,0]
            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After category {:s}:\t{:d}'.format(key, valid_traj_indices.size))

        elif key.endswith('min'):
            min_values = np.min(traj_points, axis=0)

            # Determine which trajectories remain above the limit over the
            #   prescribed time period.
            valid_this_case = np.argwhere(min_values >= category_params[key][0])[:,0]
            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After category {:s}:\t{:d}'.format(key, valid_traj_indices.size))

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If looking at the threshold criteria, make a list of the model fields
        #   needed for comparision.
        if key == 'thresholds':
            model_fields = [threshold for threshold in category_params[key].keys()]
        # If the key is not 'thresholds', create an empty list so the for loop
        #   does not run.
        else:
            model_fields = []

        for model_field in model_fields:
            # Array index of model height.
            model_level = category_params[key][model_field][0]
            # Value to compare the model variable data against.
            field_value = category_params[key][model_field][1]
            # Whether the values along the trajectory should be e.g. less than
            #   or greater than the comparison value.
            operator = category_params[key][model_field][2]
            # Whether the entire trajectory or just part of it should be the criterion.
            domain_required = category_params[key][model_field][3]

            # Determine which model coordinates to use (must use staggered
            #   grids if interpolating velocity values).
            x_coord_field = x_coord_stag if model_field == 'u' else x_coord
            y_coord_field = y_coord_stag if model_field == 'v' else y_coord
            z_coord_field = z_coord_stag if model_field == 'w' else z_coord

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # Case if all trajectory points must meet the criterion.
            if domain_required == 'all':
                # Regular grid points for one model level at one time.
                grid_coord_2D = (y_coord_field,x_coord_field)

                remaining_valid = np.copy(valid_traj_indices)
                for time_step in range(parcel_time_step_num):
                    # Get values of this budget variable at this time step.
                    variable = np.copy(ds.variables[model_field][time_step,model_level,:,:])

                    # Get forward trajectory coordinates at this time step.
                    x_traj_coord = xpos[time_step, remaining_valid]
                    y_traj_coord = ypos[time_step, remaining_valid]

                    # Create array representing the points that the model
                    #   variable is going to be sampled at.
                    traj_points = np.column_stack((y_traj_coord, x_traj_coord))

                    # Interpolate the model variable to the forward trajectory points.
                    interpolated_values = interpolate.interpn(grid_coord_2D, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

                    # Indices of remaining_valid array valid at this time step.
                    valid_this_time_subset = np.argwhere(ops[operator](interpolated_values, field_value))[:,0]

                    # Indices of full index array valid at this time step.
                    valid_this_time_full = remaining_valid[valid_this_time_subset]

                    # Remaining valid indices for all times steps
                    remaining_valid = eval_valid_indices(remaining_valid, valid_this_time_full)

                # Determine which valid indices remain.
                valid_traj_indices = eval_valid_indices(valid_traj_indices, remaining_valid)

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # Case if any of the trajectory points must meet the criterion.
            if domain_required == 'any':
                grid_coord_time = (np.round(time_coord, -1),y_coord_field,x_coord_field)
                remaining_valid = []
                # Get values of this budget variable at all time steps.
                variable = np.copy(ds.variables[model_field][:,model_level,:,:])

                for parcel_num in valid_traj_indices:
                    # Get this forward trajectory's coordinates at all time steps.
                    x_traj_coord = xpos[:, parcel_num]
                    y_traj_coord = ypos[:, parcel_num]
                    z_traj_coord = zpos[:, parcel_num]
                    time_traj_coord = np.round(traj_ds_obj.simulation_times, -1)

                    # Create array representing the points that the model
                    #   variable is going to be sampled at.
                    traj_points = np.column_stack((time_traj_coord, y_traj_coord, x_traj_coord))

                    # Interpolate the model variable to the forward trajectory points.
                    interpolated_values = interpolate.interpn(grid_coord_time, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

                    # Find indices of times where this trajectory meets the criterion.
                    valid_this_time_subset = np.argwhere(ops[operator](interpolated_values, field_value))[:,0]

                    # If any time meets the criterion, add this trajectory to
                    #   the list of remaining valid trajectories.
                    if valid_this_time_subset.size != 0:
                        remaining_valid.append(parcel_num)

                remaining_valid = np.array(remaining_valid)

                # Determine which valid indices remain.
                valid_traj_indices = eval_valid_indices(valid_traj_indices, remaining_valid)

            #print('After category {:s}:\t{:d}'.format(model_field, valid_traj_indices.size))

    print('Final trajectories in category {:s}:\t{:d}'.format(category_param_key, valid_traj_indices.size))
    print('---------------------------------------------------------------')

    # Trajectory initial positions that are to be output.
    x_val = xpos[0,valid_traj_indices]
    y_val = ypos[0,valid_traj_indices]
    z_val = zpos[0,valid_traj_indices]

    output_initial_pos = np.column_stack((z_val,y_val,x_val))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Output the set of points to the file for this category.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    cat_traj_obj = Cat_forward_traj(version_number, output_dir, parcel_label, category_param_key)
    # Creating a new file for now since it is probably not desirable to append
    #   data when categorizing things automatically.
    cat_traj_obj.create_new_nc(category_param_key)

    cat_traj_obj.write_data(output_initial_pos)

