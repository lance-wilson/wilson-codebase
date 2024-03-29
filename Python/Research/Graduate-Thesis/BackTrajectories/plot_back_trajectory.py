#!/usr/bin/env python3
#
# Name:
#   plot_back_trajectory.py
#
# Purpose:  Plot CM1 backward trajectories along with data slices to visualize
#           where the trajectories go.
#
# Syntax: python3 plot_back_trajectory.py version_number parcel_label variable [x_val] [y_val] [z_val]
#
#   Input:
#
# Execution Example:
#   python3 plot_back_trajectory.py v5 v5_meso_tornadogenesis dbz z=750
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
#                               calc_back_trajectory_meters
#   2021/09/17 - Lance Wilson:  Simplified for loop in plotting section (split
#                               from plot_back_traj_elev_color_1Darray.py).
#   2021/11/12 - Lance Wilson:  Added comments and improvements to calculations
#                               of intialization positions that are going to be
#                               plotted and plot frequency.
#   2021/12/22 - Lance Wilson:  Fixed so that plot_limit_minutes greater than
#                               the available amount of data does not cause
#                               duplication of plots at earliest times.
#

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, Normalize
from netCDF4 import Dataset
from netCDF4 import MFDataset
from parameter_list import parameters

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
    variable = sys.argv[3]
else:
    print('Variable to plot slice, parcel label, and version number must be specified.')
    print('Syntax: python3 plot_back_trajectory.py version_number parcel_label variable [x_val] [y_val] [z_val]')
    print('Example: python3 plot_back_trajectory.py v5 v5_meso_tornadogenesis dbz z=750')
    print('Currently supported version numbers: v3, 10s, v4, v5')
    sys.exit()

# Command-line arguments for plotting limited sets of trajectories.
x_flag = False
y_flag = False
z_flag = False
if len(sys.argv) > mandatory_arg_num + 1:
    for coord in sys.argv[mandatory_arg_num+1:]:
        if coord.startswith('x='):
            x_plot_val = float(coord.split('=')[-1])
            x_flag = True
        if coord.startswith('y='):
            y_plot_val = float(coord.split('=')[-1])
            y_flag = True
        if coord.startswith('z='):
            z_plot_val = float(coord.split('=')[-1])
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
# Directory where back trajectory data is stored.
archive_dir = 'back_traj_npz_{:s}/'.format(version_number)
# Directory for output images.
output_dir = 'BackTrajectoryImages/'

# How far back (in minutes) to plot trajectories.
plot_limit_minutes = 10.#20.

# How frequency to show output plots (every N minutes).
plot_freq_minutes = 3.#1.

# Minimum and maximum indices in each dimension.
# Full storm scale
xmin = 160
xmax = 610
xmax = 810
ymin = 170
ymax = 620
zmin = 0
zmax = 80

# Axis intervals based in kilometers (X,Y) meters (Z) (tick marks every N
#   meters).
xval_interval = 4.#8000.
yval_interval = 4.#4000.
zval_interval = 60.

# Model height level below which trajectory data is no longer safe to use
#   (generally the height of the lowest non-boundary w point).
min_usable_z_height = 30.

# Number of color graduations to be collected from the colormap.
colorbar_color_num = 256

# Initial colormap that may be manipulated later.
initial_colormap = cm.get_cmap('gist_rainbow', colorbar_color_num)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get parameters for the background field variable from parameter_list.py
#   Available parameters (2021/11/09):
#           'val_interval'          'datamin'           'datamax'
#           'offset'                'bar_label'         'colormap'
#           'contour_interval' 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parameters = parameters(variable)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load back trajectory data from an uncompressed numpy archive.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
traj_data = np.load(archive_dir + 'backtraj_{:s}.npz'.format(parcel_label))
# Position data for the back trajectories.
xpos = traj_data['xpos']/1000.
ypos = traj_data['ypos']/1000.
zpos = traj_data['zpos']
parcel_dimensions = traj_data['parcel_dimension']
# Total number of parcels for this set of data.
total_parcel_num = np.prod(parcel_dimensions)

# Model file at the earliest time of the trajectory dataset (zero-indexed, add
#   one to get the correct CM1 model file). Examples:
#   Trajectories back from SVC 60 time steps (from 257, file_num_offset = 197).
#   Trajectories back from downdraft 60 time steps (from 221, file_num_offset = 161).
# Adding 0 to the file value to make sure that the output is an integer.
file_num_offset = traj_data['offset'] + 0

