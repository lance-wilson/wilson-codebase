#!/usr/bin/env python3
#
# Name:
#   meso_vort_source_percentage_auto.py
#
# Purpose:  Calculate the percentage of vorticity entering the mesocyclone that
#           is from a particular source region (or regions).
#
# Syntax: python3 meso_vort_source_percentage_auto.py version_number parcel_label parcel_category1[,parcel_category2...]
#
#   Input:
#
# Execution Example:
#   python3 meso_vort_source_percentage_auto.py v5 v5_meso_tornadogenesis forward_flank,wraparound
#
# Modification History:
#   2022/01/28 - Lance Wilson:  Created.

from back_traj_interp_class import Back_traj_ds
from categorize_traj_class import Cat_traj
from calc_parcel_bounds import calc_bound_index
from trajectory_category_parameters import termination_parameters

from netCDF4 import MFDataset
from scipy import interpolate

import atexit
import numpy as np
import operator
import sys
import time

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Close the main CM1 model data netCDF file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def closeNCfile(ds):
    ds.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Determine what valid indices remain (valid_traj_indices) after calculating
#   the valid trajectories based on a specific condition (valid_this_case).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def eval_valid_indices(valid_traj_indices, valid_this_case):
    # If both arrays have indices, find the intersection of the two arrays.
    if valid_traj_indices.size != 0 and valid_this_case.size != 0:
        valid_traj_indices = np.intersect1d(valid_traj_indices, valid_this_case)
    # Otherwise, the valid indices are whatever is valid for this condition.
    #   Note: If valid_this_case is empty, then valid_traj_indices should
    #   remain empty after the else block.
    else:
        valid_traj_indices = np.copy(valid_this_case)
    return valid_traj_indices

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Find trajectories that terminate in the mesocyclone
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def get_meso_indices(ds, xpos, ypos, zpos, x_coord, y_coord, x_coord_stag, y_coord_stag):
    # Dictionary storing mathmatical operators from the operator module so that
    #   operators can be determined on a case-by-case basis.
    # Examples: ops['<'](a,b) is equivalent to: operator.lt(a,b); a < b
    ops =  {'<=' : operator.le,
            '>=' : operator.ge,
            '<'  : operator.lt,
            '>'  : operator.gt,
        }

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Find trajectories that terminate in the mesocyclone
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Parameters used for determining if the trajectory ends in the correct place.
    #end_point_params = end_point_dict[end_point_param_key]
    end_point_params = termination_parameters()['mesocyclone']

    valid_traj_indices = np.empty((0,))

    # List of keys that do not have a value of None for the this set of
    #   trajectory end points.
    defined_end_point_keys = [key for key in end_point_params.keys() if end_point_params[key]]

    for key in defined_end_point_keys:
        if key.startswith('x'):
            positions = xpos[0]
        if key.startswith('y'):
            positions = ypos[0]
        if key.startswith('z'):
            positions = zpos[0]

        if key.endswith('max'):
            # Determine which trajectories remain below the required limit over
            #   the prescribed time period.
            valid_this_case = np.argwhere(positions <= end_point_params[key])[:,0]
            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After mesocyclone {:s}:\t{:d}'.format(key, valid_traj_indices.size))

        elif key.endswith('min'):
            # Determine which trajectories remain above the required limit over
            #   the prescribed time period.
            valid_this_case = np.argwhere(positions >= end_point_params[key])[:,0]
            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After mesocyclone {:s}:\t{:d}'.format(key, valid_traj_indices.size))

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If looking at the threshold criteria, make a list of the model fields
        #   needed for comparision.
        if key == 'thresholds':
            model_fields = [threshold for threshold in end_point_params[key].keys()]
        # If the key is not 'thresholds', create an empty list so the for loop
        #   does not run.
        else:
            model_fields = []

        for model_field in model_fields:
            # Array index of model height.
            model_level = end_point_params[key][model_field][0]
            # Value to compare the model variable data against.
            field_value = end_point_params[key][model_field][1]
            # Whether the values along the trajectory should be e.g. less than
            #   or greater than the comparison value.
            operation = end_point_params[key][model_field][2]

            # Determine which model coordinates to use (must use staggered
            #   grids if interpolating velocity values).
            x_coord_field = x_coord_stag if model_field == 'u' else x_coord
            y_coord_field = y_coord_stag if model_field == 'v' else y_coord

            # Regular grid points for one model level at one time.
            grid_coord_2D = (y_coord_field,x_coord_field)

            # Get values of this budget variable at this time step.
            variable = np.copy(ds.variables[model_field][-1,model_level,:,:])

            # Get backward trajectory coordinates at this time step.
            x_traj_coord = xpos[0]
            y_traj_coord = ypos[0]

            # Create array representing the points that the model variable is
            #   going to be sampled at.
            traj_points = np.column_stack((y_traj_coord, x_traj_coord))

            # Interpolate the model variable to the trajectory points.
            interpolated_values = interpolate.interpn(grid_coord_2D, variable, traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

            # Find trajectories that meet the criterion at this time.
            valid_this_case = np.argwhere(ops[operation](interpolated_values, field_value))[:,0]

            # Determine which valid indices remain.
            valid_traj_indices = eval_valid_indices(valid_traj_indices, valid_this_case)

            #print('After mesocyclone {:s}:\t{:d}'.format(model_field, valid_traj_indices.size))


    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if valid_traj_indices.size == 0:
        print('No trajectories terminate within the mesocyclone for this dataset.')
        sys.exit()

    return valid_traj_indices

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Command-line arguments.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
mandatory_arg_num = 3

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    parcel_category_arg = sys.argv[3]
else:
    print('Variable to plot slice, parcel label, and version number must be specified.')
    print('Syntax: python3 meso_vort_source_percentage_auto.py version_number parcel_label parcel_category1[,parcel_category2...]')
    print('Example: python3 meso_vort_source_percentage_auto.py v5 v5_meso_tornadogenesis forward_flank,wraparound')
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

# Split the parcel category argument into a list for if multiple categories
#   are being used.
parcel_categories = parcel_category_arg.split(',')

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
# Directory for output file.
output_dir = cat_dir + 'vorticity_source_percent/'

outfile_name = output_dir + '{:s}_{:s}_{:s}_vort_source.txt'.format(version_number, parcel_label, parcel_category_arg)

# How far back (in minutes) to look at trajectories for getting initial positions for categories.
plot_limit_minutes = 10.

# Buffer around model grid points to make sure their is data for interpolation.
bound_buffer = 3

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create object that opens netCDF files containing vorticity budget data
#   interpolated to back trajectory locations.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
traj_ds_obj = Back_traj_ds(version_number, interp_dir, parcel_label)

# Position data for all the back trajectories.
xpos_full = traj_ds_obj.xpos
ypos_full = traj_ds_obj.ypos
zpos_full = traj_ds_obj.zpos

# Total number of parcels for this set of data.
total_parcel_num = traj_ds_obj.total_parcel_num

# Model file at the earliest time of the trajectory dataset (zero-indexed,
#   add one to get the correct CM1 model file).
file_num_offset = traj_ds_obj.file_num_offset

# Get the number of time steps in the full set of parcel data.
parcel_time_step_num = traj_ds_obj.parcel_time_step_num

# Model simulation times with back trajectory data.
simulation_times = traj_ds_obj.simulation_times

# Index of the back trajectory dataset used for this analysis.
#traj_time_index = np.argwhere(np.abs(simulation_times - analysis_time) == np.min(np.abs(simulation_times - analysis_time)))[0,0]
traj_time_index = 0

# Get back trajectory coordinates for the full dataset at this time step.
x_traj_coord_full = xpos_full[traj_time_index]
y_traj_coord_full = ypos_full[traj_time_index]
z_traj_coord_full = zpos_full[traj_time_index]

# Create array representing the points that the vorticity variables are
#   going to be sampled at.
full_traj_points = np.column_stack((z_traj_coord_full, y_traj_coord_full, x_traj_coord_full))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open CM1 dataset over the time period where back trajectories are calculated.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_list = [model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset+1, file_num_offset+parcel_time_step_num+1)]
ds = MFDataset(file_list)

