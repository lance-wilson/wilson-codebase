#!/usr/bin/env python3
#
# Name:
#   calc_file_num_offset.py
#
# Purpose:  Calculate a suggested starting file for when CM1 trajectories
#           were initialized during a particular model run to ensure trajectory
#           and contour plots are time-matched.
#
# Syntax:
#   Forward traj.:
#       python calc_file_num_offset.py version_number parcel_id_num
#   Back traj.:
#       python3 calc_file_num_offset.py version_number parcel_start_time
#
#   Input:
#
# Execution Example:
#   Forward traj.:  python calc_file_num_offset.py v4 9
#   Back traj.:     python calc_file_num_offset.py v5 6200
#
# Modification History:
#   2021/03/05 - Lance Wilson:  Script to suggest a file_num_offset for the
#                               forward trajectories based on the start time of
#                               trajectory integration (in namelist).
#   2021/10/21 - Lance Wilson:  Adding check so that code can calculate back
#                               trajectory file_calc_start values using an
#                               input time for parcel_id_num.
#

import numpy as np
import sys

def help_message():
    print('Syntax (forward traj.): python3 calc_file_num_offset.py version_number parcel_id_num')
    print('Example (forward traj.): python calc_file_num_offset.py v4 9')
    print('Syntax (back traj.): python3 calc_file_num_offset.py version_number parcel_start_time')
    print('Example (back traj.): python calc_file_num_offset.py v5 6200')
    print('Currently supported version numbers: v3, 10s, v4, v5')
    sys.exit()

def calc_file_offset(version, parcel_start_time):
    if version == 'v3':
        transition_time = 0.
        transition_file = 1
        output_freq = 60.
    elif version == '10s':
        transition_time = 6000.
        transition_file = 1 if parcel_start_time <= transition_time else 101
        output_freq = 60. if parcel_start_time <= transition_time else 10.
    elif version == 'v4':
        transition_time = 3600.
        transition_file = 1 if parcel_start_time <= transition_time else 61
        output_freq = 60. if parcel_start_time <= transition_time else 10.
    elif version == 'v5':
        transition_time = 4800.
        transition_file = 1 if parcel_start_time <= transition_time else 81
        output_freq = 60. if parcel_start_time <= transition_time else 10.
    else:
        print('Version number not found')
        help_message()
    return int(((parcel_start_time-transition_time)/output_freq) + transition_file)

if __name__ == '__main__':
    if len(sys.argv) > 2:
        version = sys.argv[1]
        parcel_id = sys.argv[2]
    else:
        print('Version number or Parcel data file was not specified.')
        help_message()

    # Location of namelist file (for forward trajectories).
    namelist_dir = '75m_100p_{:s}/namelists/'.format(version)
    namelist_filename = namelist_dir + 'namelist_{:s}.input'.format(parcel_id)

    try:
        # Look at the namelist.input file to get the parcel initialization time.
        with open(namelist_filename, 'r') as namelist_file:
            namelist_lines = namelist_file.readlines()
            for line in namelist_lines:
                line = line.strip()
                if line.startswith('var2'):
                    line = line.replace(',','')
                    line = line.split('=')
                    parcel_start_time = int(float(line[-1]))
    # If there is no namelist file, then assume that a back trajectory
    #   initialization time has been entered.
    except IOError:
        parcel_start_time = float(parcel_id)

    file_num_offset = calc_file_offset(version, parcel_start_time)

    print('Suggested file_num_offset: {:d}'.format(file_num_offset))
