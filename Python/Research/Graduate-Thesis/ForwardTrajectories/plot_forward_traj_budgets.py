#!/usr/bin/env python3
#
# Name:
#   plot_back_traj_budgets.py
#
# Purpose:  Plot CM1 forward trajectories visualizing vorticity budget data
#           along the trajectories.
#
# Syntax: python3 plot_forward_traj_budgets.py version_number parcel_label field_variable budget_variable [x=x_min,xmax] [y=y_min,y_max] [z=z_min,z_max]
#
#   Input: CM1 netCDF model files
#          netCDF file containing vorticity budgets interpolated to forward
#               trajectory positions accessed via Forward_traj_ds in
#               forward_traj_interp_class.py
#
# Execution Example:
#   python3 plot_forward_traj_budgets.py v5 1000parcel_tornadogenesis dbz x_stretch_term z=750,1000
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
#   2021/12/22 - Lance Wilson:  Fixed so that plot_limit_minutes greater than
#                               the available amount of data does not cause
#                               duplication of plots at earliest times.
#   2021/04/08 - Lance Wilson:  Split from plot_back_traj_budgets to plot
#                               forward trajectory data.
#

from forward_traj_interp_class import Forward_traj_ds
from parameter_list import parameters, budget_barlabels

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, Normalize
from netCDF4 import Dataset
from netCDF4 import MFDataset

import atexit
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

# Close the main CM1 model data netCDF file.
def closeNCfile(ds):
    ds.close()

mandatory_arg_num = 4

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    variable = sys.argv[3]
    budget_var_arg = sys.argv[4]
else:
    print('Variable to plot slice, parcel label, and version number must be specified.')
    print('Syntax: python3 plot_back_traj_budgets.py version_number parcel_label field_variable budget_variable [x=x_min,xmax] [y=y_min,y_max] [z=z_min,z_max]')
    print('Example: python3 plot_forward_traj_budgets.py v5 1000parcel_tornadogenesis dbz x_stretch_term z=750,1000')
    print('Currently supported version numbers: v4, v5')
    print('Set budget_variable to \'all\' to plot all variables.')
    sys.exit()

if version_number == '3' or version_number =='10s':
    print('Version number is not valid.')
    print('Currently supported version numbers: 4, 5')
    sys.exit()

# Command-line arguments for plotting limited sets of trajectories.
x_flag = False
y_flag = False
z_flag = False
if len(sys.argv) > mandatory_arg_num + 1:
    for coord in sys.argv[mandatory_arg_num+1:]:
        if coord.startswith('x='):
            x_plot_vals = coord.split('=')[-1].split(',')
            x_plot_min = float(x_plot_vals[0])
            x_plot_max = float(x_plot_vals[1])
            x_flag = True
        if coord.startswith('y='):
            y_plot_vals = coord.split('=')[-1].split(',')
            y_plot_min = float(y_plot_vals[0])
            y_plot_max = float(y_plot_vals[1])
            y_flag = True
        if coord.startswith('z='):
            z_plot_vals = coord.split('=')[-1].split(',')
            z_plot_min = float(z_plot_vals[0])
            z_plot_max = float(z_plot_vals[1])
            z_flag = True

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
analysis_dir = model_dir + 'forward_traj_analysis/'
# Directory with netCDF files of vorticity budget data interpolated to trajectory locations.
interp_dir = analysis_dir + 'parcel_interpolation/'
# Directory for output images.
output_dir = analysis_dir + 'ForwardTrajectoryImages/'

# How frequency to show output plots (every N minutes).
plot_freq_minutes = 3.

# Minimum and maximum indices in each dimension.
# Full storm scale
xmin = 160
xmax = 810
ymin = 170
ymax = 620
zmin = 0
zmax = 80

# Axis intervals for plot based in meters (tick marks every N meters).
xval_interval = 4.
yval_interval = 4.
zval_interval = 6.

# Limits of percentile to take of vorticity budget data to determine more
#   reasonable limits for the colorbar.
percentile_min = 3
percentile_max = 97

# Number of color graduations to be collected from the colormap.
colorbar_color_num = 256

# Initial colormap that may be manipulated later.
initial_colormap = cm.get_cmap('RdBu_r', colorbar_color_num)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get parameters for the background field variable from parameter_list.py
#   Available parameters (2021/11/09):
#           'val_interval'          'datamin'           'datamax'
#           'offset'                'bar_label'         'colormap'
#           'contour_interval' 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parameters = parameters(variable)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create object that opens netCDF files containing vorticity budget data
#   interpolated to forward trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
traj_ds_obj = Forward_traj_ds(version_number, interp_dir, parcel_label)
traj_ds_obj.read_data()

