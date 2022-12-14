#!/usr/bin/env python3
#
# Name:
#   plot_forward_trajectory.py
#
# Purpose:  Plot CM1 foward trajectories along with data slices to visualize
#           where the trajectories go.
#
# Syntax: python3 plot_forward_trajectory.py model_version_number parcel_id_num variable [x=x_val] [y=y_val] [z=z_val]
#
#   Input:
#
# Execution Example:
#   python3 plot_forward_trajectory.py v3 7 xvort z=750
#
# Modification History:
#   2019/09/19 - Lance Wilson:  Modified from code written by Tom Gowan, using
#                               trajectories_plot.ipynb from:
# https://github.com/tomgowan/trajectories/blob/master/trajectory_plot.ipynb
#   2019/10/01 - Lance Wilson:  Split 3D plot into separate file, as that is
#                               likely what will be used going forward.
#   2020/11/23 - Lance Wilson:  New file to plot trajectory positions from a
#                               cm1out_pdata.nc file.
#   2020/12/18 - Lance Wilson:  Attempting to combine
#                               plot_trajectory_3d_20191001.py and
#                               plot_output_trajectory_3d_test.py.
#   2021/12/28 - Lance Wilson:  Added improvements from plot_back_trajectory
#                               and plot_back_traj_budgets.
#

from calc_file_num_offset import calc_parcel_start_time, calc_file_offset
from parameter_list import parameters

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from netCDF4 import Dataset
from netCDF4 import MFDataset

import atexit
import itertools
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import sys

def closeNCfiles(ds):
    ds.close()

mandatory_arg_num = 3

if len(sys.argv) > 3:
    version_number = sys.argv[1]
    parcel_id = sys.argv[2]
    variable = sys.argv[3]
else:
    print('Parcel data file, model version number, and/or variable to plot slice of was not specified.')
    print('Syntax: python3 plot_forward_trajectory.py model_version_number parcel_id_num variable [x=x_val] [y=y_val] [z=z_val]')
    print('Example: python3 plot_forward_trajectory.py v3 7 xvort z=75')
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
model_dir = '75m_100p_{:s}/'.format(version_number)
parcel_dir = '75m_100p_{:s}/parcel_files/'.format(version_number)
namelist_dir = '75m_100p_{:s}/namelists/'.format(version_number)

parcel_file_name = parcel_dir + 'cm1out_pdata_{:s}.nc'.format(parcel_id)
namelist_filename = namelist_dir + 'namelist_{:s}.input'.format(parcel_id)

# How many minutes of trajectories to plot.
plot_limit_minutes = 20.

# How frequency to show output plots (every N minutes).
plot_freq_minutes = 5.

# Minimum and maximum indices in each dimension.
# Full storm scale
xmin = 160
xmax = 610
ymin = 170
ymax = 620
zmin = 0
zmax = 40

# Axis tick intervals based in meters (tick marks every N meters).
xval_interval = 4000.
yval_interval = 4000.
zval_interval = 60.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# Use the namelist.input file to get when parcels start moving.
parcel_start_time = calc_parcel_start_time(parcel_id, namelist_filename)

# Model file when parcels start moving.
file_num_offset = calc_file_offset(version_number, parcel_start_time)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get parameters for the background field variable from parameter_list.py
#   Available parameters (2021/11/09):
#           'val_interval'          'datamin'           'datamax'
#           'offset'                'bar_label'         'colormap'
#           'contour_interval' 
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
parameters = parameters(variable)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load forward trajectory data from the cm1out_pdata netCDF file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ds_parcel = Dataset(parcel_file_name, "r")
xpos = np.copy(ds_parcel.variables['x'][:])
ypos = np.copy(ds_parcel.variables['y'][:])
zpos = np.copy(ds_parcel.variables['z'][:])
ds_parcel.close()

# Number of parcel output times in the model run.
parcel_output_num = len(xpos)

