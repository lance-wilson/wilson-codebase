#!/usr/bin/env python3
#
# Name:
#   meso_vort_source_percentage.py
#
# Purpose:  Calculate the percentage of vorticity entering the mesocyclone that
#           is from a particular source region (or regions).
#
# Syntax: python3 meso_vort_source_percentage.py version_number parcel_label parcel_category1[,parcel_category2...]
#
#   Input:
#
# Execution Example:
#   python3 meso_vort_source_percentage.py v5 v5_meso_tornadogenesis forward_flank,wraparound
#
# Modification History:
#   2022/01/28 - Lance Wilson:  Created.
#   2022/02/09 - Lance Wilson:  Added helicity calculations.

from back_traj_interp_class import Back_traj_ds
from categorize_traj_class import Cat_traj
from calc_parcel_bounds import calc_bound_index

from netCDF4 import MFDataset
from scipy import interpolate

import atexit
import numpy as np
import sys
import time

# Close the main CM1 model data netCDF file.
def closeNCfile(ds):
    ds.close()

mandatory_arg_num = 3

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    parcel_label = sys.argv[2]
    parcel_category_arg = sys.argv[3]
else:
    print('Variable to plot slice, parcel label, and version number must be specified.')
    print('Syntax: python3 meso_vort_source_percentage.py version_number parcel_label parcel_category1[,parcel_category2...]')
    print('Example: python3 meso_vort_source_percentage.py v5 v5_meso_tornadogenesis forward_flank,wraparound')
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
# Directory for output images.
output_dir = cat_dir + 'Images/'

# Time at which to evaluate vorticity.
analysis_time = 6200.

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
traj_time_index = np.argwhere(np.abs(simulation_times - analysis_time) == np.min(np.abs(simulation_times - analysis_time)))[0,0]

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
file_list = [model_dir + 'JS_75m_run{:d}_000{:03d}.nc'.format(run_number, file_num) for file_num in range(file_num_offset+1, file_num_offset+parcel_time_step_num+1)]
ds = MFDataset(file_list)

# Close the main CM1 data netCDF file when the program exits.
atexit.register(closeNCfile, ds)

# Coordinates of the unstaggered CM1 grid in each dimension (converted from
#   kilometers to meters).
x_coord = np.copy(ds.variables['xh'])*1000.
y_coord = np.copy(ds.variables['yh'])*1000.
z_coord = np.copy(ds.variables['z'])*1000.

# Model file number at the parcel initialization time.
model_time_step = parcel_time_step_num - traj_time_index - 1

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
# Get back trajectory data at the analysis time step for the category (or
#   categories) being analyzed.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Empty array to concatenate array of indices of categorized back trajectories.
category_indices = np.zeros((0), dtype=np.int)

for parcel_category in parcel_categories:
    # Trajectories to be plotted, based on intialization positions stored in a
    #   netCDF file created by categorize_trajectories.
    cat_traj_obj = Cat_traj(version_number, cat_dir, parcel_label, parcel_category)
    # It is possible that a file could be created without there being any data
    #   in it, so plots will only be attempted if the object's "existing_file"
    #   flag is true.
    if cat_traj_obj.existing_file:
        cat_traj_obj.open_file(parcel_category)
        # Initialization positions are converted to an array index.
        category_indices = np.concatenate((category_indices, cat_traj_obj.meters_to_trajnum(traj_ds_obj.xpos, traj_ds_obj.ypos, traj_ds_obj.zpos)))
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

# Convert list of categories to a string that can be printed out.
category_string = '{:s}'.format(parcel_category_arg).strip('[]').replace("'", "")

print('{:.1f} percent of trajectories in ({:s}) region(s)'.format(category_traj_percent, category_string))

print('{:.1f} percent of E-W horizontal vorticity is from ({:s}) region(s)'.format(x_percent, category_string))
print('{:.1f} percent of N-S horizontal vorticity is from ({:s}) region(s)'.format(y_percent, category_string))
print('{:.1f} percent of vertical vorticity is from ({:s}) region(s)'.format(z_percent, category_string))

print('{:.1f} percent of horizontal vorticity is from ({:s}) region(s)'.format(horiz_percent, category_string))
print('{:.1f} percent of 3D vorticity is from ({:s}) region(s)'.format(full3d_percent, category_string))

print('')

print('{:.1f} percent of E-W horizontal helicity is from ({:s}) region(s)'.format(x_helicity_percent, category_string))
print('{:.1f} percent of N-S horizontal helicity is from ({:s}) region(s)'.format(y_helicity_percent, category_string))
print('{:.1f} percent of vertical helicity is from ({:s}) region(s)'.format(z_helicity_percent, category_string))

print('{:.1f} percent of horizontal helicity is from ({:s}) region(s)'.format(horiz_helicity_percent, category_string))
print('{:.1f} percent of 3D helicity is from ({:s}) region(s)'.format(helicity_3d_percent, category_string))

