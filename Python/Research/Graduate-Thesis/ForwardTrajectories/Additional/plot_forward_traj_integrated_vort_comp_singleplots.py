#!/usr/bin/env python3
#
# Name:
#   plot_forward_traj_integrated_vort_comp_singleplots.py
#
# Purpose:  Plot CM1 forward trajectories visualizing vorticity budget data
#           along the trajectories.
#           This program plots one image at a time (as opposed to multi-panel plots).
#
# Syntax: python3 plot_forward_traj_integrated_vort_comp_singleplots.py version_number parcel_label
#
# Input:  netCDF file containing vorticity budget data interpolated to forward
#           trajectory posititions
#         netCDF file containing intialization positions of forward trajectories
#           determined to be located in a certain region of the storm
#
# Execution Example:
#   python3 plot_forward_traj_integrated_vort_comp_singleplots.py v5 1000parcel_tornadogenesis
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
#   2021/12/21 - Lance Wilson:  Added trajectory categorization object for
#                               selecting the trajectories that are to be
#                               plotted.
#   2022/01/27 - Lance Wilson:  Adjusted access of catergorized trajectory
#                               object to accommodate new method of setting up
#                               the netCDF file.
#   2022/04/08 - Lance Wilson:  Split from plot_back_traj_vort_component to
#                               work with forward trajectory data.
#   2022/08/13 - Lance Wilson:  Combine plot_forward_traj_vort_component and
#                               plot_forward_prog_vort to show total vorticity
#                               components.
#

from forward_traj_interp_class import Forward_traj_ds
from categorize_traj_class import Cat_traj
from parameter_list import budget_legendlabels, title_dir_sub, budget_linecolors

from netCDF4 import Dataset, MFDataset
from scipy import interpolate
import atexit
import itertools
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import sys

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Close the main CM1 model data netCDF file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def closeNCfile(ds):
    ds.close()

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
# Command Line Arguments
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mandatory_arg_num = 4

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    parcel_category = sys.argv[3]
    number_plots = int(sys.argv[4])
else:
    print('Parcel label and version number must be specified.')
    print('Syntax: python3 plot_forward_traj_integrated_vort_comp_singleplots.py version_number parcel_label parcel_category number_plots')
    print('Example: python3 plot_forward_traj_integrated_vort_comp_singleplots.py v5 1000parcel_tornadogenesis forward_flank 4')
    print('Currently supported version numbers: v4, v5')
    sys.exit()

if version_number == 'v3' or version_number == '10s':
    print('Version number is not valid.')
    print('Currently supported version numbers: v4, v5')
    sys.exit()

if version_number.startswith('v'):
    run_number = int(version_number[-1])
else:
    print('Version number format: v#.')
    sys.exit()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# User-Defined Input/Output Directories and Constants
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Directory with CM1 model output.
model_dir = '75m_100p_{:s}/'.format(version_number)
# Directory where back trajectory analysis data is stored
analysis_dir = model_dir + 'forward_traj_analysis/'
# Directory with netCDF files of vorticity budget data interpolated to trajectory locations.
interp_dir = analysis_dir + 'parcel_interpolation/'
# Directory with netCDF files containing parcel initialization positions
#   belong to a particular region of the storm.
cat_dir = analysis_dir + 'categorized_trajectories/'
# Directory with indices of categorized trajectories ordered by how close they
#   are to a mean prognostic trajectory.
index_dir = cat_dir + 'index_order_from_mean/'
# Directory for output images.
output_dir = analysis_dir + 'ForwardTrajectoryImages/'

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open object using netCDF files containing vorticity budget data interpolated
#   to back trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ds_obj = Forward_traj_ds(version_number, interp_dir, parcel_label)
ds_obj.read_data()

# Initialization Position time for parcels.
initialize_time = int(ds_obj.simulation_times[0])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create a dictionary of the six subsets of vorticity budget data that are to
#   be plotted (representing both the direct vorticity equation calculation and
#   the vorticity tendencies calculated from CM1 momentum budget in all three
#   spatial dimensions). 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
budget_var_names = {}
for axis in ['x', 'y', 'z']:
    budget_var_names[axis + '_budget'] = []
    budget_var_names[axis + '_equation'] = []
