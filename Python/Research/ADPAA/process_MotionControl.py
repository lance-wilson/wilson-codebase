#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/process_MotionControl.py
#
# Name:
#   process_MotionControl.py
#
# Purpose:
#   To subset the Thorlabs Motion Control log file to only contain "Position"
#   line information.
#
# Syntax:
#   python process_MotionControl.py
#
#   Input: Thorlabs motion control log file.
#
#   Output: A subsetted file of the original log file.
#
# Execution Example:
#   Linux example: python process_MotionControl Thorlabs.MotionControl_und28.log
#
# CALLS:
#   Nothing.
#
# Modification History:
#   2017/05/29 - David Delene <delene@aero.und.edu>: Written
#   2017/06/12 - Lance Wilson:  Rewritten.
#   2017/06/13 - Lance Wilson:  Updated header comments.
#   2017/06/14 - Lance Wilson:  Updated help message conditions.
#   2017/07/18 - Lance Wilson:  Added verification of data, added comments.
#
# Verification of Data:
#   Ran both this program and the original process_MotionControl script located
#   in the scripts directory of ADPAA.  The cmp command was then used to
#   compare both files, and the result was that the content of the files was
#   identical.
#  
# Copyright 2017 Lance Wilson, David Delene
#
# This program is distributed under the terms of the GNU General Public License
#
# This file is part of Airborne Data Processing and Analysis (ADPAA).
#
# ADPAA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADPAA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADPAA.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys

def help_message():
    print 'SYNTAX:  python process_MotionControl inputfile'
    print '  inputfile - The Thorlabs Motion Control log file.'
    print '  Example:  process_MotionControl Thorlabs.MotionControl_und28.log'
    exit()

# Terminate execution if there isn't the proper number of arguments.
if (len(sys.argv) != 2):
  help_message()

for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') | sys.argv[x].endswith('help')):
        help_message()

# Open the log file, and create a name for the subsetted file.
logfile = open(sys.argv[1], 'r')
outfilename = sys.argv[1] + '.subsetted'

position_line = []
for line in logfile:
    # Remove lines containing "Position"
    if (re.search(', Position: ', line)):
        position_line.append(line)

moving_removed = []
for match in position_line:
    # Remove lines containing "Moving"
    if not (re.search('Moving', match)):
        moving_removed.append(match)

calibrated_removed = []
for match in moving_removed:
    # Remove lines containing "Calibrated"
    if not (re.search('Calibrated', match)):
        calibrated_removed.append(match)

original_removed = []
for match in calibrated_removed:
    # Remove lines containing "Original"
    if not (re.search('Original', match)):
        original_removed.append(match)

m_limitSwitchParams_removed = []
for match in original_removed:
    # Remove lines containing "m_limitSwitchParams"
    if not (re.search('m_limitSwitchParams', match)):
        m_limitSwitchParams_removed.append(match)

MoveToPosition_removed = []
for match in m_limitSwitchParams_removed:
    # Remove lines containing "MoveToPosition"
    if not (re.search('MoveToPosition', match)):
        MoveToPosition_removed.append(match)

Information_removed = []
for match in MoveToPosition_removed:
    # Remove lines containing "Information"
    if not (re.search('Information', match)):
        Information_removed.append(match)

Final_Subset = []
for match in Information_removed:
    # Remove lines containing "Position Limits"
    if not (re.search('Position Limits', match)):
        Final_Subset.append(match)

logfile.close()

outfile = open(outfilename, 'w')

# Print the final matches to the subsetted file.
for match in Final_Subset:
    outfile.write(match)

outfile.close()

print 'Finished creating ' + outfilename + ' file'