# Position data for the forward trajectories.
# Converting x and y locations to kilometers for plotting.
xpos = traj_ds_obj.xpos/1000.
ypos = traj_ds_obj.ypos/1000.
# Leaving z location in meters (for colorbar scale).
zpos = traj_ds_obj.zpos

# Total number of parcels for this set of data.
total_parcel_num = traj_ds_obj.total_parcel_num

# Model file at the earliest time of the trajectory dataset.
file_num_offset = traj_ds_obj.file_num_offset

# Get the number of time steps in the full set of parcel data.
parcel_time_step_num = traj_ds_obj.parcel_time_step_num

# List of vorticity budget variables, which are all variables in the file
#   except those containing position data (which end in 'pos') and those
#   that have only one dimension (which should just be file_num_offset).
budget_var_keys = traj_ds_obj.budget_var_keys

# Create a list of vorticity budget variables that are to be plotted.
if budget_var_arg == 'all':
    # If plotting all budget variables, use the full list of budget variables.
    budget_var_names = budget_var_keys
else:
    # If there is just one variable being plotted (and it is in the list
    #   of variables in the interpolated budget dataset), will make it a
    #   one-item list so that it can still work with the plotting loop.
    if budget_var_arg in budget_var_keys:
        budget_var_names = [budget_var_arg]
    else:
        print('Invalid budget variable name.')
        sys.exit()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset over the time period where back trajectories are calculated.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset, file_num_offset+parcel_time_step_num)]
ds = MFDataset(file_list)

# Close the main CM1 data netCDF file when the program exits.
atexit.register(closeNCfile, ds)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Dimensions and boundaries of the plot.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# If the background variable is a staggered wind variable, use distances on the
#   staggered grid.  Otherwise, use the unstaggered grid points.
x_dim_param = 'xf' if variable == 'u' else 'xh'
y_dim_param = 'yf' if variable == 'v' else 'yh'
z_dim_param = 'zf' if variable == 'w' else 'z'

# Range of data points on which to plot the background data.
x_vals = np.copy(ds.variables[x_dim_param])
y_vals = np.copy(ds.variables[y_dim_param])

# Minimum and maximum values in each dimension (based on the input indices)
#   (in kilometers).
xval_min = x_vals[xmin]
xval_max = x_vals[xmax]
yval_min = y_vals[ymin]
yval_max = y_vals[ymax]
zval_min = ds.variables[z_dim_param][zmin]
zval_max = ds.variables[z_dim_param][zmax]

# Location of axis tick marks (in kilometers)
xticks = np.arange(np.round(xval_min),np.round(xval_max),xval_interval)
yticks = np.arange(np.round(yval_min),np.round(yval_max),yval_interval)

# Initialization Position time for parcels.
initialize_time = int(ds.variables['time'][0])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Variables to put in plot title
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Height of the background field variable, converted to meters.
contour_height = int(ds.variables[z_dim_param][parameters['offset']] * 1000.)