# Total number of parcels.
total_parcel_num = xpos[0].size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset over the time period where forward trajectories were
#   calculated in the model.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset, parcel_output_num+1)]
ds = MFDataset(file_list)
# Close the netCDF dataset when the program exits.
atexit.register(closeNCfiles, ds)

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

# Location of axis tick marks (in meters)
xticks = np.arange(xval_min,xval_max,xval_interval)
yticks = np.arange(yval_min,yval_max,yval_interval)
zticks = np.arange(zval_min,zval_max,zval_interval)

# Range of data points on which to plot the background data.
x_vals = np.linspace(xval_min, xval_max,xmax-xmin)
y_vals = np.linspace(yval_min, yval_max,ymax-ymin)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Variables to put in plot title
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Height of the background field variable, converted to meters.
contour_height = int(ds.variables[z_dim_param][parameters['offset']] * 1000.)

variable_long_name = getattr(ds.variables[variable], 'def').title()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Starting points of the trajectories (based on initialization points).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
plot_indices_part = {}
# For each set of coordinates, the valid plot indices for that dimension are
#   the indices where that position array is equal to the command-line
#   argument if one was supplied.  If no argument was supplied, then all
#   indices may be used.
if x_flag == True:
    x_diff = np.abs(xpos[file_num_offset-1] - x_plot_val)
    plot_indices_part['x'] = np.where(x_diff == np.min(x_diff))[0]
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
    xpos_min = int(np.min(xpos[file_num_offset-1,plot_indices]))
    ypos_min = int(np.min(ypos[file_num_offset-1,plot_indices]))
    zpos_min = int(np.min(zpos[file_num_offset-1,plot_indices]))
    xpos_max = int(np.max(xpos[file_num_offset-1,plot_indices]))
    ypos_max = int(np.max(ypos[file_num_offset-1,plot_indices]))
    zpos_max = int(np.max(zpos[file_num_offset-1,plot_indices]))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the indices of the CM1 data subset that are to be plotted, based
#   on a user-defined frequency (in minutes) to plot images.
#   The earliest (initialization) time is also added to the list to be plotted.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = 60. * plot_limit_minutes

data_timespan = ds.variables['time'][-1] - ds.variables['time'][0]

# Ensure that the data does not repeat plots if the plot limit is greater than
#   the available amount of data by limiting it to the total timespan of data.
if plot_limit_seconds > data_timespan:
    plot_limit_seconds = np.round(data_timespan)

# Array of all time steps lengths for this set of trajectory data.
time_step_lengths = np.round(ds.variables['time'][1:] - ds.variables['time'][:-1])
# Cumulative sum array of the time step lengths.
cumulative_time_steps = np.cumsum(time_step_lengths)

# Check that at least one time step is going to be plotted (i.e.
#   plot_limit_seconds must be no smaller than the smallest time_step),
#   otherwise np.argwhere result will be empty and crash the program.
if plot_limit_seconds < time_step_lengths[0]:
    print('Length of time desired to plot is less than the time step, ' + 
          'so there is no trajectory data to plot.')
    sys.exit()

# Convert plot_freq_minutes to seconds.
plot_freq_seconds = 60. * plot_freq_minutes

# Initial list of times that should be plotted at this plotting frequency
plot_freq_times = np.arange(0, plot_limit_seconds+1, plot_freq_seconds)[1:]

# Empty list to store the model file numbers that are to be plotted.
plot_file_nums = []

# Convert each plot frequency time (in seconds) to the nearest file number.
for plot_time in plot_freq_times:
    diff = np.abs(cumulative_time_steps - plot_time)
    # Number of file numbers forward from the initialization time.
    #   Add one to account for the CM1 files starting at 1.
    file_num_forward = np.argwhere(diff == np.min(diff))[0,0] + 1

    # Add the above number of time steps to the model file number offset to get
    #   the actual file number from the CM1 dataset.
    subset_file_num = file_num_offset + file_num_forward

    plot_file_nums.append(subset_file_num)

