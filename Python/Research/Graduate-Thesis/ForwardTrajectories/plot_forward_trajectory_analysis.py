#!/usr/bin/env python3
#
# Name:
#   plot_forward_trajectory_analysis.py
#
# Purpose:  Plot CM1 foward trajectories used for analysis along with data
#           slices to visualize where the trajectories go.
#
# Syntax: python3 plot_forward_trajectory_analysis.py model_version_number parcel_id_num/label variable [x=x_min,xmax] [y=y_min,y_max] [z=z_min,z_max]
#
#   Input: CM1 netCDF model files
#          A CM1 parcel data netCDF file ("cm1out_pdata_{parcel_label}.nc")
#          The namelist ("namelist_{parcel_label}.input") used to initialize the
#               model run that generated the parcel data file.
#
# Execution Example:
#   python3 plot_forward_trajectory_analysis.py v5 1000parcel_tornadogenesis xvort x=575,1500 z=75,250
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
#   2022/03/30 - Lance Wilson:  Split from plot_forward_trajectory_elevation_color
#                               to plot analysis trajectories, which need to
#                               have an end time specified.
#   2022/05/03 - Lance Wilson:  Changed plot ticks to kilometers.
#   2022/05/04 - Lance Wilson:  Added plotting of data outside of shown domain.
#

from calc_file_num_offset import calc_parcel_start_time, calc_parcel_end_time, calc_file_offset
from parameter_list import parameters

from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
from netCDF4 import Dataset
from netCDF4 import MFDataset

import atexit
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import sys

def closeNCfiles(ds):
    ds.close()

mandatory_arg_num = 3

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_id = sys.argv[2]
    variable = sys.argv[3]
else:
    print('Parcel data file, model version number, and/or variable to plot slice of was not specified.')
    print('Syntax: python3 plot_forward_trajectory_analysis.py model_version_number parcel_id_num/label variable [x=x_min,xmax] [y=y_min,y_max] [z=z_min,z_max]')
    print('Example: python3 plot_forward_trajectory_analysis.py v5 1000parcel_tornadogenesis xvort x=575,1500 z=75,250')
    print('Currently supported version numbers: v4, v5')
    sys.exit()

# Command-line arguments for plotting limited sets of trajectories.
x_flag = False
y_flag = False
z_flag = False
if len(sys.argv) > mandatory_arg_num + 1:
    for coord in sys.argv[mandatory_arg_num+1:]:
        if coord.startswith('x='):
            x_plot_vals = coord.split('=')[-1].split(',')
            # Convert to kilometers.
            x_plot_min = float(x_plot_vals[0])/1000.
            x_plot_max = float(x_plot_vals[1])/1000.
            x_flag = True
        if coord.startswith('y='):
            y_plot_vals = coord.split('=')[-1].split(',')
            # Convert to kilometers.
            y_plot_min = float(y_plot_vals[0])/1000.
            y_plot_max = float(y_plot_vals[1])/1000.
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
model_dir = '75m_100p_{:s}/'.format(version_number)
parcel_dir = '75m_100p_{:s}/parcel_files/'.format(version_number)
namelist_dir = '75m_100p_{:s}/namelists/'.format(version_number)

output_dir = model_dir + '/forward_traj_analysis/ForwardTrajectoryImages/'

parcel_file_name = parcel_dir + 'cm1out_pdata_{:s}.nc'.format(parcel_id)
namelist_filename = namelist_dir + 'namelist_{:s}.input'.format(parcel_id)

# How frequency to show output plots (every N minutes).
plot_freq_minutes = 4.

# Minimum and maximum indices in each dimension.
# Full storm scale
xmin = 160
xmax = 810
ymin = 170
ymin = 140
ymax = 620
zmin = 0
zmax = 40

# Axis tick intervals based in kilometers (tick marks every N kilometers).
xval_interval = 4.
yval_interval = 4.

