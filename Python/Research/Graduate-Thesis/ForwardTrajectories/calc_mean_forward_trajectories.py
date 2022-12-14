#!/usr/bin/env python3
#
# Name:
#   calc_mean_forward_trajectories.py
#
# Purpose:  Order a category of forward trajectories based on how close they
#           are to a mean "prognostic" trajectory, with "prognostic" vorticity
#           being calculated by integrating vorticity tendencies from an
#           initial vorticity point.
#           Integration equation:
#                   zeta_t_n = zeta_t_(n-1) + sum(tend_n) * delta_t
#
# Syntax: python3 calc_mean_forward_trajectories.py version_number parcel_label parcel_category
#
#   Input:
#
# Execution Example:
#   python3 calc_mean_forward_trajectories v5 1000parcel_tornadogenesis forward_flank
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
#   2021/11/18 - Lance Wilson:  Split from plot_back_traj_budgets to begin
#                               plotting graphs of each component for an
#                               individual trajectory vs. time.
#   2021/11/26 - Lance Wilson:  Split from plot_back_traj_vort_component to
#                               calculate comparison of model vorticity and
#                               "prognostic" vorticity calculated by
#                               integrating budget data.
#   2021/12/03 - Lance Wilson:  Split from compare_back_traj_prog_vort to perform
#                               the same calculations and plots on the CM1
#                               forward trajectories.
#   2022/05/24 - Lance Wilson:  Split from compare_forward_traj_prog_vort to
#                               plot trajectories most representative of the
#                               category's mean trajectory.
#   2022/06/09 - Lance Wilson:  Splitting calculation of "mean"/representative
#                               trajectory and plotting of prognostic vorticity
#                               into separate programs.
#

from categorize_forward_traj_class import Cat_forward_traj
from forward_traj_interp_class import Forward_traj_ds

from netCDF4 import Dataset
from netCDF4 import MFDataset
from scipy import interpolate

import atexit
import numpy as np
import sys

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Function to close netCDF dataset.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def closeNCfile(ds):
    ds.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the "prognostic" vorticity using the equation:
#       zeta_t_n = zeta_t_(n-1) + sum(tend_n) * delta_t
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_prog_vort(prog_vort, plot_limit, plot_index, time_step_lengths, budget_var_names, axis_num, traj_num):
    for out_arr_i, obj_i in enumerate(range(1, plot_limit)):
        tend_sum = 0.
        for budget_var in budget_var_names:
            tend_sum += ds_obj.getBudgetData(budget_var)[obj_i, plot_index]

        prog_vort[axis_num, out_arr_i+1, traj_num] = prog_vort[axis_num, out_arr_i, traj_num] + tend_sum * time_step_lengths[out_arr_i]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Interpolate CM1 vorticity data to trajectory points.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def interpolate_vort(grid_coord, xpos, ypos, zpos, variable):
    # Create array representing the points that the budget variable is
    #   going to be sampled at.
    ##traj_points = np.stack((z_coord, y_coord, x_coord), axis = 1)
    traj_points = np.column_stack((zpos, ypos, xpos))

    # Interpolate the budget variable to the forward trajectory points.
    return interpolate.interpn(grid_coord, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Command line arguments
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mandatory_arg_num = 3

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    parcel_category = sys.argv[3]
else:
    print('Parcel label and version number must be specified.')
    print('Syntax: python3 calc_mean_forward_trajectories version_number parcel_label parcel_category')
    print('Example: python3 calc_mean_forward_trajectories v5 1000parcel_tornadogenesis forward_flank')
    print('Currently supported version numbers: v4, v5')
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
# Directory with netCDF files of initialization positions of categorized
#   forward trajectories.
cat_dir = analysis_dir + 'categorized_trajectories/'
# Directory for output images.
output_dir = cat_dir + 'index_order_from_mean/' 

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open object using netCDF files containing vorticity budget data interpolated
#   to forward trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ds_obj = Forward_traj_ds(version_number, interp_dir, parcel_label)
ds_obj.read_data()

# Create a dictionary of the six subsets of vorticity budget data that are to
#   be plotted (representing both the direct vorticity equation calculation and
#   the vorticity tendencies calculated from CM1 momentum budget in all three
#   spatial dimensions). 
budget_var_names = {}
for axis in ['x', 'y', 'z']:
    budget_var_names[axis] = {}
    budget_var_names[axis]['budget'] = []
    budget_var_names[axis]['equation'] = []
# Sort the budget variable labels into the appropriate subset of the dictionary.
for key in ds_obj.budget_var_keys:
    # Since the trajectories are moving along with the flow, need to look at
    #   the total derivative, so don't include the advection terms.
    if 'advection' in key or 'adv' in key:
        pass
    # Since the model tendency advection terms include the components for
    #   stretching and tilting, the manually calculated components must be
    #   included in the model budget terms.
    elif 'stretch' in key or 'tilt' in key:
        budget_var_names[key[0]]['budget'].append(key)
        budget_var_names[key[0]]['equation'].append(key)
    else:
        if 'vortb' in key:
            budget_var_names[key[0]]['budget'].append(key)
        else:
            budget_var_names[key[0]]['equation'].append(key)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Trajectories to be plotted, based on intialization positions stored in a
#   netCDF file created by categorize_forward_trajectories.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cat_traj_obj = Cat_forward_traj(version_number, cat_dir, parcel_label, parcel_category)
# It is possible that a file could be created without there being any data in
#   it, so plots will only be attempted if the object's "existing_file" flag
#   is true.
if cat_traj_obj.existing_file:
    cat_traj_obj.open_file(parcel_category)
    # Initialization positions are converted to an array index.
    category_indices = cat_traj_obj.meters_to_trajnum(ds_obj.xpos, ds_obj.ypos, ds_obj.zpos)
else:
    print 'Categorized trajectory file does not contain any data'
    sys.exit()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds_obj.simulation_times[1:] - ds_obj.simulation_times[:-1])

