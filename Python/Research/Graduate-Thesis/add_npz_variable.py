#!/usr/bin/env python3
#
# Name:
#   add_npz_variable.py
#
# Purpose:  Rewrite an .npz numpy archive to add a variable without having to
#           rerun the original parcel calculation.
#
# Syntax: python add_npz_variable.py parcel_label
#
#   Input:
#
# Execution Example:
#   python add_npz_variable.py downdraft
#
# Modification History:
#   2021/02/26 - Lance Wilson:  Created
#

import numpy as np
import sys

if len(sys.argv) > 1:
    # Label for output file name.
    parcel_label = sys.argv[1]
else:
    print('Variable to plot slice of was not specified.')
    print('Syntax: python3 add_npz_variable.py parcel_label')
    print('Example: python3 add_npz_variable.py downdraft')
    sys.exit()

# Load data from uncompressed numpy archive.
traj_data = np.load('back_traj_np/backtraj_{:s}.npz'.format(parcel_label))
xpos = traj_data['xpos']
ypos = traj_data['ypos']
zpos = traj_data['zpos']
# Adding 0 to the file value to make sure that the output is an integer.
file_num_offset = traj_data['offset'] + 0
parcel_dimensions = traj_data['parcel_dimension']

# Variable to add.
#parcel_dimensions = np.array((6,5,42))

# Save to numpy uncompressed archive for the plotting script.
np.savez('back_traj_np/backtraj_{:s}'.format(parcel_label), xpos=xpos, ypos=ypos, zpos=zpos, offset=file_num_offset, parcel_dimension=parcel_dimensions)