# Sort the budget variable labels into the appropriate subset of the dictionary.
for key in ds_obj.budget_var_keys:
    # Since the trajectories are moving along with the flow, need to look at
    #   the total derivative, so don't include the advection terms.
    if 'advection' in key or 'adv' in key or 'pgrad' in key:
        pass
    # Since the model tendency advection terms include the components for
    #   stretching and tilting, the manually calculated components must be
    #   included in the model budget terms.
    elif 'stretch' in key or 'tilt' in key:
        budget_var_names[key[0] + '_budget'].append(key)
        budget_var_names[key[0] + '_equation'].append(key)
    else:
        if 'vortb' in key:
            # Turbulence and diffusion variables will be defined; vertical
            #   component is skipped so that they are not added in twice.
            if 'vturb' in key or 'vedif' in key:
                pass
            # Add a combined form of the turbulence and diffusion variables to
            #   list of budget variables.
            elif 'hturb' in key or 'hedif' in key:
                budget_var_names[key[0] + '_budget'].append(ds_obj.remove_dirFromVar(key))
            else:
                budget_var_names[key[0] + '_budget'].append(key)
        else:
            budget_var_names[key[0] + '_equation'].append(key)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Trajectories to be plotted, based on intialization positions stored in a
#   netCDF file created by collect_ff_trajectories.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cat_traj_obj = Cat_traj(version_number, cat_dir, parcel_label, parcel_category)
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
#   total time range of data).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = ds_obj.simulation_times[-1] - ds_obj.simulation_times[0]

# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds_obj.simulation_times[1:] - ds_obj.simulation_times[:-1])

# Cumulative sum array of the time step lengths.
cumulative_time_steps = np.cumsum(time_step_lengths)

# Check that at least one time step is going to be plotted (i.e.
#   plot_limit_seconds must be no smaller than the smallest time_step),
#   otherwise np.argwhere result will be empty and crash the program.
if plot_limit_seconds < time_step_lengths[-1]:
    print('Length of time desired to plot is less than the time step, ' + 
          'so there is no trajectory data to plot.')
    sys.exit()