# Number of back trajectory parcel output times.
parcel_time_step_num = len(xpos)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset over the time period where back trajectories are calculated.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset+1, file_num_offset+parcel_time_step_num+1)]
ds = MFDataset(file_list)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Dimensions and boundaries of the plot.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# If the background variable is a staggered wind variable, use distances on the
#   staggered grid.  Otherwise, use the unstaggered grid points.
x_dim_param = 'xf' if variable == 'u' else 'xh'
y_dim_param = 'yf' if variable == 'v' else 'yh'
z_dim_param = 'zf' if variable == 'w' else 'z'

# Minimum and maximum values in each dimension (based on the input indices)
#   (not converted to meters).
xval_min = ds.variables[x_dim_param][xmin]#*1000.
xval_max = ds.variables[x_dim_param][xmax]#*1000.
yval_min = ds.variables[y_dim_param][ymin]#*1000.
yval_max = ds.variables[y_dim_param][ymax]#*1000.
zval_min = ds.variables[z_dim_param][zmin]#*1000.
zval_max = ds.variables[z_dim_param][zmax]#*1000.

# Locations of axis tick marks (in kilometers).
xticks = np.arange(np.round(xval_min),np.round(xval_max),xval_interval)
yticks = np.arange(np.round(yval_min),np.round(yval_max),yval_interval)
zticks = np.arange(zval_min,zval_max,zval_interval)

# Range of data points on which to plot the background data.
#x_vals = np.linspace(xval_min, xval_max,xmax-xmin)
#y_vals = np.linspace(yval_min, yval_max,ymax-ymin)
x_vals = np.copy(ds.variables[x_dim_param])
y_vals = np.copy(ds.variables[y_dim_param])

# Initialization Position time for parcels.
initialize_time = int(ds.variables['time'][parcel_time_step_num-1])

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
plot_indices_part = {}
# For each set of coordinates, the valid plot indices for that dimension are
#   the indices where that position array is equal to the command-line
#   argument if one was supplied.  If no argument was supplied, then all
#   indices may be used.
if x_flag == True:
    plot_indices_part['x'] = np.where(xpos[0] == x_plot_val)[0]
else:
    plot_indices_part['x'] = range(total_parcel_num)

if y_flag == True:
    plot_indices_part['y'] = np.where(ypos[0] == y_plot_val)[0]
else:
    plot_indices_part['y'] = range(total_parcel_num)

if z_flag == True:
    plot_indices_part['z'] = np.where(zpos[0] == z_plot_val)[0]
else:
    plot_indices_part['z'] = range(total_parcel_num)

# Get indices that are to be plotted from the intersection of the x and y
#   parts, and then the intersection of that and the z part.
part1 = np.intersect1d(plot_indices_part['x'], plot_indices_part['y'])
plot_indices = np.intersect1d(part1, plot_indices_part['z'])