# How many time steps to plot trajectories.
plot_limit = len(ds_obj.xpos)

# List of CM1 model files to open.
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(ds_obj.file_num_offset, ds_obj.file_num_offset + plot_limit)]
# Open CM1 dataset.
ds = MFDataset(file_list)
# Close the CM1 netCDF file when the program exits.
atexit.register(closeNCfile, ds)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the "prognostic" vorticity for each set of trajectories.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Coordinates (in meters) in each dimension.
x_coord = np.copy(ds.variables['xh'])*1000.
y_coord = np.copy(ds.variables['yh'])*1000.
z_coord = np.copy(ds.variables['z'])*1000.

prog_budget_vort = np.zeros((len(budget_var_names.keys()), plot_limit, len(category_indices)))
prog_equation_vort = np.zeros((len(budget_var_names.keys()), plot_limit, len(category_indices)))
interp_vort = np.zeros((len(budget_var_names.keys()), plot_limit, len(category_indices)))

# Get the limits of trajectory data in meters.
xmin_m = np.min(ds_obj.xpos[:plot_limit, category_indices])
xmax_m = np.max(ds_obj.xpos[:plot_limit, category_indices])
ymin_m = np.min(ds_obj.ypos[:plot_limit, category_indices])
ymax_m = np.max(ds_obj.ypos[:plot_limit, category_indices])
zmin_m = np.min(ds_obj.zpos[:plot_limit, category_indices])
zmax_m = np.max(ds_obj.zpos[:plot_limit, category_indices])

# Get indices of the limits of the data to save time when accessing CM1
#   vorticity data.
xmin = np.argwhere(np.abs(x_coord - xmin_m) == np.min(np.abs(x_coord - xmin_m)))[0,0]-1
xmax = np.argwhere(np.abs(x_coord - xmax_m) == np.min(np.abs(x_coord - xmax_m)))[0,0]+2
ymin = np.argwhere(np.abs(y_coord - ymin_m) == np.min(np.abs(y_coord - ymin_m)))[0,0]-1
ymax = np.argwhere(np.abs(y_coord - ymax_m) == np.min(np.abs(y_coord - ymax_m)))[0,0]+2
zmin = np.argwhere(np.abs(z_coord - zmin_m) == np.min(np.abs(z_coord - zmin_m)))[0,0]-1
zmax = np.argwhere(np.abs(z_coord - zmax_m) == np.min(np.abs(z_coord - zmax_m)))[0,0]+2