# How far forward (in time steps) to plot trajectories.
#   The final row of the np.argwhere output contains the index of the last
#   appropriate time, so the limit for the plotting loop is one more than that.
plot_limit = np.argwhere(cumulative_time_steps <= plot_limit_seconds)[-1,0] + 1

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open the CM1 Dataset.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Number of CM1 file with the starting point vorticity (e.g. 5 minutes before
#   tornadogenesis).
start_file_num = ds_obj.file_num_offset

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
xmin_m = np.min(ds_obj.xpos[:plot_limit+1, plot_indices])
xmax_m = np.max(ds_obj.xpos[:plot_limit+1, plot_indices])
ymin_m = np.min(ds_obj.ypos[:plot_limit+1, plot_indices])
ymax_m = np.max(ds_obj.ypos[:plot_limit+1, plot_indices])
zmin_m = np.min(ds_obj.zpos[:plot_limit+1, plot_indices])
zmax_m = np.max(ds_obj.zpos[:plot_limit+1, plot_indices])

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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#                                                                    #
#   Plot Budget Components                                           #
#                                                                    #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#for plot_index in plot_indices:
#    for budget_coord_type, budget_var_list in budget_var_names.items():
for plot_index, (budget_coord_type, budget_var_list) in itertools.product(plot_indices, budget_var_names.items()):

    ds_var = budget_coord_type[0] + 'vort'
    vort_var = np.copy(ds.variables[ds_var][:,zmin:zmax,ymin:ymax,xmin:xmax])

    # Initialization (earliest time) trajectory positions.
    traj_init_xpos = ds_obj.xpos[0, plot_index]
    traj_init_ypos = ds_obj.ypos[0, plot_index]
    traj_init_zpos = ds_obj.zpos[0, plot_index]

    # Title string for whether this is the model-based budget calculation or
    #   the direct equation calculation.
    equation_string = budget_coord_type.split('_')[-1].title()
    if equation_string == 'Budget':
        context_string = ' from CM1 Output'
    else:
        context_string = ', Directly Calculated'
    # Dimension of the data to put in the title.
    direction = budget_coord_type.split('_')[0]
    dir_string = title_dir_sub(direction)

    # Title string for trajectory that is plotted and its starting positions.
    title_substring = '\nTrajectory {:d}, Initialized (z,y,x) (m): {:.1f}, {:.1f}, {:.1f}'.format(plot_index, traj_init_zpos, traj_init_ypos, traj_init_xpos)

    # Initialize the plot.
    fig2 = plt.figure(figsize=(13,7))
    ax = fig2.add_subplot(111)

    # Starting (earliest time) trajectory positions.
    start_vort_xpos = ds_obj.xpos[0, plot_index]
    start_vort_ypos = ds_obj.ypos[0, plot_index]
    start_vort_zpos = ds_obj.zpos[0, plot_index]

    # Get "correct" vorticity (CM1 vorticity interpolated to trajectory
    #   positions) at each time step.
    interp_vort = np.zeros((ds_obj.parcel_time_step_num))
    for i in range(plot_limit+1):
        interp_xpos = ds_obj.xpos[i, plot_index]
        interp_ypos = ds_obj.ypos[i, plot_index]
        interp_zpos = ds_obj.zpos[i, plot_index]
        interp_vort[i] = interpolate_vort(grid_coord, interp_xpos, interp_ypos, interp_zpos, vort_var[i])

    budget_vars_sum = np.zeros((ds_obj.parcel_time_step_num))
    for budget_var_name in budget_var_list:
        # For the turbulence and diffusion variables, add them together since
        #   they are small and the difference between the horizontal and
        #   vertical components is not important.
        if budget_var_name.endswith('turb') or budget_var_name.endswith('edif'):
            budget_var = ds_obj.getCombinedBudgetData(budget_var_name)[:,plot_index]
        # Other tendencies are large enough to be treated separately.
        else:
            budget_var = ds_obj.getBudgetData(budget_var_name)[:,plot_index]
        # Sum of the vorticity tendencies.
        budget_vars_sum += budget_var

        # Get integrated vorticity terms from vorticity tendency terms.
        budget_comp = np.zeros((ds_obj.parcel_time_step_num))
        # First value is the total vorticity component, as values of individual
        #   terms are not available.
        budget_comp[0] = interpolate_vort(grid_coord, start_vort_xpos, start_vort_ypos, start_vort_zpos, vort_var[0])
        for i in range(1, plot_limit+1):
            budget_comp[i] = budget_comp[i-1] + budget_var[i] * time_step_lengths[i-1]

        # Plot of individual vorticity components.
        plt.plot(ds_obj.simulation_times[:plot_limit+1], budget_comp[:plot_limit+1], label=budget_legendlabels(budget_var_name), color=budget_linecolors(budget_var_name), linewidth=2)

    # Calculate the "prognostic" vorticity.
    prog_vort = np.zeros((ds_obj.parcel_time_step_num))
    prog_vort[0] = interpolate_vort(grid_coord, start_vort_xpos, start_vort_ypos, start_vort_zpos, vort_var[0])
    for i in range(1,plot_limit+1):
        prog_vort[i] = prog_vort[i-1] + budget_vars_sum[i] * time_step_lengths[i-1]

    # Plot of "prognostic" vorticity.
    plt.plot(ds_obj.simulation_times[:plot_limit+1], prog_vort[:plot_limit+1], label='Total Prog Vort.', color='black', linestyle='dashed', linewidth=2)

    # Plot of "correct" vorticity (CM1 vorticity interpolated to trajectory
    #   positions) at each time step.
    plt.plot(ds_obj.simulation_times[:plot_limit+1], interp_vort[:plot_limit+1], label='Total Correct Vort.', color='black', linewidth=2)

    # Reference line at initial vorticity value.
    plt.plot(ds_obj.simulation_times, np.repeat(interp_vort[0], repeats=ds_obj.parcel_time_step_num), color='black', label='Init. Vort. Value')

    plt.title('{:s} Vorticity{:s}{:s}'.format(dir_string, context_string, title_substring))
    plt.xlim(initialize_time, ds_obj.simulation_times[plot_limit])
    plt.xlabel('Simulation Time (seconds)')
    plt.ylabel(r'Vorticity (s$\mathregular{^{-1}}$)')
    plt.legend(loc='best')

    image_file_name = output_dir + 'cm1_forwardtraj_vort_components_{:s}_{:s}_inittime{:d}_p{:d}.png'.format(parcel_label, budget_coord_type, initialize_time, plot_index)
    #plt.savefig(image_file_name, dpi=400)

    plt.show()

