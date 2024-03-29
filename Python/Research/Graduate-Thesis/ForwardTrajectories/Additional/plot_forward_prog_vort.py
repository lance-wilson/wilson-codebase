#!/usr/bin/env python3
#
# Name:
#   plot_forward_prog_vort.py
#
# Purpose:  Compare CM1 model output vorticity with "prognostic" vorticity
#           calculated by integrating vorticity tendencies from an initial
#           vorticity point.
#           Integration equation:
#                   zeta_t_n = zeta_t_(n-1) + sum(tend_n) * delta_t
#
# Syntax: python3 plot_forward_prog_vort.py version_number parcel_label parcel_category number_plots
#
#   Input:
#
# Execution Example:
#   python3 plot_forward_prog_vort.py v5 1000parcel_tornadogenesis forward_flank 4
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
from parameter_list import title_dir_sub

from netCDF4 import Dataset
from netCDF4 import MFDataset
from scipy import interpolate

import atexit
import matplotlib.pyplot as plt
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
def calc_prog_vort(prog_vort, start_time_index, plot_limit, plot_index, time_step_lengths, budget_var_names):
    for out_arr_i, obj_i in enumerate(range(start_time_index+1, start_time_index+plot_limit+1)):
        tend_sum = 0.
        for budget_var in budget_var_names:
            tend_sum += ds_obj.getBudgetData(budget_var)[obj_i, plot_index]

        prog_vort[out_arr_i+1] = prog_vort[out_arr_i] + tend_sum * time_step_lengths[out_arr_i]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Plot the "prognostic" vorticity for the equation terms and the model
#   tendency terms along with the "true" vorticity interpolated to trajectory
#   positions.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def plot_prog_vort(simulation_times, prog_budget_vort, prog_equation_vort, cm1_vort, budget_type, output_name):
    # Dimension of the data to put in the title.
    dir_string = title_dir_sub(budget_type)

    title_string = '{:s} Vorticity'.format(dir_string)

    fig1 = plt.figure()

    plt.plot(simulation_times, prog_budget_vort, label='Prog. Budget')
    plt.plot(simulation_times, prog_equation_vort, label='Prog. Equation')
    plt.plot(simulation_times, cm1_vort, label='"True" Value')
    plt.xlim(np.min(simulation_times), np.max(simulation_times))
    plt.xlabel('Time (s)')
    plt.ylabel(r'Vorticity (s$\mathregular{^{-1}}$)')
    plt.title('Comparison of CM1 Model Vorticity and\n"Prognostic" Vorticity from Tendencies\n' + title_string)
    plt.legend(loc='best')
    plt.tight_layout()
    #plt.savefig(output_name, dpi=400)
    plt.show()

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
mandatory_arg_num = 4

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    parcel_category = sys.argv[3]
    number_plots = int(sys.argv[4])
else:
    print('Parcel label and version number must be specified.')
    print('Syntax: python3 plot_forward_prog_vort.py version_number parcel_label parcel_category number_plots')
    print('Example: python3 plot_forward_prog_vort.py v5 1000parcel_tornadogenesis forward_flank 4')
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
# Directory with indices of categorized trajectories ordered by how close they
#   are to a mean prognostic trajectory.
index_dir = cat_dir + 'index_order_from_mean/'
# Directory for output images.
output_dir = analysis_dir + 'ForwardTrajectoryImages/'

# Minutes after initialization time to end integration.
plot_limit_minutes = 10.

# Array index at which to start the integration.
start_time_index = 0

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

# Initialization Position time for parcels.
initialize_time = int(ds_obj.simulation_times[0])

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