# Make sure the earliest time is plotted.
if not file_num_offset in plot_file_nums:
    plot_file_nums = [file_num_offset] + plot_file_nums

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Plot Trajectories
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Loop over each parcel output time that is to be plotted.
for cur_file_num in plot_file_nums:
    fig2 = plt.figure(figsize=(10,7))

    # Initialize the plot.
    ax = fig2.add_subplot(111)

    cur_index_num = cur_file_num - file_num_offset
    # Background field variable data for the filled contour plot.
    data_array = np.copy(ds.variables[variable][cur_index_num,parameters['offset'],ymin:ymax,xmin:xmax])

    z_vals = data_array

    # Make a filled contour plot of the background field variable.
    ref = ax.contourf(x_vals, y_vals, z_vals, np.linspace(parameters['datamin'], parameters['datamax'], parameters['contour_interval']), offset=parameters['offset'], zdir='z', cmap=parameters['colormap'])

    # Model file number of the whole CM1 model run (as opposed to the
    #   subset taken for plotting).
    model_file_num = file_num_offset + cur_index_num
    # The simulation time (in seconds) of this model time step.
    real_file_time = int(ds.variables['time'][cur_index_num])

    if len(plot_indices) > 0:
        for j in plot_indices:
            # Scatter plot of the initial positions of the trajectories.
            ax.scatter(xpos[file_num_offset-1,j], ypos[file_num_offset-1,j])
            # Take subsets of x, y, and z trajectory positions from the
            #   earliest time to the time currently being plotted.
            xpos_subset = xpos[file_num_offset-1:cur_file_num,j]
            ypos_subset = ypos[file_num_offset-1:cur_file_num,j]
            zpos_subset = zpos[file_num_offset-1:cur_file_num,j]

            points = np.array([xpos_subset, ypos_subset]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            #norm = plt.Normalize(np.nanmin(zpos), np.nanmax(zpos))
            norm = plt.Normalize(np.nanmin(zpos), 1000.)
            lc = LineCollection(segments, cmap='gist_rainbow', norm=norm)
            lc.set_array(zpos_subset)
            lc.set_linewidth(2)
            line = ax.add_collection(lc)
        # Colorbar for the trajectory height.
        bar2 = fig2.colorbar(line, ax=ax)
        bar2.set_label('Height (m)', fontsize = 16)

        plt.title('Simulation Time {:d} s (Model File {:d})\n{:s} at Height {:d} m, Forward Trajectories Initialized at {:d} s\nStarting Positions (m): X ({:d} to {:d}), Y ({:d} to {:d}), Z ({:d} to {:d})\nParcels Plotted/Total Parcel Number: {:d}/{:d}'.format(real_file_time, model_file_num, variable_long_name, contour_height, parcel_start_time, xpos_min, xpos_max, ypos_min, ypos_max, zpos_min, zpos_max, len(plot_indices), total_parcel_num))
    else:
        plt.title('Simulation Time {:d} s (Model File {:d})\n{:s} at Height {:d} m'.format(real_file_time, model_file_num, variable_long_name, contour_height))
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xlabel('E-W Distance (m)', fontsize = 16)
    ax.set_ylabel('N-S Distance (m)', fontsize = 16)

    # Colorbar ticks for the background field variable.
    cticks = np.arange(parameters['datamin'], parameters['datamax']+parameters['val_interval'], parameters['val_interval'])
    # Colorbar for the background field variable.
    bar = plt.colorbar(ref, ticks=cticks)
    bar.set_label(parameters['bar_label'], fontsize = 16)

    # Adjust plot so that a given distance is of equal length on both axes.
    plt.axes().set_aspect('equal', 'datalim')

    plt.tight_layout()

    # Code to save files
    #image_file_name = 'ForwardTrajectoryImages/cm1_forwardtraj_{:s}_{:s}_nc{:d}_time{:d}.png'.format(parcel_id, variable, model_file_num, real_file_time)
    #plt.savefig(image_file_name, dpi=400)

plt.show()

