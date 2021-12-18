#!/usr/bin/env python3
#
# Name:
#   new_writeout_exact_initialization.py
#
# Purpose:  Use trajectory position arrays to create text that can be pasted
#           into writeout.F
#
# Syntax: python3 new_writeout_exact_initialization.py v5_meso_tornadogenesis
#
#   Input: Back trajectory numpy archive, named "backtraj_(parcel_label).npz"
#
# Execution Example:
#   python3 new_writeout_exact_initialization.py v5_meso_tornadogenesis
#
# Modification History:
#   2021/02/26 - Lance Wilson:  Created
#   2021/09/08 - Lance Wilson:  Began modification to run on any back
#                               trajectory parcel file.
#

import itertools
import numpy as np
#import random
import sys

if len(sys.argv) > 1:
    # Label of back trajectory parcel file.
    parcel_label = sys.argv[1]
else:
    print('Parcel label was not specified.')
    print('Syntax: python3 new_writeout_exact_initialization.py parcel_label')
    print('Example: python3 new_writeout_exact_initialization.py v5_meso_tornadogenesis')
    sys.exit()

version_number = 'v5'

archive_dir = 'back_traj_npz_{:s}/'.format(version_number)
output_dir = '75m_100p_{:s}/back_traj_verify/'.format(version_number)

# Number of parcels used in CM1 model; also the number of samples to take from
#   random.sample() function
cm1_parcel_num = 100

# Model height level below which trajectory data is no longer safe to use
#   (generally the height of the lowest non-boundary w point).
min_usable_z_height = 30.

minutes_integrated_back = 10
output_freq_sec = 10

seconds_integrated_back = 60 * minutes_integrated_back
array_index = int((seconds_integrated_back/output_freq_sec)-1)

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
index4 = np.argwhere(init_zpos >= min_usable_z_height)

# Find indices that are in all four of the above arrays.
intersection1 = np.intersect1d(index1, index2)
intersection2 = np.intersect1d(index3, index4)
valid_indices = np.intersect1d(intersection1, intersection2)

if len(valid_indices) < cm1_parcel_num:
    print('Not enough valid indices')
    exit()
# Get a pseudo-random sample of indices from the set of valid indices.
#   k is the number of samples, drawn without replacement.
#test_indices = np.array(sorted(random.sample(list(valid_indices), k=cm1_parcel_num)))
test_indices = sorted(np.random.choice(valid_indices, cm1_parcel_num, replace=False))

# New arrays containing the values at the set of sampled indices.
xpos = init_xpos[test_indices]
ypos = init_ypos[test_indices]
zpos = init_zpos[test_indices]

# Stack arrays for easier print loop.
pos = np.stack((xpos,ypos,zpos))

# Print out the code to be pasted into writeout.F
with open(output_dir + 'writeout_positions_{:s}.txt'.format(parcel_label), "a") as outfile:
    for i,j in itertools.product(range(1,4), range(1,cm1_parcel_num+1)):
        print('        pdata({:d},{:d}) = {:f}'.format(i, j, pos[i-1,j-1]), file=outfile)

# Adding 0 to the file value to make sure that the output is an integer.
file_num_offset = traj_data['offset'] + 0

out_file_num_offset = file_num_offset + len(traj_data['xpos'])

out_xpos = traj_data['xpos'][0]
out_ypos = traj_data['ypos'][0]
out_zpos = traj_data['zpos'][0]

np.savez(output_dir + 'back_verify_back_{:s}'.format(parcel_label), xpos=out_xpos, ypos=out_ypos, zpos=out_zpos, offset=out_file_num_offset, indices=test_indices)