# Colormap used for the elevation colorbar.
elev_colormap = 'gist_rainbow'

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Use the namelist.input file to get when parcels start moving.
parcel_start_time = calc_parcel_start_time(parcel_id, namelist_filename)

# Use the namelist.input file to get when this parcel run ends.
parcel_end_time = calc_parcel_end_time(parcel_id, namelist_filename)

# Model file when parcels start moving.
file_num_offset = calc_file_offset(version_number, parcel_start_time)

# Model file when parcels stop (should be one output step after the intended
#   termination time).
file_num_end = calc_file_offset(version_number, parcel_end_time)

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
# Converting x and y locations to kilometers for plotting.
xpos = np.copy(ds_parcel.variables['x'][:])/1000.
ypos = np.copy(ds_parcel.variables['y'][:])/1000.
# Leaving z location in meters (for colorbar scale).
zpos = np.copy(ds_parcel.variables['z'][:])
parcel_times = np.copy(ds_parcel.variables['time'][:])
ds_parcel.close()

# Use parcel start and end time to determine the array indices of parcel data
#   to use.
parcel_start_diff = np.abs(parcel_times - parcel_start_time)
parcel_end_diff = np.abs(parcel_times - parcel_end_time)

parcel_start_index = np.argwhere(parcel_start_diff == np.min(parcel_start_diff))[0,0]
parcel_end_index = np.argwhere(parcel_end_diff == np.min(parcel_end_diff))[0,0]

# Number of parcel output times in the model run.
parcel_output_num = len(xpos)

# Total number of parcels.
total_parcel_num = xpos[0].size

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset over the time period where forward trajectories were
#   calculated in the model.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset, file_num_end)]
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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Variables to put in plot title
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Height of the background field variable, converted to meters.
contour_height = int(ds.variables[z_dim_param][parameters['offset']] * 1000.)

variable_long_name = getattr(ds.variables[variable], 'def').title()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Starting points of the trajectories (based on initialization points).
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# For each set of coordinates, the valid plot indices for that dimension are
#   the indices where that position array is between (inclusive) the values (in
#   meters) in the command line argument (ex. x=750,1000) if one was supplied.
#   If no argument was supplied, then all indices may be used.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if x_flag == True:
    part1 = np.where(xpos[parcel_start_index] >= x_plot_min)[0]
    part2 = np.where(xpos[parcel_start_index] <= x_plot_max)[0]
    plot_indices_part_x = np.intersect1d(part1, part2)
else:
    plot_indices_part_x = range(total_parcel_num)

if y_flag == True:
    part1 = np.where(ypos[parcel_start_index] >= y_plot_min)[0]
    part2 = np.where(ypos[parcel_start_index] <= y_plot_max)[0]
    plot_indices_part_y = np.intersect1d(part1, part2)
else:
    plot_indices_part_y = range(total_parcel_num)

if z_flag == True:
    part1 = np.where(zpos[parcel_start_index] >= z_plot_min)[0]
    part2 = np.where(zpos[parcel_start_index] <= z_plot_max)[0]
    plot_indices_part_z = np.intersect1d(part1, part2)
else:
    plot_indices_part_z = range(total_parcel_num)

# Get indices that are to be plotted from the intersection of the x and y
#   parts, and then the intersection of that and the z part.
part1 = np.intersect1d(plot_indices_part_x, plot_indices_part_y)
plot_indices = np.intersect1d(part1, plot_indices_part_z)

if len(plot_indices) > 0:
    # Minimum and maximum values for each position initialization (in meters).
    xpos_min = int(np.min(xpos[parcel_start_index,plot_indices])*1000)
    ypos_min = int(np.min(ypos[parcel_start_index,plot_indices])*1000)
    zpos_min = int(np.min(zpos[parcel_start_index,plot_indices]))
    xpos_max = int(np.max(xpos[parcel_start_index,plot_indices])*1000)
    ypos_max = int(np.max(ypos[parcel_start_index,plot_indices])*1000)
    zpos_max = int(np.max(zpos[parcel_start_index,plot_indices]))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the indices of the CM1 data subset that are to be plotted, based