variable_long_name = getattr(ds.variables[variable], 'def').title()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Determination of which trajectories are to be plotted (based on
#   initialization points).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# For each set of coordinates, the valid plot indices for that dimension are
#   the indices where that position array is equal to the command-line
#   argument if one was supplied.  If no argument was supplied, then all
#   indices may be used.
if x_flag == True:
    part1 = np.where(xpos[0] >= x_plot_min)[0]
    part2 = np.where(xpos[0] <= x_plot_max)[0]
    plot_indices_part_x = np.intersect1d(part1, part2)
else:
    plot_indices_part_x = range(total_parcel_num)

if y_flag == True:
    part1 = np.where(ypos[0] >= y_plot_min)[0]
    part2 = np.where(ypos[0] <= y_plot_max)[0]
    plot_indices_part_y = np.intersect1d(part1, part2)
else:
    plot_indices_part_y = range(total_parcel_num)

if z_flag == True:
    part1 = np.where(zpos[0] >= z_plot_min)[0]
    part2 = np.where(zpos[0] <= z_plot_max)[0]
    plot_indices_part_z = np.intersect1d(part1, part2)
else:
    plot_indices_part_z = range(total_parcel_num)

# Get indices that are to be plotted from the intersection of the x and y
#   parts, and then the intersection of that and the z part.
part1 = np.intersect1d(plot_indices_part_x, plot_indices_part_y)
plot_indices = np.intersect1d(part1, plot_indices_part_z)

if len(plot_indices) > 0:
    # Minimum and maximum values for each position at initialization.
    xpos_min = int(np.min(xpos[0,plot_indices])*1000)
    ypos_min = int(np.min(ypos[0,plot_indices])*1000)
    zpos_min = int(np.min(zpos[0,plot_indices]))
    xpos_max = int(np.max(xpos[0,plot_indices])*1000)
    ypos_max = int(np.max(ypos[0,plot_indices])*1000)
    zpos_max = int(np.max(zpos[0,plot_indices]))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate how many time steps of trajectory data to plot (based on
#   user-defined number of minutes to be plotted).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = np.round(traj_ds_obj.simulation_times[-1] - traj_ds_obj.simulation_times[0])

# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds.variables['time'][1:] - ds.variables['time'][:-1])
# Cumulative sum array of the time step lengths.
cumulative_time_steps = np.cumsum(time_step_lengths)

data_timespan = ds.variables['time'][-1] - ds.variables['time'][0]

# Ensure that the data does not repeat plots if the plot limit is greater than
#   the available amount of data by limiting it to the total timespan of data.
if plot_limit_seconds > data_timespan:
    plot_limit_seconds = np.round(data_timespan)

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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the indices of the CM1 data subset that are to be plotted, based
#   on a user-defined frequency (in minutes) to plot images.
#   The earliest time with visible trajectory paths and the initialization time
#   are also added to the list to be plotted.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_freq_minutes to seconds.
plot_freq_seconds = 60. * plot_freq_minutes

# Initial list of times that should be plotted at this plotting frequency
#   (time 0 being removed).
plot_freq_times = np.arange(0, plot_limit_seconds+1, plot_freq_seconds)[1:]

# Empty list to store the model file numbers that are to be plotted.
plot_file_nums = []

# Convert each plot frequency time (in seconds) to the nearest file number.
for plot_time in plot_freq_times:
    diff = np.abs(cumulative_time_steps - plot_time)
    # Number of file numbers forward from the initialization time.
    file_num_forward = np.argwhere(diff == np.min(diff))[0,0]

    plot_file_nums.append(file_num_forward)

# Make sure the earliest time is plotted.
first_time_step = 0
if not first_time_step in plot_file_nums:
    plot_file_nums = [first_time_step] + plot_file_nums

# Make sure the last (termination) time is plotted.
if not (parcel_time_step_num - 1) in plot_file_nums:
    plot_file_nums.append(parcel_time_step_num - 1)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#                                                                    #
#   Plot Trajectories                                                #
#                                                                    #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#

# Data for the background variable (e.g. DBZ).
#   Data is accessed all at once outside the loop to ensure more consistent
#   time-performance.
data_array = np.copy(ds.variables[variable][:, parameters['offset'], :, :])

for budget_var_name in budget_var_names:
    # Timer
    start = time.time()

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Get data for this vorticity budget variable.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if len(plot_indices) > 0:
        # Get Data for this vorticity budget variable and create a label for the colorbar.
        budget_var = traj_ds_obj.getBudgetData(budget_var_name)

        # Get percentile-based limits for the colorbar, so that the range is more
        #   reasonable and not dictated by outliers.
        color_range_min = np.nanpercentile(budget_var, percentile_min)
        color_range_max = np.nanpercentile(budget_var, percentile_max)

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # Make adjustments to the diverging colormap so that the zero/neutral
        #   point does not have to be centered, and can be based on the data
        #   being plotted. 
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If the data range is not on either side of zero, there is no point
        #   in adjusting the neutral point of the (diverging) colormap.
        if color_range_max <= 0. or color_range_min >= 0.:
            newcolors = initial_colormap(np.linspace(0,1,colorbar_color_num))
        else:
            outer_bound = np.max((np.abs(color_range_min), color_range_max))
            inner_bound = np.min((np.abs(color_range_min), color_range_max))

            # Calculate the proportion of data that should be cut off for the
            #   neutral point to match the zero point in the data.
            color_drop_boundary = (outer_bound - inner_bound)/(2. * outer_bound)

            # If the magnitude of the positive end of the colorbar range is
            #   larger than the magnitude of the negative end, remove the
            #   negative portion of the colormap.
            if color_range_max > np.abs(color_range_min):
                newcolors = initial_colormap(np.linspace(color_drop_boundary, 1, colorbar_color_num))
            # Otherwise, remove the positive portion of the colormap.
            else:
                newcolors = initial_colormap(np.linspace(0, 1-color_drop_boundary, colorbar_color_num))

        # Create a new colormap based on the adjusted colors.
        newcmp = ListedColormap(newcolors)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Create the plots.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Make plots at the desired times. 
    for cur_file_num in plot_file_nums:
        # Initialize the plot.
        fig2 = plt.figure(figsize=(13,7))
        ax = fig2.add_subplot(111)

        # Background field variable data for the filled contour plot.
        z_vals = data_array[cur_file_num]

        # Make a filled contour plot of the background field variable.
        ref = ax.contourf(x_vals, y_vals, z_vals, np.linspace(parameters['datamin'], parameters['datamax'], parameters['contour_interval']), offset=parameters['offset'], zdir='z', cmap=parameters['colormap'])

        # Model file number of the whole CM1 model run (as opposed to the
        #   subset taken for plotting).
        model_file_num = file_num_offset + cur_file_num
        # The simulation time (in seconds) of this model time step.
        real_file_time = int(ds.variables['time'][cur_file_num])

        if len(plot_indices) > 0:
            # Scatter plot of the initial positions of the back trajectories.
            ax.scatter(xpos[0], ypos[0])
            for j in plot_indices:
                # Take subsets of x and y trajectory positions from the
                #   earliest time to the time currently being plotted.
                xpos_subset = xpos[0:cur_file_num,j]
                ypos_subset = ypos[0:cur_file_num,j]
                # Take a subset of this vorticity budget variable from the
                #   earliest time to the time currently being plotted.
                budget_var_subset = budget_var[0:cur_file_num,j]

                points = np.array([xpos_subset, ypos_subset]).T.reshape(-1, 1, 2)
                segments = np.concatenate([points[:-1], points[1:]], axis=1)
                norm = plt.Normalize(color_range_min, color_range_max)
                #lc = LineCollection(segments, cmap='gist_rainbow', norm=norm)
                lc = LineCollection(segments, cmap=newcmp, norm=norm)
                lc.set_array(budget_var_subset)
                lc.set_linewidth(2)
                line = ax.add_collection(lc)
            # Colorbar for the vorticity budget variable.
            bar2 = fig2.colorbar(line, ax=ax)
            bar2.set_label(budget_barlabels(budget_var_name), fontsize = 16)

            plt.title('Simulation Time {:d} s (Model File {:d})\n{:s} at Height {:d} m, Forward Trajectories Initialized at {:d} s\nStarting Positions (m): X ({:d} to {:d}), Y ({:d} to {:d}), Z ({:d} to {:d})\nParcels Plotted/Total Parcel Number: {:d}/{:d}'.format(real_file_time, model_file_num, variable_long_name, contour_height, initialize_time, xpos_min, xpos_max, ypos_min, ypos_max, zpos_min, zpos_max, len(plot_indices), total_parcel_num))
        else:
            plt.title('Simulation Time {:d} s (Model File {:d})\n{:s} at Height {:d} m'.format(real_file_time, model_file_num, variable_long_name, contour_height))

        ax.set_xticks(xticks)
        ax.set_yticks(yticks)
        ax.set_xlim(xval_min, xval_max)
        ax.set_ylim(yval_min, yval_max)
        ax.set_xlabel('E-W Distance from Center (km)', fontsize = 16)
        ax.set_ylabel('N-S Distance from Center (km)', fontsize = 16)

        # Colorbar ticks for the background field variable.
        cticks = np.arange(parameters['datamin'], parameters['datamax']+parameters['val_interval'], parameters['val_interval'])
        # Colorbar for the background field variable.
        bar = plt.colorbar(ref, ticks=cticks)
        bar.set_label(parameters['bar_label'], fontsize = 16)

        # Adjust plot so that a given distance is of equal length on both axes.
        plt.axes().set_aspect('equal', 'datalim')

        plt.tight_layout()

        # Code to save files
        image_file_name = output_dir + 'cm1_forwardtraj_vortbudget_{:s}_{:s}_{:s}_nc{:d}_time{:d}.png'.format(parcel_label, budget_var_name, variable, model_file_num, real_file_time)
        #plt.savefig(image_file_name, dpi=400)

    end = time.time()
    print('Finished plotting variable {:s} in {:.2f} seconds'.format(budget_var_name, end-start))

plt.show()