# Close the main CM1 data netCDF file when the program exits.
atexit.register(closeNCfile, ds)

# Coordinates of the unstaggered CM1 grid in each dimension (converted from
#   kilometers to meters).
x_coord = np.copy(ds.variables['xh'])*1000.
y_coord = np.copy(ds.variables['yh'])*1000.
z_coord = np.copy(ds.variables['z'])*1000.

# Staggered coordinates in each dimension (converted to meters).
x_coord_stag = np.copy(ds.variables['xf'])*1000.
y_coord_stag = np.copy(ds.variables['yf'])*1000.

# Model file number at the parcel initialization time.
#model_time_step = parcel_time_step_num - traj_time_index - 1
model_time_step = -1

# Get the boundary indices of the CM1 data that the full set of trajectories
#   are located in (to save time in loading vorticity data).
x1 = calc_bound_index(x_coord, np.min(x_traj_coord_full), -1 * bound_buffer)
y1 = calc_bound_index(y_coord, np.min(y_traj_coord_full), -1 * bound_buffer)
z1 = calc_bound_index(z_coord, np.min(z_traj_coord_full), -1 * bound_buffer)
x2 = calc_bound_index(x_coord, np.max(x_traj_coord_full), bound_buffer)
y2 = calc_bound_index(y_coord, np.max(y_traj_coord_full), bound_buffer)
z2 = calc_bound_index(z_coord, np.max(z_traj_coord_full), bound_buffer)