#   on a user-defined frequency (in minutes) to plot images.
#   The earliest (initialization) time is also added to the list to be plotted.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_limit_minutes to seconds.
plot_limit_seconds = parcel_end_time - parcel_start_time

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

# Make sure the last (termination) time is plotted.
if not (file_num_end - 1) in plot_file_nums:
    plot_file_nums.append(file_num_end - 1)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Plot Trajectories
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Loop over each parcel output time that is to be plotted.
for cur_file_num in plot_file_nums:
    #fig2 = plt.figure(figsize=(10,7))
    fig2 = plt.figure(figsize=(13,7))

    # Initialize the plot.
    ax = fig2.add_subplot(111)

    cur_index_num = cur_file_num - file_num_offset
    # Background field variable data for the filled contour plot.
    data_array = np.copy(ds.variables[variable][cur_index_num,parameters['offset'],:,:])

    z_vals = data_array

    # Make a filled contour plot of the background field variable.
    ref = ax.contourf(x_vals, y_vals, z_vals, np.linspace(parameters['datamin'], parameters['datamax'], parameters['contour_interval']), offset=parameters['offset'], zdir='z', cmap=parameters['colormap'])

    # Model file number of the whole CM1 model run (as opposed to the
    #   subset taken for plotting).
    model_file_num = file_num_offset + cur_index_num
    # The simulation time (in seconds) of this model time step.
    real_file_time = int(ds.variables['time'][cur_index_num])

    cur_parcel_diff = np.abs(parcel_times - real_file_time)
    cur_parcel_index = np.argwhere(cur_parcel_diff == np.min(cur_parcel_diff))[0,0]

    if len(plot_indices) > 0:
        # Scatter plot of the initial positions of the trajectories.
        #norm = plt.Normalize(np.nanmin(zpos), np.nanmax(zpos))
        norm = plt.Normalize(np.nanmin(zpos), 1000.)
        ax.scatter(xpos[parcel_start_index, plot_indices], ypos[parcel_start_index, plot_indices], c=zpos[parcel_start_index, plot_indices], norm=norm, cmap=elev_colormap)

        for j in plot_indices:
            # Take subsets of x, y, and z trajectory positions from the
            #   earliest time to the time currently being plotted.
            xpos_subset = xpos[parcel_start_index:cur_parcel_index,j]
            ypos_subset = ypos[parcel_start_index:cur_parcel_index,j]
            zpos_subset = zpos[parcel_start_index:cur_parcel_index,j]

            points = np.array([xpos_subset, ypos_subset]).T.reshape(-1, 1, 2)
            segments = np.concatenate([points[:-1], points[1:]], axis=1)
            lc = LineCollection(segments, cmap=elev_colormap, norm=norm)
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
    ax.set_xlim(xval_min, xval_max)
    ax.set_ylim(yval_min, yval_max)
    ax.set_xlabel('E-W Distance (km)', fontsize = 16)
    ax.set_ylabel('N-S Distance (km)', fontsize = 16)

    # Colorbar ticks for the background field variable.
    cticks = np.arange(parameters['datamin'], parameters['datamax']+parameters['val_interval'], parameters['val_interval'])
    # Colorbar for the background field variable.
    bar = plt.colorbar(ref, ticks=cticks)
    bar.set_label(parameters['bar_label'], fontsize = 16)

    # Adjust plot so that a given distance is of equal length on both axes.
    plt.axes().set_aspect('equal', 'datalim')

    plt.tight_layout()

    # Code to save files
    image_file_name = output_dir + 'cm1_forwardtraj_{:s}_{:s}_nc{:d}_time{:d}.png'.format(parcel_id, variable, model_file_num, real_file_time)
    #plt.savefig(image_file_name, dpi=400)

plt.show()