plot_indices_file = np.load(index_dir + 'indices_from_mean_{:s}_{:s}_{:s}.npz'.format(version_number, parcel_label, parcel_category))
plot_indices_ordered = plot_indices_file['plot_indices_ordered']
plot_indices = category_indices[plot_indices_ordered[:number_plots]]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate how many time steps of trajectory data to plot (based on
#   user-defined number of minutes to be plotted).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = 60. * plot_limit_minutes

# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds_obj.simulation_times[1:] - ds_obj.simulation_times[:-1])[start_time_index:]

# Cumulative sum array of the time step lengths.
cumulative_time_steps = np.cumsum(time_step_lengths)

# Check that at least one time step is going to be plotted (i.e.
#   plot_limit_seconds must be no smaller than the smallest time_step),
#   otherwise np.argwhere result will be empty and crash the program.
if plot_limit_seconds < time_step_lengths[-1]:
    print('Length of time desired to plot is less than the time step, ' + 
          'so there is no trajectory data to plot.')
    sys.exit()

# How many time steps to plot trajectories.
#   The final row of the np.argwhere output contains the index of the last
#   appropriate time, so the limit for the plotting loop is one more than that.
plot_limit = np.argwhere(cumulative_time_steps <= plot_limit_seconds)[-1,0] + 1

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open the CM1 Dataset.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Number of CM1 file with the starting point vorticity (e.g. 5 minutes before
#   tornadogenesis).
start_file_num = ds_obj.file_num_offset + start_time_index

# List of CM1 model files to open.
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(start_file_num, start_file_num + plot_limit + 1)]
# Open CM1 dataset.
ds = MFDataset(file_list)
# Close the CM1 netCDF file when the program exits.
atexit.register(closeNCfile, ds)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate and plot the "prognostic" vorticity.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Coordinates (in meters) in each dimension.
x_coord = np.copy(ds.variables['xh'])*1000.
y_coord = np.copy(ds.variables['yh'])*1000.
z_coord = np.copy(ds.variables['z'])*1000.

# Get the spatial limits of trajectory data in meters.
xmin_m = np.min(ds_obj.xpos[start_time_index:start_time_index+plot_limit+1, plot_indices])
xmax_m = np.max(ds_obj.xpos[start_time_index:start_time_index+plot_limit+1, plot_indices])
ymin_m = np.min(ds_obj.ypos[start_time_index:start_time_index+plot_limit+1, plot_indices])
ymax_m = np.max(ds_obj.ypos[start_time_index:start_time_index+plot_limit+1, plot_indices])
zmin_m = np.min(ds_obj.zpos[start_time_index:start_time_index+plot_limit+1, plot_indices])
zmax_m = np.max(ds_obj.zpos[start_time_index:start_time_index+plot_limit+1, plot_indices])

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

# Calculate and plot prognostic and correct vorticity for each direction.
for budget_type in sorted(budget_var_names.keys()):

    ds_var = budget_type + 'vort'
    vort_var = np.copy(ds.variables[ds_var][:,zmin:zmax,ymin:ymax,xmin:xmax])

    for plot_index in plot_indices:
        prog_budget_vort = np.zeros((plot_limit+1))
        prog_equation_vort = np.zeros((plot_limit+1))
        interp_vort = np.zeros((plot_limit+1))

        # Starting (earliest time) trajectory positions.
        start_vort_xpos = ds_obj.xpos[start_time_index, plot_index]
        start_vort_ypos = ds_obj.ypos[start_time_index, plot_index]
        start_vort_zpos = ds_obj.zpos[start_time_index, plot_index]

        # Get "correct" vorticity (CM1 vorticity interpolated to trajectory
        #   positions) at each time step.
        for out_arr_i, obj_i in enumerate(range(start_time_index,start_time_index+plot_limit+1)):
            interp_xpos = ds_obj.xpos[obj_i, plot_index]
            interp_ypos = ds_obj.ypos[obj_i, plot_index]
            interp_zpos = ds_obj.zpos[obj_i, plot_index]
            interp_vort[out_arr_i] = interpolate_vort(grid_coord, interp_xpos, interp_ypos, interp_zpos, vort_var[out_arr_i])

        # Starting positions for the prognostic vorticity (same for both tendency sets).
        prog_budget_vort[0] = interpolate_vort(grid_coord, start_vort_xpos, start_vort_ypos, start_vort_zpos, vort_var[0])
        prog_equation_vort[0] = interpolate_vort(grid_coord, start_vort_xpos, start_vort_ypos, start_vort_zpos, vort_var[0])

        # Calculate the "prognostic" vorticity at each time step.
        calc_prog_vort(prog_budget_vort, start_time_index, plot_limit, plot_index, time_step_lengths, budget_var_names[budget_type]['budget'])
        calc_prog_vort(prog_equation_vort, start_time_index, plot_limit, plot_index, time_step_lengths, budget_var_names[budget_type]['equation'])


        image_file_name = output_dir + 'cm1_forwardtraj_progvort_comparison_{:s}_{:s}_inittime{:d}_p{:d}.png'.format(parcel_label, budget_type, initialize_time, plot_index)

        #print(plot_index)

        plot_prog_vort(ds.variables['time'][:], prog_budget_vort, prog_equation_vort, interp_vort, budget_type, image_file_name)