# Create a tuple of the coordinates that is passed to the interpn function
#   to be used as the regular grid.
grid_coord = (z_coord[zmin:zmax], y_coord[ymin:ymax], x_coord[xmin:xmax])

# Calculate prognostic and correct vorticity for each direction.
for axis_num, budget_type in enumerate(sorted(budget_var_names.keys())):

    ds_var = budget_type + 'vort'
    vort_var = np.copy(ds.variables[ds_var][:,zmin:zmax,ymin:ymax,xmin:xmax])

    for traj_num, category_index in enumerate(category_indices):

        # Starting (earliest time) trajectory positions.
        start_vort_xpos = ds_obj.xpos[0, category_index]
        start_vort_ypos = ds_obj.ypos[0, category_index]
        start_vort_zpos = ds_obj.zpos[0, category_index]

        # Get "correct" vorticity (CM1 vorticity interpolated to trajectory
        #   positions) at each time step.
        for out_arr_i, obj_i in enumerate(range(plot_limit)):
            interp_xpos = ds_obj.xpos[obj_i, category_index]
            interp_ypos = ds_obj.ypos[obj_i, category_index]
            interp_zpos = ds_obj.zpos[obj_i, category_index]
            interp_vort[axis_num, out_arr_i, traj_num] = interpolate_vort(grid_coord, interp_xpos, interp_ypos, interp_zpos, vort_var[out_arr_i])

        # Starting positions for the prognostic vorticity (same for both tendency sets).
        prog_budget_vort[axis_num, 0, traj_num] = interpolate_vort(grid_coord, start_vort_xpos, start_vort_ypos, start_vort_zpos, vort_var[0])
        prog_equation_vort[axis_num, 0, traj_num] = interpolate_vort(grid_coord, start_vort_xpos, start_vort_ypos, start_vort_zpos, vort_var[0])

        # Calculate the "prognostic" vorticity at each time step.
        calc_prog_vort(prog_budget_vort, plot_limit, category_index, time_step_lengths, budget_var_names[budget_type]['budget'], axis_num, traj_num)
        calc_prog_vort(prog_equation_vort, plot_limit, category_index, time_step_lengths, budget_var_names[budget_type]['equation'], axis_num, traj_num)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Determine each trajectory's ordered difference from the mean trajectory.
#   Difference from mean is determined as the sum of squares of differences
#   from the mean of each directional component individually.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mean_budget_vort = np.mean(prog_budget_vort, axis=2)
budget_diff_sqd = np.square(prog_budget_vort - mean_budget_vort[:,:,None])
budget_sum_squares = np.sum(budget_diff_sqd, axis=(0,2))

mean_equation_vort = np.mean(prog_equation_vort, axis=2)
equation_diff_sqd = np.square(prog_equation_vort - mean_equation_vort[:,:,None])
equation_sum_squares = np.sum(equation_diff_sqd, axis=(0,2))

combine_sum_squares = budget_sum_squares + equation_sum_squares
mean_sum_index_comp = np.argwhere(combine_sum_squares == np.min(combine_sum_squares))[0,0]

plot_indices = np.argwhere(combine_sum_squares <= sorted(combine_sum_squares)[-1])[:,0]

order_of_indices = np.argwhere(sorted(combine_sum_squares) == combine_sum_squares[plot_indices][:,None])[:,1]

plot_indices_ordered = np.zeros((len(plot_indices)), dtype=np.int)
plot_indices_ordered[order_of_indices] = plot_indices

np.savez(output_dir + 'indices_from_mean_{:s}_{:s}_{:s}'.format(version_number, parcel_label, parcel_category), plot_indices_ordered=plot_indices_ordered)

