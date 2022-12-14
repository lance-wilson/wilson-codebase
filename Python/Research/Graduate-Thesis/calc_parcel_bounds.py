#!/usr/bin/env python3
#
# Name:
#   calc_parcel_bounds.py
#
# Purpose:  Calculate the indices used as boundaries to the subset of data
#           written to a vorticity budget output file.
#
# Syntax: from calc_parcel_bounds import calc_boundaries
#         x1, y1, z1, x2, y2, z2 = calc_boundaries(version_number, bound_buffer)
#
#         python3 calc_parcel_bounds.py version_number, bound_buffer
#
# Input:  CM1 Model version number (see README_Model_Version_Descriptions.txt)
#         Number of grid points to use as a buffer around the outer edge of the
#         sub-domain (integer)
#
# Execution Example:
#   x1, y1, z1, x2, y2, z2 = calc_boundaries('v5', 5)
#   python3 calc_parcel_bounds.py v5 5
#
# Modification History:
#   2021/09/30 - Lance Wilson:  Created, splitting off code from
#                               calc_vort_budget.py to calculate boundaries
#                               based on back trajectory files that will also
#                               be used in calc_vort_equation.py.
#   2022/02/04 - Lance Wilson:  Updated comments for calc_bound_index function.
#

from netCDF4 import Dataset
import glob
import numpy as np
import sys

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the index to use as a boundary value in the vorticity budget output file.
#   Arguments:
#       coord: locations of model grid points
#       position: location of point to calculate index from
#       bound_buffer: integer to add to the index to include a buffer zone
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_bound_index(coord, position, bound_buffer=0):
    # Calculate the difference between the minimum or maximum position and each
    #   grid point value (in meters).
    pos_diff = np.abs(coord - position)
    # Find where the smallest difference occurs.
    pos_index = np.argwhere(pos_diff == np.min(pos_diff))[0,0]
    # Add a buffer to the value, and clip to the maximum model dimensions.
    return np.clip(pos_index + bound_buffer, 0, len(coord))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the boundaries in meters and retrieve the coordinate positions that
#   are used to calculate the indices used as boundaries to the subset of data
#   written to the vorticity budget output file.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_boundaries(version_number, bound_buffer=0):
    back_traj_dir = 'back_traj_npz_{:s}/'.format(version_number)
    model_dir = '75m_100p_{:s}/'.format(version_number)

    # Output file number that is the beginning of the higher resolution
    #   temporal CM1 output.
    if version_number == '10s':
        high_res_time = 101
    elif version_number == 'v4':
        high_res_time = 61
    elif version_number == 'v5':
        high_res_time = 81

    # Get a list of all back trajectory numpy archives.
    parcel_file_list = glob.glob(back_traj_dir + '*.npz')

    # Both CM1 and this code assume that the coordinate grid positions will
    #   remain constant throughout the model run, so opening the first
    #   available file alone is sufficient to get the x, y, and z coordinate
    #   positions.
    ds = Dataset(glob.glob(model_dir + 'JS_75m_run*_000*.nc')[0])

    # Get staggered coordinates for the wind data, converted from kilometers to
    #   meters.
    stagger_x_coord = np.copy(ds.variables['xf'])*1000.
    stagger_y_coord = np.copy(ds.variables['yf'])*1000.
    stagger_z_coord = np.copy(ds.variables['zf'])*1000.
    # Get unstaggered coordinates for thermodynamic variables, converted from
    #   kilometers to meters.
    x_coord = np.copy(ds.variables['xh'])*1000.
    y_coord = np.copy(ds.variables['yh'])*1000.
    z_coord = np.copy(ds.variables['z'])*1000.

    ds.close()

    # Intitial minimum values will be the maximum value in the model grid.
    x_min = np.max([np.max(stagger_x_coord), np.max(x_coord)])
    y_min = np.max([np.max(stagger_y_coord), np.max(y_coord)])
    # Intitial maximum values will be the minimum value in the model grid.
    x_max = np.min([np.min(stagger_x_coord), np.min(x_coord)])
    y_max = np.min([np.min(stagger_y_coord), np.min(y_coord)])
    z_max = np.min([np.min(stagger_z_coord), np.min(z_coord)])

    # Calculate the minimum and maximum bounds of the data in the vorticity
    #   budget output file using the locations of all back trajectory datasets
    #   for this model version.
    for parcel_file in parcel_file_list:
        # Load data from uncompressed numpy archive.
        traj_data = np.load(parcel_file)
        # Adding 1 to the file value to match the CM1 model file number.
        file_num_offset = traj_data['offset'] + 1

        # For data that has is integrated back into the lower temporal
        #   resolution output, calculate an upper-bound index so that only data
        #   within the higher resolution output is used.
        # If all of the data is in the higher resolution output, the resulting
        #   limit will be greater than the size of the back trajectory data,
        #   which will return the full array.
        high_res_limit_index = len(traj_data['xpos']) - (high_res_time - file_num_offset)

        xpos = traj_data['xpos'][:high_res_limit_index]
        ypos = traj_data['ypos'][:high_res_limit_index]
        zpos = traj_data['zpos'][:high_res_limit_index]

        # New minimum will be the minimum between the old value and the current
        #   dataset's minimum.
        x_min = np.min([x_min, np.nanmin(xpos)])
        y_min = np.min([y_min, np.nanmin(ypos)])
        # New maximum will be the maximum between the old value and the current
        #   dataset's maximum.
        x_max = np.max([x_max, np.nanmax(xpos)])
        y_max = np.max([y_max, np.nanmax(ypos)])
        z_max = np.max([z_max, np.nanmax(zpos)])

    # Get the indices where the minimum trajectory values are located.
    x1 = calc_bound_index(x_coord, x_min, -1 * bound_buffer)
    y1 = calc_bound_index(y_coord, y_min, -1 * bound_buffer)
    # Skipping z_min calculation because it is probably close to 0.
    z1 = 0

    # Get the indices where the maximum trajectory values are located.
    x2 = calc_bound_index(x_coord, x_max, bound_buffer)
    y2 = calc_bound_index(y_coord, y_max, bound_buffer)
    z2 = calc_bound_index(z_coord, z_max, bound_buffer)

    return (x1, y1, z1, x2, y2, z2)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# If run as main program, will print out the boundaries that are used for a
#   particular model version and buffer.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if __name__ == '__main__':
    if len(sys.argv) > 2:
        # Model run that is being used.
        version_number = sys.argv[1]
        bound_buffer = int(sys.argv[2])
    else:
        print('Model version number or buffer size was not specified.')
        print('Syntax: python3 calc_parcel_bounds.py model_version buffer')
        print('Example: python3 calc_parcel_bounds.py v5 5')
        print('Currently supported version numbers: 10s, v4, v5')
        sys.exit()

    if version_number == 'v3':
        print('Version number is not valid.')
        print('Currently supported version numbers: 10s, v4, v5')
        sys.exit()

    x1, y1, z1, x2, y2, z2 = calc_boundaries(version_number, bound_buffer)

    print('Min. Indices (x y z): ', x1, y1, z1)
    print('Max. Indices (x y z): ', x2, y2, z2)

