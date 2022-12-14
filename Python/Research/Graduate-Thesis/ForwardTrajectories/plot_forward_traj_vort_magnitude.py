#!/usr/bin/env python3
#
# Name:
#   plot_forward_traj_vort_magnitude.py
#
# Purpose:  Plot horizontal and vertical vorticity along CM1 forward
#           trajectories, and display the magnitudes at defined intervals.
#
# Syntax: python3 plot_forward_traj_integrated_vort_comp.py version_number parcel_label parcel_category number_plots
#
# Input:  CM1 netCDF model files
#         netCDF file containing vorticity budget data interpolated to forward
#           trajectory posititions
#         netCDF file containing intialization positions of forward trajectories
#           determined to be located in a certain region of the storm
#
# Execution Example:
#   python3 plot_forward_traj_vort_magnitude.py v5 1000parcel_tornadogenesis forward_flank 4
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
#   2022/10/04 - Lance Wilson:  Modify plot_forward_traj_integrated_vort_component
#                               to plot the horizontal and vertical vorticity,
#                               and display the magnitudes at specific times.
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
# Determine the magnitude of a component of vorticity at a particular time.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_mag_at_time(traj_vort, calc_time, simulation_times):
    time_index = np.argwhere(simulation_times == calc_time)[0,0]
    return traj_vort[time_index]

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
    print('Syntax: python3 plot_forward_traj_vort_magnitude.py version_number parcel_label parcel_category number_plots')
    print('Example: python3 plot_forward_traj_vort_magnitude.py v5 1000parcel_tornadogenesis forward_flank 4')
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

# How frequency of labels of vorticity magnitudes (every N minutes).
plot_freq_minutes = 2.5

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open object using netCDF files containing vorticity budget data interpolated
#   to back trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ds_obj = Forward_traj_ds(version_number, interp_dir, parcel_label)
ds_obj.read_data()

# Initialization Position time for parcels.
initialize_time = int(ds_obj.simulation_times[0])

parcel_time_step_num = ds_obj.parcel_time_step_num

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
plot_limit_seconds = np.round(ds_obj.simulation_times[-1] - ds_obj.simulation_times[0])

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

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the indices of the CM1 data subset that are to be labelled, based
#   on a user-defined frequency (in minutes) to plot magnitude labels.
#   The earliest time with visible trajectory paths and the initialization time
#   are also added to the list to be plotted.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert plot_freq_minutes to seconds.
plot_freq_seconds = 60. * plot_freq_minutes

# Initial list of times that should be plotted at this plotting frequency.
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
    diff1 = parcel_time_step_num - plot_file_nums[-1]
    diff2 = parcel_time_step_num - plot_file_nums[-2]
    # If the the last time is close to termination time, just replace it.
    if diff1 <= diff2/4.:
        plot_file_nums[-1] = parcel_time_step_num - 1
    else:
        plot_file_nums.append(parcel_time_step_num - 1)

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
for (plot_id, plot_index) in enumerate(plot_indices):

    interp_vort = np.zeros((3,ds_obj.parcel_time_step_num))
    for j, axis in enumerate(['x', 'y', 'z']):
        ds_var = axis + 'vort'
        vort_var = np.copy(ds.variables[ds_var][:,zmin:zmax,ymin:ymax,xmin:xmax])

        # Get "correct" vorticity (CM1 vorticity interpolated to trajectory
        #   positions) at each time step.
        for i in range(plot_limit+1):
            interp_xpos = ds_obj.xpos[i, plot_index]
            interp_ypos = ds_obj.ypos[i, plot_index]
            interp_zpos = ds_obj.zpos[i, plot_index]
            interp_vort[j,i] = interpolate_vort(grid_coord, interp_xpos, interp_ypos, interp_zpos, vort_var[i])

    vert_vort = interp_vort[2]
    # Horizontal vorticity magnitude.
    horiz_vort = np.sqrt(np.square(interp_vort[0]) + np.square(interp_vort[1]))

    # Get list of magnitudes to add as text to the plot.
    time_list = ds_obj.simulation_times[plot_file_nums]
    horiz_mag_list = [calc_mag_at_time(horiz_vort, t, ds_obj.simulation_times) for t in time_list]
    vert_mag_list = [calc_mag_at_time(vert_vort, t, ds_obj.simulation_times) for t in time_list]

    # Initialization (earliest time) trajectory positions.
    traj_init_xpos = ds_obj.xpos[0, plot_index]
    traj_init_ypos = ds_obj.ypos[0, plot_index]
    traj_init_zpos = ds_obj.zpos[0, plot_index]

    # Dimension of the data to put in the title.
    dir_string = title_dir_sub(axis)

    # Title string for trajectory that is plotted and its starting positions.
    title_substring = 'Trajectory {:d}, Initialized (z,y,x) (m): {:.1f}, {:.1f}, {:.1f}'.format(plot_index, traj_init_zpos, traj_init_ypos, traj_init_xpos)

    # Initialize the plot.
    fig2 = plt.figure(num=plot_id+1,figsize=(13,16))
    ax1 = fig2.add_subplot(2,1,1)
    ax2 = fig2.add_subplot(2,1,2)

    # Plot of horizontal vorticity (CM1 vorticity interpolated to trajectory
    #   positions) at each time step.
    ax1.plot(ds_obj.simulation_times[:plot_limit+1], horiz_vort[:plot_limit+1], label='Horiz. Vort.', color='black', linewidth=2)
    ax1.scatter(ds_obj.simulation_times[plot_file_nums], horiz_vort[plot_file_nums])

    # Plot of horizontal vorticity (CM1 vorticity interpolated to trajectory
    #   positions) at each time step.
    ax2.plot(ds_obj.simulation_times[:plot_limit+1], vert_vort[:plot_limit+1], label='Vert. Vort.', color='black', linewidth=2)
    ax2.scatter(ds_obj.simulation_times[plot_file_nums], vert_vort[plot_file_nums])

    ax1.set_title('Horizontal Vorticity)')
    ax2.set_title('Vertical Vorticity)')

    # Print labels of the magnitudes of vorticity onto the graph every
    #   plot_freq_num minutes
    for k, file_num in enumerate(plot_file_nums):
        ax1.text(ds_obj.simulation_times[file_num] * 1.001, horiz_vort[file_num] * 1.001, str(horiz_mag_list[k])[:7])
        ax2.text(ds_obj.simulation_times[file_num] * 1.001, vert_vort[file_num] * 1.001, str(vert_mag_list[k])[:7])

    fig2.suptitle(title_substring, fontsize=18)

    ax1.set_xlim(initialize_time, ds_obj.simulation_times[plot_limit])
    ax1.set_ylabel(r'Vorticity (s$\mathregular{^{-1}}$)', fontsize=18)
    ax2.set_xlim(initialize_time, ds_obj.simulation_times[plot_limit])
    ax2.set_ylabel(r'Vorticity (s$\mathregular{^{-1}}$)', fontsize=18)

    plt.xlabel('Simulation Time (seconds)', fontsize=18)
    image_file_name = output_dir + 'cm1_forwardtraj_vort_magnitude_{:s}_inittime{:d}_p{:d}.png'.format(parcel_label, initialize_time, plot_index)
    #plt.savefig(image_file_name, dpi=400)

plt.show()

