#!/usr/bin/env python3
#
# Name:
#   categorize_trajectories.py
#
# Purpose:  Plot CM1 backward trajectories and determine which ones belong in 
#
# Syntax: python3 categorize_trajectories.py version_number parcel_label field_variable category [y=y_val1[,yval2]] [z=z_val1[,z_val2]]
#
#   Input:
#
# Execution Example:
#   python3 categorize_trajectories.py v5 v5_meso_tornadogenesis dbz forward_flank y=-9750 z=750,850
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
#

from back_traj_interp_class import Back_traj_ds
from back_trajectory_start_pos import get_start_pos
from categorize_traj_class import Cat_traj
from parameter_list import parameters, budget_barlabels

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, Normalize
from netCDF4 import Dataset
from netCDF4 import MFDataset

import atexit
import itertools
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

# Close the main CM1 model data netCDF file.
def closeNCfile(ds):
    ds.close()

# Function to run on the matplotlib button press event.
def onclick(event):
    global ix, iy
    ix = event.xdata

    global coords
    coords.append(ix)

    return

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Command-line arguments.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mandatory_arg_num = 4

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    variable = sys.argv[3]
    category = sys.argv[4]
else:
    print('Variable to plot slice, parcel label, and version number must be specified.')
    print('Syntax: python3 categorize_trajectories.py version_number parcel_label field_variable category [y=y_val1[,yval2]] [z=z_val1[,z_val2]]')
    print('Example: python3 categorize_trajectories.py v5 v5_meso_tornadogenesis dbz forward_flank y=-9750 z=750,850')
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
# Directory for output images.
output_dir = analysis_dir + 'categorized_trajectories/'

# How far back (in minutes) to plot trajectories.
plot_limit_minutes = 10.

# Minimum and maximum indices in each dimension.
xmin = 310
xmax = 610
ymin = 220
ymax = 470
zmin = 0
zmax = 80

# Axis intervals for plot based in meters (tick marks every N meters).
xval_interval = 8000.
yval_interval = 4000.
zval_interval = 60.

# Model height level below which trajectory data is no longer safe to use
#   (generally the height of the lowest non-boundary w point).
min_usable_z_height = 30.

# Limits of percentile to take of vorticity budget data to determine more
#   reasonable limits for the colorbar.
percentile_min = 3
percentile_max = 97

# Number of color graduations to be collected from the colormap.
colorbar_color_num = 256

# Initial colormap that may be manipulated later.
initial_colormap = cm.get_cmap('gist_rainbow', colorbar_color_num)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Determine which trajectories to plot.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
start_pos = get_start_pos(parcel_label)

# Command-line arguments for plotting limited sets of trajectories.
y_flag = False
z_flag = False
if len(sys.argv) > mandatory_arg_num + 1:
    for coord in sys.argv[mandatory_arg_num+1:]:
        # Get y-coordinates that are to be plotted (either a single value or a
        #   range of values). The starting (left-most) value must be a valid
        #   coordinate location. 
        if coord.startswith('y='):
            y_plot_vals = coord.split('=')[-1]
            y_split = y_plot_vals.split(',')
            y_points = [y for y in np.arange(float(y_split[0]), float(y_split[-1])+1., start_pos['y_increment'])]
            y_flag = True
        # Get z-coordinates that are to be plotted (either a single value or a
        #   range of values). The starting (left-most) value must be a valid
        #   coordinate location. 
        if coord.startswith('z='):
            z_plot_vals = coord.split('=')[-1]
            z_split = z_plot_vals.split(',')
            z_points = [z for z in np.arange(float(z_split[0]), float(z_split[-1])+1., start_pos['z_increment'])]
            z_flag = True

# Get all y points if a starting range was not entered.
if not y_flag:
    end_point = start_pos['y_start']+start_pos['y_increment']*start_pos['num_start_y']
    y_points = [y for y in np.arange(start_pos['y_start'], end_point, start_pos['y_increment'])]

# Get all z points if a starting range was not entered.
if not z_flag:
    end_point = start_pos['z_start']+start_pos['z_increment']*start_pos['num_start_z']
    z_points = [z for z in np.arange(start_pos['z_start'], end_point, start_pos['z_increment'])]

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
#   interpolated to back trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
traj_ds_obj = Back_traj_ds(version_number, interp_dir, parcel_label)

# Position data for the back trajectories.
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
# Open CM1 dataset over the time period where back trajectories are calculated.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_000{:03d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset+1, file_num_offset+parcel_time_step_num+1)]
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

# Minimum and maximum values in each dimension (based on the input indices)
#   (converted to meters).
xval_min = ds.variables[x_dim_param][xmin]*1000.
xval_max = ds.variables[x_dim_param][xmax]*1000.
yval_min = ds.variables[y_dim_param][ymin]*1000.
yval_max = ds.variables[y_dim_param][ymax]*1000.
zval_min = ds.variables[z_dim_param][zmin]*1000.
zval_max = ds.variables[z_dim_param][zmax]*1000.

