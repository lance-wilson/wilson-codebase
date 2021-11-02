#!/usr/bin/env python3
#
# Name:
#   calc_back_traj_start_pos.py
#
# Purpose:  
#
# Syntax:
#   python3 calc_back_traj_start_pos.py left_index right_index number_of_points
#
# Execution Example:
#   python3 calc_back_traj_start_pos.py 390 445 10
#
# Output of Example:
#   Left Point: -5250
#   Increment: 458.33
#
# Modification History:
#   2021/09/01 - Lance Wilson:  Created.
#

import sys

if len(sys.argv) > 3:
    left_index = int(sys.argv[1])
    right_index = int(sys.argv[2])
    num_points = int(sys.argv[3])
else:
    print('Syntax: python3 calc_back_traj_start_pos.py left_index right_index number_of_points')
    print('Example: python3 calc_back_traj_start_pos.py 390 445 10')
    sys.exit()

center_point = 460
resolution = 75.

left_distance = (left_index - center_point) * resolution
right_distance = (right_index - center_point) * resolution
increment = (right_distance - left_distance)/(num_points - 1)

print('Left Point: {:d}'.format(int(left_distance)))
print('Increment: {:.2f}'.format(increment)) 

