#!/usr/bin/env python3
#
# Name:
#   plot_back_traj_vort_component.py
#
# Purpose:  Plot CM1 backward trajectories visualizing vorticity budget data
#           along the trajectories.
#
# Syntax: python3 plot_back_traj_vort_component.py version_number parcel_label
#
# Input:  netCDF file containing vorticity budget data interpolated to back
#           trajectory posititions
#         netCDF file containing intialization positions of back trajectories
#           determined to be located in a certain region of the storm
#
# Execution Example:
#   python3 plot_back_traj_vort_component.py v5 downdraft
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
#

from back_traj_interp_class import Back_traj_ds
from categorize_traj_class import Cat_traj
from parameter_list import budget_legendlabels, title_dir_sub

from netCDF4 import Dataset
import itertools
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import sys

mandatory_arg_num = 3

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    parcel_category = sys.argv[3]
else:
    print('Parcel label and version number must be specified.')
    print('Syntax: python3 plot_back_traj_vort_component.py version_number parcel_label')
    print('Example: python3 plot_back_traj_vort_component.py v5 downdraft')
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
# Directory where back trajectory analysis data is stored
analysis_dir = model_dir + 'back_traj_analysis/'
# Directory with netCDF files of vorticity budget data interpolated to trajectory locations.
interp_dir = analysis_dir + 'parcel_interpolation/'
# Directory with netCDF files containing parcel initialization positions
#   belong to a particular region of the storm.
cat_dir = analysis_dir + 'categorized_trajectories/'
# Directory for output images.
output_dir = analysis_dir + 'BackTrajectoryImages/'

# How far back (in minutes) to plot trajectories.
plot_limit_minutes = 10.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open object using netCDF files containing vorticity budget data interpolated
#   to back trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ds_obj = Back_traj_ds(version_number, interp_dir, parcel_label)

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
    if 'advection' in key or 'adv' in key:
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
    # Initialization positions are converted to an array index.
    plot_indices = cat_traj_obj.meters_to_trajnum(ds_obj.xpos, ds_obj.ypos, ds_obj.zpos)
else:
    print 'Categorized trajectory file does not contain any data'
    sys.exit()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate how many time steps of trajectory data to plot (based on
#   user-defined number of minutes to be plotted).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = 60. * plot_limit_minutes

# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds_obj.simulation_times[:-1] - ds_obj.simulation_times[1:])

# Cumulative sum array of the time step lengths, which are already oriented
#   backward in time, and thus can tell how many indices to count backward
#   directly.
cumulative_time_steps = np.cumsum(time_step_lengths)

# Check that at least one time step is going to be plotted (i.e.
#   plot_limit_seconds must be no smaller than the smallest time_step),
#   otherwise np.argwhere result will be empty and crash the program.
if plot_limit_seconds < time_step_lengths[-1]:
    print('Length of time desired to plot is less than the time step, ' + 
          'so there is no trajectory data to plot.')
    sys.exit()

# How far back (in time steps) to plot trajectories.
#   The final row of the np.argwhere output contains the index of the last
#   appropriate time, so the limit for the plotting loop is one more than that.
plot_limit = np.argwhere(cumulative_time_steps <= plot_limit_seconds)[-1,0] + 1

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#                                                                    #
#   Plot Budget Components                                           #
#                                                                    #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#for plot_index in plot_indices:
#    for budget_coord_type, budget_var_list in budget_var_names.items():
for plot_index, (budget_coord_type, budget_var_list) in itertools.product(plot_indices, budget_var_names.items()):

    # Initialization (latest time) trajectory positions.
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
    title_substring = '\nTrajectory {:d}, Initialized (z,y,x): {:.1f}, {:.1f}, {:.1f}'.format(plot_index, traj_init_zpos, traj_init_ypos, traj_init_xpos)

    # Initialize the plot.
    fig2 = plt.figure(figsize=(13,7))
    ax = fig2.add_subplot(111)

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

        # Plot of individual vorticity tendencies.
        plt.plot(ds_obj.simulation_times[:plot_limit][::-1], budget_var[:plot_limit][::-1], label=budget_legendlabels(budget_var_name))

    # Plot of sum of the vorticity tendencies.
    plt.plot(ds_obj.simulation_times[:plot_limit][::-1], budget_vars_sum[:plot_limit][::-1], label='Total Vort.', color='black')

    # Reference line at 0.
    plt.plot(ds_obj.simulation_times[:plot_limit][::-1], np.zeros(ds_obj.simulation_times[:plot_limit].shape), color='black')

    plt.title('{:s} Vorticity {:s} Components{:s}{:s}'.format(dir_string, equation_string, context_string, title_substring))
    plt.xlim(ds_obj.simulation_times[plot_limit-1], initialize_time)
    plt.xlabel('Simulation Time (seconds)')
    plt.ylabel(r'Vorticity Tendency (s$\mathregular{^{-2}}$)')
    plt.legend(loc='upper left')

    #image_file_name = output_dir + 'cm1_backtraj_vortbudget_components_{:s}_{:s}_inittime{:d}_p{:d}.png'.format(parcel_label, budget_coord_type, initialize_time, plot_index)
    #plt.savefig(image_file_name, dpi=400)

    plt.show()

