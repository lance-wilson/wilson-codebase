#!/usr/bin/env python3
#
# Name:
#   writeout_initialization_parcels.py
#
# Purpose:  Use trajectory position arrays to create text that can be pasted
#           into writeout.F.  If there are fewer usable points than desired,
#           points will be created between close pairs of points to fill the
#           rest of the array.  If there are more points desired, a pseudo-
#           random subset of points will be selected from the original set of
#           trajectories.
#
# Syntax: 
#   python3 writeout_initialization_parcels.py version_number parcel_label
#
#   Input: Back trajectory numpy archive, named "backtraj_(parcel_label).npz"
#
#   Output: Text file named "writeout_positions_1000parcels_(parcel_label).txt"
#           containing parcel positions that can be pasted into writeout.F
#
# Execution Example:
#   python3 writeout_initialization_parcels.py v5 v5_meso_tornadogenesis
#
# Modification History:
#   2021/02/26 - Lance Wilson:  Created
#   2021/09/08 - Lance Wilson:  Began modification to run on any back
#                               trajectory parcel file.
#   2022/02/17 - Lance Wilson:  Modification of new_writeout_exact_initialization
#                               to create 1000 parcel starting points to run
#                               forward in CM1 from sets of back trajectories.
#   2022/11/12 - Lance Wilson:  Fixed bug that caused duplicate points in the
#                               final output.
#

import itertools
import numpy as np
import sys

if len(sys.argv) > 2:
    version_number = sys.argv[1][-1]
    # Label of back trajectory parcel file.
    parcel_label = sys.argv[2]
else:
    print('Parcel label was not specified.')
    print('Syntax: python3 writeout_initialization_parcels.py version_number parcel_label')
    print('Example: python3 writeout_initialization_parcels.py v5 v5_meso_tornadogenesis')
    sys.exit()

archive_dir = 'back_traj_npz_v{:s}/'.format(version_number)
output_dir = '75m_100p_{:s}/parcel_analysis/'.format(version_number)

# Number of parcels to be used in CM1 model.
cm1_parcel_num = 1000

# Model height level below which trajectory data is no longer safe to use
#   (generally the height of the lowest non-boundary w point).
min_usable_z_height = 30.

minutes_integrated_back = 10
output_freq_sec = 10

seconds_integrated_back = 60 * minutes_integrated_back
array_index = int((seconds_integrated_back/output_freq_sec)-1)

# Set pseudorandom seed to be able to reproduce randomly selected indices.
np.random.seed(279)

# Load data from uncompressed numpy archive.
traj_data = np.load(archive_dir + 'backtraj_{:s}.npz'.format(parcel_label))
init_xpos = traj_data['xpos'][array_index]
init_ypos = traj_data['ypos'][array_index]
init_zpos = traj_data['zpos'][array_index]

# Get indices of values that are not nan in the x, y, and z position arrays.
#   np.isfinite() checks for both NAN and INF, which is fine for this purpose.
index1 = np.argwhere(np.isfinite(init_xpos))
index2 = np.argwhere(np.isfinite(init_ypos))
index3 = np.argwhere(np.isfinite(init_zpos))
# Get indices of values that are above the minimum usable z height threshold.
index4 = np.argwhere(np.min(traj_data['zpos'][:array_index+1], axis=0) >= min_usable_z_height)

# Find indices that are in all four of the above arrays.
intersection1 = np.intersect1d(index1, index2)
intersection2 = np.intersect1d(index3, index4)
valid_indices = np.intersect1d(intersection1, intersection2)

# Number of valid trajectories used from the original set of trajectories.
valid_original_values = len(valid_indices)

# Number of values that must be created via interpolation.
created_values = cm1_parcel_num - valid_original_values

# New arrays containing the values at the set of sampled indices.
orig_xpos = init_xpos[valid_indices]
orig_ypos = init_ypos[valid_indices]
orig_zpos = init_zpos[valid_indices]

orig_pos = np.stack((orig_xpos,orig_ypos,orig_zpos))

# If the number of output parcels is less than the number of trajectories
#   available, some interpolation is required.
if valid_original_values < cm1_parcel_num:
    # Array to store extra points created by interpolation.
    new_points = np.zeros((3,created_values))

    values_left_to_create = created_values

    # Choose the 1st, 2nd, etc. nearest on each iteration so that the same
    #   points are calculated in multiple iterations.
    nth_nearest_point = 1
    values_created_so_far = 0

    while values_left_to_create > 0:
        if valid_original_values >= values_left_to_create:
            values_created_this_time = values_left_to_create
        else:
            values_created_this_time = cm1_parcel_num - values_left_to_create -values_created_so_far

        # Get a pseudo-random sample of indices from the set of valid indices.
        created_indices = sorted(np.random.choice(range(valid_original_values), values_created_this_time, replace=False))

        values_skipped = 0

        for i, created_index in enumerate(created_indices):
            # Pseudo-randomly selected point.
            point = orig_pos[:,created_index]

            # Find the closest points by Euclidean distance (square root
            #   calculation is not needed since only the relative distance
            #   matters).
            sum_squares = np.sum(np.square(orig_pos - point.reshape((3,1))), axis=0)
            # Index of the nth nearest point.
            nearest_point_index = np.argwhere(sum_squares == sorted(sum_squares)[nth_nearest_point])[0,0]

            nearest_point = orig_pos[:,nearest_point_index]

            # Create a new point halfway between the original point and the
            #   nth nearest point.
            new_point = np.mean((point, nearest_point), axis=0)

            x_bool = True if new_point[0] in new_points[0,:] else False
            y_bool = True if new_point[1] in new_points[1,:] else False
            z_bool = True if new_point[2] in new_points[2,:] else False
            if x_bool and y_bool and z_bool:
                values_skipped += 1
            else:
                new_points[:,i+values_created_so_far-values_skipped] = new_point

        nth_nearest_point += 1
        values_left_to_create -= (values_created_this_time - values_skipped)
        values_created_so_far += (values_created_this_time - values_skipped)

        if nth_nearest_point > (valid_original_values/2.):
            print('Unable to produce new unique points. Output will be incomplete.')
            break

    full_pos = np.concatenate((orig_pos, new_points), axis=1)
# If there are more valid trajectories than are required, select a
#   pseudo-random subset of them.
elif valid_original_values > cm1_parcel_num:
    # Get a pseudo-random sample of indices from the set of valid indices.
    selected_indices = sorted(np.random.choice(valid_indices, cm1_parcel_num, replace=False))
    full_pos = orig_pos[:,selected_indices]
# If the number of valid trajectories is the same number of output values, the
#   original positions can be used.
else:
    full_pos = orig_pos

# Print out the code to be pasted into writeout.F
with open(output_dir + 'writeout_init_positions_parcels_{:s}.txt'.format(parcel_label), "w") as outfile:
    for i,j in itertools.product(range(1,4), range(1,cm1_parcel_num+1)):
        print('        pdata({:d},{:d}) = {:f}'.format(i, j, full_pos[i-1,j-1]), file=outfile)