if len(plot_indices) > 0:
    # Minimum and maximum values for each position initialization.
    xpos_min = int(np.min(xpos[0,plot_indices])*1000.)
    ypos_min = int(np.min(ypos[0,plot_indices])*1000.)
    zpos_min = int(np.min(zpos[0,plot_indices]))
    xpos_max = int(np.max(xpos[0,plot_indices])*1000.)
    ypos_max = int(np.max(ypos[0,plot_indices])*1000.)
    zpos_max = int(np.max(zpos[0,plot_indices]))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate how many time steps of trajectory data to plot (based on
#   user-defined number of minutes to be plotted).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = 60. * plot_limit_minutes

data_timespan = ds.variables['time'][-1] - ds.variables['time'][0]

# Ensure that the data does not repeat plots if the plot limit is greater than
#   the available amount of data by limiting it to the total timespan of data.
if plot_limit_seconds > data_timespan:
    plot_limit_seconds = np.round(data_timespan)

# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds.variables['time'][1:] - ds.variables['time'][:-1])
# Cumulative sum array of the inverse of the time step lengths, as we need to
#   know how many indices to count backward.
cumulative_time_steps = np.cumsum(time_step_lengths[::-1])

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
#   Array is inverted so that the file numbers are added to the list in the correct order.
plot_freq_times = np.arange(0, plot_limit_seconds, plot_freq_seconds)[1:][::-1]

# Empty list to store the model file numbers that are to be plotted.
plot_file_nums = []

# Convert each plot frequency time (in seconds) to the nearest file number.
for plot_time in plot_freq_times:
    diff = np.abs(cumulative_time_steps - plot_time)
    # Number of file numbers back from the initialization time.
    #   Index n in inverted array is equivalent to -(n+1) index in regular
    #   array, so adding one to this value.
    file_num_back = np.argwhere(diff == np.min(diff))[0,0] + 1
    # Subtract the above number of time steps from the total number of parcel
    #   time steps to get the actual file number from the CM1 data subset.
    # Also subtracting 1 from the total number of parcels, so that the index
    #   retrieved from the file is the expected number of time steps back.
    subset_file_num = (parcel_time_step_num - 1) - file_num_back
    plot_file_nums.append(subset_file_num)

# Make sure the earliest time is plotted.
first_time_step = parcel_time_step_num - plot_limit + 1
if not first_time_step in plot_file_nums:
    plot_file_nums = [first_time_step] + plot_file_nums

# Make sure the last (initialization) time is plotted.
if not (parcel_time_step_num - 1) in plot_file_nums:
    plot_file_nums.append(parcel_time_step_num - 1)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create a new colormap that has the lowest 30 meters colored black
# Based on "Creating listed colormaps" section of
# https://matplotlib.org/stable/tutorials/colors/colormap-manipulation.html
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
newcolors = initial_colormap(np.linspace(0, 1, colorbar_color_num))
black = np.array([0, 0, 0, 1])
nearest_index = int(np.round(colorbar_color_num * min_usable_z_height/(np.nanmax(zpos)-np.nanmin(zpos))))
newcolors[:nearest_index, :] = black
newcmp = ListedColormap(newcolors)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
#                                                                    #
#   Plot Trajectories                                                #
#                                                                    #
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
# Make plots at the desired times. 
for cur_file_num in plot_file_nums:
    # Inverted time index of the back trajectory data (which runs backwards in time).
    i = parcel_time_step_num - cur_file_num

    # Initialize the plot.
    fig2 = plt.figure(figsize=(14,7))
    ax = fig2.add_subplot(111)

    # Background field variable data for the filled contour plot.
    #data_array = np.copy(ds.variables[variable][cur_file_num, parameters['offset'], ymin:ymax, xmin:xmax])
    data_array = np.copy(ds.variables[variable][cur_file_num, parameters['offset'], :, :])

    z_vals = data_array

    # Make a filled contour plot of the background field variable.
    ref = ax.contourf(x_vals, y_vals, z_vals, np.linspace(parameters['datamin'], parameters['datamax'], parameters['contour_interval']), offset=parameters['offset'], zdir='z', cmap=parameters['colormap'])

    # Model file number of the whole CM1 model run (as opposed to the
    #   subset taken for plotting).
    model_file_num = file_num_offset + cur_file_num + 1
    # The simulation time (in seconds) of this model time step.
    real_file_time = int(ds.variables['time'][cur_file_num])

    if len(plot_indices) > 0:
        # Scatter plot of the initial positions of the back trajectories.
        ax.scatter(xpos[0], ypos[0])
        for j in plot_indices:
            # Take subsets of x, y, and z trajectory positions from the
            #   earliest time to the time currently being plotted.
            xpos_subset = xpos[i-1:plot_limit,j]
            ypos_subset = ypos[i-1:plot_limit,j]
            zpos_subset = zpos[i-1:plot_limit,j]

            points = np.array([xpos_subset, ypos_subset]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            #norm = plt.Normalize(np.nanmin(zpos), np.nanmax(zpos))
            norm = plt.Normalize(np.nanmin(zpos), 1000.)
            #lc = LineCollection(segments, cmap='gist_rainbow', norm=norm)
            lc = LineCollection(segments, cmap=newcmp, norm=norm)
            lc.set_array(zpos_subset)
            lc.set_linewidth(2)
            line = ax.add_collection(lc)
        # Colorbar for the trajectory height.
        bar2 = fig2.colorbar(line, ax=ax)
        bar2.set_label('Height (m)', fontsize = 16)

        plt.title('Simulation Time {:d} s (Model File {:d})\n{:s} at Height {:d} m, Backward Trajectories Initialized at {:d} s\nStarting Positions (m): X ({:d} to {:d}), Y ({:d} to {:d}), Z ({:d} to {:d})\nParcels Plotted/Total Parcel Number: {:d}/{:d}'.format(real_file_time, model_file_num, variable_long_name, contour_height, initialize_time, xpos_min, xpos_max, ypos_min, ypos_max, zpos_min, zpos_max, len(plot_indices), total_parcel_num))
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
    #image_file_name = output_dir + 'cm1_backtraj_{:s}_{:s}_nc{:d}_time{:d}.png'.format(parcel_label, variable, model_file_num, real_file_time)
    #plt.savefig(image_file_name, dpi=400)

plt.show()

if not sys.flags.interactive:
    ds.close()