# Locations of axis tick marks (in meters).
xticks = np.arange(xval_min,xval_max,xval_interval)
yticks = np.arange(yval_min,yval_max,yval_interval)
zticks = np.arange(zval_min,zval_max,zval_interval)

# Range of data points on which to plot the background data.
x_vals = np.linspace(xval_min, xval_max, xmax-xmin)
y_vals = np.linspace(yval_min, yval_max, ymax-ymin)

# Initialization Position time for parcels.
initialize_time = int(ds.variables['time'][parcel_time_step_num-1])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Variables to put in plot title
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Height of the background field variable, converted to meters.
contour_height = int(ds.variables[z_dim_param][parameters['offset']] * 1000.)

variable_long_name = getattr(ds.variables[variable], 'def').title()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate how many time steps of trajectory data to plot (based on
#   user-defined number of minutes to be plotted).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = 60. * plot_limit_minutes

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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# For selecting trajectories, only need to plot the last (initialization) time.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cur_file_num = parcel_time_step_num - 1

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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Display trajectories.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# List to store the back trajectory initialization points nearest to the
#   clicked points.
coords_meters = []

for y_plot_val, z_plot_val in itertools.product(y_points, z_points):
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Determination of which trajectories are to be plotted (based on
    #   initialization points).
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    plot_indices_part = {}

    plot_indices_part['y'] = np.where(ypos[0] == y_plot_val)[0]
    plot_indices_part['z'] = np.where(zpos[0] == z_plot_val)[0]

    # Get indices that are to be plotted from the intersection of the y and z
    #   parts.
    plot_indices = np.intersect1d(plot_indices_part['y'], plot_indices_part['z'])

    if len(plot_indices) > 0:
        # Minimum and maximum values for each position at initialization.
        xpos_min = int(np.min(xpos[0,plot_indices]))
        ypos_min = int(np.min(ypos[0,plot_indices]))
        zpos_min = int(np.min(zpos[0,plot_indices]))
        xpos_max = int(np.max(xpos[0,plot_indices]))
        ypos_max = int(np.max(ypos[0,plot_indices]))
        zpos_max = int(np.max(zpos[0,plot_indices]))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    #   Plot Trajectories                                                #
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^#
    # Inverted time index of the back trajectory data (which runs backwards in time).
    i = parcel_time_step_num - cur_file_num

    # Initialize the plot.
    fig2 = plt.figure(figsize=(14,7))
    ax = fig2.add_subplot(111)

    # Background field variable data for the filled contour plot.
    data_array = np.copy(ds.variables[variable][cur_file_num, parameters['offset'], ymin:ymax, xmin:xmax])

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
            norm = plt.Normalize(np.nanmin(zpos), np.nanmax(zpos))
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
    ax.set_xlabel('E-W Distance from Center (m)', fontsize = 16)
    ax.set_ylabel('N-S Distance from Center (m)', fontsize = 16)

    # Colorbar ticks for the background field variable.
    cticks = np.arange(parameters['datamin'], parameters['datamax']+parameters['val_interval'], parameters['val_interval'])
    # Colorbar for the background field variable.
    bar = plt.colorbar(ref, ticks=cticks)
    bar.set_label(parameters['bar_label'], fontsize = 16)

    # Adjust plot so that a given distance is of equal length on both axes.
    plt.axes().set_aspect('equal', 'datalim')

    plt.tight_layout()

    # List to store the x coordinates of the clicked points.
    coords = []

    cid = fig2.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    fig2.canvas.mpl_disconnect(cid)

    # Get the number of zooms to remove those clicks from the list of coordinates.
    zooms = input('# of Zooms (-1 to cancel):')
    if zooms == -1:
        sys.exit()
    # Convert the non-zoom coordinates to an array.
    traj_x_meters = np.array(coords[int(zooms):])

    # Determine which trajectory locations are closest to the points that were
    #   clicked on.
    for traj_x_loc in traj_x_meters:
        x_index = np.where(np.abs(xpos[0] - traj_x_loc) == np.min(np.abs(xpos[0] - traj_x_loc)))[0][0]
        x_plot_val = xpos[0,x_index]
        # Combine the calculate x location to the y and z locations, and add to
        #   the list of points.
        traj_meters = (z_plot_val, y_plot_val, x_plot_val)
        coords_meters.append(traj_meters)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Output the set of points to the file for this category.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
cat_traj_obj = Cat_traj(version_number, output_dir, parcel_label, category)
cat_traj_obj.open_file(category)

# Convert the list of new points a 2D array.
new_initial_pos = np.array(coords_meters)

cat_traj_obj.write_data(new_initial_pos)