# Create a tuple of the coordinates that is passed to the interpn function
#   to be used as the regular grid.
grid_coord = (z_coord[z1:z2],y_coord[y1:y2],x_coord[x1:x2])

# Get values of vorticity at this time step.
xvort = np.copy(ds.variables['xvort'][model_time_step,z1:z2,y1:y2,x1:x2])
yvort = np.copy(ds.variables['yvort'][model_time_step,z1:z2,y1:y2,x1:x2])
zvort = np.copy(ds.variables['zvort'][model_time_step,z1:z2,y1:y2,x1:x2])

# Get values of wind interpolated to the scalar grid points.
u_interp = np.copy(ds.variables['uinterp'][model_time_step,z1:z2,y1:y2,x1:x2])
v_interp = np.copy(ds.variables['vinterp'][model_time_step,z1:z2,y1:y2,x1:x2])
w_interp = np.copy(ds.variables['winterp'][model_time_step,z1:z2,y1:y2,x1:x2])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Interpolate vorticity to the full dataset of back trajectory points at this
#   time step.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Individual vorticity components.
xvort_full = interpolate.interpn(grid_coord, xvort, full_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
yvort_full = interpolate.interpn(grid_coord, yvort, full_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
zvort_full = interpolate.interpn(grid_coord, zvort, full_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

# Full horizontal vorticity.
horiz_full = np.sqrt(np.square(xvort_full) + np.square(yvort_full))
# Full 3D vorticity.
vort3d_full = np.sqrt(np.square(xvort_full) + np.square(yvort_full) + np.square(zvort_full))

# Individual wind components.
u_full = interpolate.interpn(grid_coord, u_interp, full_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
v_full = interpolate.interpn(grid_coord, v_interp, full_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
w_full = interpolate.interpn(grid_coord, w_interp, full_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

# Helicity components.
x_helicity_full = u_full * xvort_full
y_helicity_full = v_full * yvort_full
z_helicity_full = w_full * zvort_full

# Horizontal helicity.
horiz_helicity_full = x_helicity_full + y_helicity_full
# Full 3D helicity.
helicity_3d_full = x_helicity_full + y_helicity_full + z_helicity_full

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

# How far back (in time steps) to plot trajectories.
#   The final row of the np.argwhere output contains the index of the last
#   appropriate time, so the limit for the plotting loop is one more than that.
plot_limit = np.argwhere(cumulative_time_steps <= plot_limit_seconds)[-1,0] + 1

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get position data for the backward trajectories, reversed in time (i.e.
#   increasing array index is forward in time), for the time period being
#   analyzed.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
xpos_subset = traj_ds_obj.xpos[::-1][parcel_time_step_num-plot_limit:]
ypos_subset = traj_ds_obj.ypos[::-1][parcel_time_step_num-plot_limit:]
zpos_subset = traj_ds_obj.zpos[::-1][parcel_time_step_num-plot_limit:]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get back trajectory data at the analysis time step for the category (or
#   categories) being analyzed.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Empty array to concatenate array of indices of categorized back trajectories.
category_indices = np.zeros((0), dtype=np.int)

for parcel_category in parcel_categories:
    # Trajectories to be plotted, based on intialization positions stored in a
    #   netCDF file created by categorize_trajectories.
    #cat_traj_obj = Cat_traj(version_number, cat_dir, parcel_label, parcel_category)
    cat_traj_obj = Cat_traj(version_number, cat_dir, parcel_label, parcel_category + '_auto')
    # It is possible that a file could be created without there being any data
    #   in it, so plots will only be attempted if the object's "existing_file"
    #   flag is true.
    if cat_traj_obj.existing_file:
        #cat_traj_obj.open_file(parcel_category)
        cat_traj_obj.open_file(parcel_category + '_auto')
        # Initialization positions are converted to an array index.
        category_indices = np.concatenate((category_indices, cat_traj_obj.meters_to_trajnum(xpos_subset, ypos_subset, zpos_subset)))
    else:
        print 'Categorized trajectory file {:s} does not contain any data'.format(parcel_category)
        sys.exit()

# Make sure there is only one of each index.
category_indices = np.unique(category_indices)

# Determine the percentage of valid trajectories that the category represents.
num_category_traj = len(category_indices)
category_traj_percent = 100. * num_category_traj/total_parcel_num

# Get coordinates of this category's back trajectory data at this time step.
x_traj_coord_cat = xpos_full[traj_time_index,category_indices]
y_traj_coord_cat = ypos_full[traj_time_index,category_indices]
z_traj_coord_cat = zpos_full[traj_time_index,category_indices]

# Create array representing the points that the vorticity variable is
#   going to be sampled at.
category_traj_points = np.column_stack((z_traj_coord_cat, y_traj_coord_cat, x_traj_coord_cat))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Interpolate vorticity to to this category's back trajectory points at this
#   time step.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Individual vorticity components.
xvort_category = interpolate.interpn(grid_coord, xvort, category_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
yvort_category = interpolate.interpn(grid_coord, yvort, category_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
zvort_category = interpolate.interpn(grid_coord, zvort, category_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

# Full horizontal vorticity.
horiz_category = np.sqrt(np.square(xvort_category) + np.square(yvort_category))
# Full 3D vorticity.
vort3d_category = np.sqrt(np.square(xvort_category) + np.square(yvort_category) + np.square(zvort_category))

# Individual wind components.
u_category = interpolate.interpn(grid_coord, u_interp, category_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
v_category = interpolate.interpn(grid_coord, v_interp, category_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)
w_category = interpolate.interpn(grid_coord, w_interp, category_traj_points, method = 'linear', bounds_error=False, fill_value= np.nan)

# Helicity components.
x_helicity_category = u_category * xvort_category
y_helicity_category = v_category * yvort_category
z_helicity_category = w_category * zvort_category

# Horizontal helicity.
horiz_helicity_category = x_helicity_category + y_helicity_category
# Full 3D helicity.
helicity_3d_category = x_helicity_category + y_helicity_category + z_helicity_category

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get components of just positive vorticity entering the mesocyclone.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Positive vorticity for the whole set of trajectories.
plus_x_full = xvort_full[np.argwhere(xvort_full >= 0.)[:,0]]
plus_y_full = yvort_full[np.argwhere(yvort_full >= 0.)[:,0]]
plus_z_full = zvort_full[np.argwhere(zvort_full >= 0.)[:,0]]

# Positive vorticity for the parcel category. 
plus_x_cat = xvort_category[np.argwhere(xvort_category >= 0.)[:,0]]
plus_y_cat = yvort_category[np.argwhere(yvort_category >= 0.)[:,0]]
plus_z_cat = zvort_category[np.argwhere(zvort_category >= 0.)[:,0]]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get full set of trajectories that are just part of the mesocyclone.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
meso_indices = get_meso_indices(ds, xpos_full, ypos_full, zpos_full, x_coord, y_coord, x_coord_stag, y_coord_stag)
# Get components of vorticity entering the mesocyclone.
xvort_meso = xvort_full[meso_indices]
yvort_meso = yvort_full[meso_indices]
zvort_meso = zvort_full[meso_indices]

# Positive vorticity in mesocyclone trajectories.
plus_xvort_meso = xvort_meso[np.argwhere(xvort_meso >= 0.)[:,0]]
plus_yvort_meso = yvort_meso[np.argwhere(yvort_meso >= 0.)[:,0]]
plus_zvort_meso = zvort_meso[np.argwhere(zvort_meso >= 0.)[:,0]]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the percentage of vorticity that comes from this category.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Individual vorticity components.
x_percent = 100. * np.sum(xvort_category)/np.sum(xvort_full)
y_percent = 100. * np.sum(yvort_category)/np.sum(yvort_full)
z_percent = 100. * np.sum(zvort_category)/np.sum(zvort_full)

# Full horizontal vorticity.
horiz_percent = 100. * np.sum(horiz_category)/np.sum(horiz_full)
# Full 3D vorticity.
full3d_percent = 100. * np.sum(vort3d_category)/np.sum(vort3d_full)

# Individual helicity components.
x_helicity_percent = 100. * np.sum(x_helicity_category)/np.sum(x_helicity_full)
y_helicity_percent = 100. * np.sum(y_helicity_category)/np.sum(y_helicity_full)
z_helicity_percent = 100. * np.sum(z_helicity_category)/np.sum(z_helicity_full)

# Horizontal helicity.
horiz_helicity_percent = 100. * np.sum(horiz_helicity_category)/np.sum(horiz_helicity_full)
# Full 3D helicity.
helicity_3d_percent = 100. * np.sum(helicity_3d_category)/np.sum(helicity_3d_full)

# Positive vorticity-only percentages.
plus_x_percent = 100. * np.sum(plus_x_cat)/np.sum(plus_x_full)
plus_y_percent = 100. * np.sum(plus_y_cat)/np.sum(plus_y_full)
plus_z_percent = 100. * np.sum(plus_z_cat)/np.sum(plus_z_full)

plus_x_traj_percent = 100. * len(plus_x_cat)/len(plus_x_full)
plus_y_traj_percent = 100. * len(plus_y_cat)/len(plus_y_full)
plus_z_traj_percent = 100. * len(plus_z_cat)/len(plus_z_full)

# Mesocyclone-only percentages
x_meso_percent = 100. * np.sum(xvort_category)/np.sum(xvort_meso)
y_meso_percent = 100. * np.sum(yvort_category)/np.sum(yvort_meso)
z_meso_percent = 100. * np.sum(zvort_category)/np.sum(zvort_meso)

plus_x_meso_percent = 100. * np.sum(plus_x_cat)/np.sum(plus_xvort_meso)
plus_y_meso_percent = 100. * np.sum(plus_y_cat)/np.sum(plus_yvort_meso)
plus_z_meso_percent = 100. * np.sum(plus_z_cat)/np.sum(plus_zvort_meso)

meso_traj_percent = 100. * num_category_traj/len(meso_indices)

plus_x_meso_traj_percent = 100. * len(plus_x_cat)/len(plus_xvort_meso)
plus_y_meso_traj_percent = 100. * len(plus_y_cat)/len(plus_yvort_meso)
plus_z_meso_traj_percent = 100. * len(plus_z_cat)/len(plus_zvort_meso)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Print output to file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Convert list of categories to a string that can be printed out.
category_string = '{:s}'.format(parcel_category_arg).strip('[]').replace("'", "")

with open(outfile_name, 'w') as outfile:
    outfile.write('Percentages of the full trajectory dataset:\n')

    outfile.write('{:d} of {:d} ({:.1f} percent) of trajectories in ({:s}) region(s)\n'.format(num_category_traj, total_parcel_num, category_traj_percent, category_string))

    outfile.write('{:.1f} percent of E-W horizontal vorticity is from ({:s}) region(s)\n'.format(x_percent, category_string))
    outfile.write('{:.1f} percent of N-S horizontal vorticity is from ({:s}) region(s)\n'.format(y_percent, category_string))
    outfile.write('{:.1f} percent of vertical vorticity is from ({:s}) region(s)\n'.format(z_percent, category_string))

    outfile.write('{:.1f} percent of horizontal vorticity is from ({:s}) region(s)\n'.format(horiz_percent, category_string))
    outfile.write('{:.1f} percent of 3D vorticity is from ({:s}) region(s)\n'.format(full3d_percent, category_string))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    outfile.write('\n')

    outfile.write('{:.1f} percent of E-W horizontal helicity is from ({:s}) region(s)\n'.format(x_helicity_percent, category_string))
    outfile.write('{:.1f} percent of N-S horizontal helicity is from ({:s}) region(s)\n'.format(y_helicity_percent, category_string))
    outfile.write('{:.1f} percent of vertical helicity is from ({:s}) region(s)\n'.format(z_helicity_percent, category_string))

    outfile.write('{:.1f} percent of horizontal helicity is from ({:s}) region(s)\n'.format(horiz_helicity_percent, category_string))
    outfile.write('{:.1f} percent of 3D helicity is from ({:s}) region(s)\n'.format(helicity_3d_percent, category_string))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    outfile.write('\n')

    outfile.write('{:d} of {:d} ({:.1f} percent) of positive E-W horizontal vorticity trajectories from ({:s}) region(s)\n'.format(len(plus_x_cat), len(plus_x_full), plus_x_traj_percent, category_string))
    outfile.write('{:d} of {:d} ({:.1f} percent) of positive N-S horizontal vorticity trajectories from ({:s}) region(s)\n'.format(len(plus_y_cat), len(plus_y_full), plus_y_traj_percent, category_string))
    outfile.write('{:d} of {:d} ({:.1f} percent) of positive vertical vorticity trajectories from ({:s}) region(s)\n'.format(len(plus_z_cat), len(plus_z_full), plus_z_traj_percent, category_string))

    outfile.write('{:.1f} percent of positive E-W horizontal vorticity is from ({:s}) region(s)\n'.format(plus_x_percent, category_string))
    outfile.write('{:.1f} percent of positive N-S horizontal vorticity is from ({:s}) region(s)\n'.format(plus_y_percent, category_string))
    outfile.write('{:.1f} percent of positive vertical vorticity is from ({:s}) region(s)\n'.format(plus_z_percent, category_string))

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    outfile.write('\n')
    outfile.write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    outfile.write('Percentages of mesocyclone trajectories only:\n')

    outfile.write('{:d} of {:d} ({:.1f} percent) of trajectories from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(num_category_traj, len(meso_indices), meso_traj_percent, category_string))
    outfile.write('{:d} of {:d} ({:.1f} percent) of positive E-W horizontal vorticity trajectories from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(len(plus_x_cat), len(plus_xvort_meso), plus_x_meso_traj_percent, category_string))
    outfile.write('{:d} of {:d} ({:.1f} percent) of positive N-S horizontal vorticity trajectories from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(len(plus_y_cat), len(plus_yvort_meso), plus_y_meso_traj_percent, category_string))
    outfile.write('{:d} of {:d} ({:.1f} percent) of positive vertical vorticity trajectories from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(len(plus_z_cat), len(plus_zvort_meso), plus_z_meso_traj_percent, category_string))

    outfile.write('{:.1f} percent of E-W horizontal vorticity is from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(x_meso_percent, category_string))
    outfile.write('{:.1f} percent of N-S horizontal vorticity is from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(y_meso_percent, category_string))
    outfile.write('{:.1f} percent of vertical vorticity is from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(z_meso_percent, category_string))

    outfile.write('{:.1f} percent of positive E-W horizontal vorticity is from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(plus_x_meso_percent, category_string))
    outfile.write('{:.1f} percent of positive N-S horizontal vorticity is from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(plus_y_meso_percent, category_string))
    outfile.write('{:.1f} percent of positive vertical vorticity is from ({:s}) region(s) as percent of total mesocyclone trajectories only\n'.format(plus_z_meso_percent, category_string))

