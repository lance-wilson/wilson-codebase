#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/python_lib/tempdiff_calc.py
#
# Name:
#   tempdiff_calc.py
#
# Purpose:
#   Use a best fit line of supersaturation percentage vs. temperature
#   difference (calculated by line_calc function) at the defined temperature
#   to find the required temperature difference to produce a given
#   supersaturation percentage between the top and bottom plates.
#
# Syntax:
#   From Windows Command Prompt:
#       1. tempdiff_calc.py    (no command-line arguments ONLY)
#       2. python tempdiff_calc.py [arg1] [arg2]
#
#   From Bash:
#       1. ./tempdiff_calc.py [arg1] [arg2]
#       2. python tempdiff_calc.py [arg1] [arg2]
#
#   Input:
#       arg1 - top_temp: Top plate temperature to calculate a
#              temperature difference for (degrees C) (default 20.0 C)
#       arg2 - sspercent: The supersaturation percentage to find a temperature
#              difference for (default is 1.0%)
#
#   Output:
#       Print out of numerical value of bottom plate temperature.
#
# Execution example:
#   python tempdiff_calc.py 29.388 1.0257
#   Gives:
#   24.2007
#
# Modification History:
#   2015/12/01 - Lance Wilson: Written.
#   2016/01/13 - Lance Wilson: Added comments
#   2016/02/01 - Lance Wilson: Modified comments
#   2016/02/19 - Lance Wilson: Accommodated changes in line_calc
#   2016/02/29 - Lance Wilson: Improved the accuracy of range_max with if-else
#                              structure, error handling for improper min and
#                              max temperatures
#   2016/03/30 - Lance Wilson: Added comments, added suppport for command-line
#                              arguments
#   2016/04/04 - Lance Wilson: Added comments, added error-checking
#   2016/04/18 - Lance Wilson: Added comments, added loop to line_calc
#                              calculations, changed precision in print out
#                              of data
#   2016/04/20 - Lance Wilson: Modified comments, modified default variables,
#                              modified temperature difference equation
#   2016/04/27 - Lance Wilson: Added help message
#   2016/05/23 - Lance Wilson: Modified input and output of program, comments
#   2016/05/24 - David Delene: Changed output syntax.
#   2016/06/09 - Lance Wilson: Removed unnecessary code in help message block,
#                              modified comments.
#
# Verification of Data:
#   Data has been verified by comparison with ADPAA ccn2conc module, which
#   calculates the CCN concentration based on CN counts and flow rates
#   (source: http://adpaa.sourceforge.net/wiki/index.php/.:uwyoccnc:LabM200)
#
# Copyright 2016 David Delene
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

import math
import numpy as np
from line_calc import line_calc
import sys

# Set the top plate temperature in Kelvin (default 293.15 K)
top_temp = 293.15
# Set the supersaturation percentage (default = 1.0)
sspercent = 1.0
# Variable for number of arguments
num_args = len(sys.argv)

# Help message
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h')):
        print 'Syntax: python tempdiff_calc.py -h [top_temp] [sspercent]\n'
        print ('Purpose: Calculates the bottom plate temperature (degrees C) '
               'given a top plate temperature (degrees C) and supersaturation '
               'percentage\n')
        print ('-h Provide syntax of command.')
        print ('top_temp - Top plate temperature for which to '
               'calculate a temperature difference (degrees C) (default 20.0 C)')
        print ('sspercent - The supersaturation percentage for which '
               'to find a temperature difference (default is 1.0%)\n')
        quit()

# If user enters no command line arguments
if (num_args < 2):
    if (sys.platform.startswith('win')): # Check for Windows OS
        print ('Warning: must use "python tempdiff_calc.py" for command'
               '-line arguments in Windows\n')

# If user enters just top plate temperature
elif (num_args == 2):
    top_temp = float(sys.argv[1])+273.15

# If user enters top plate temperature and supersaturation percent
else:
    top_temp = float(sys.argv[1])+273.15
    sspercent = float(sys.argv[2])

# Calculate slope and intercept of best-fit line at this top plate temp
slope, intercept = line_calc(top_temp)

# Calculate the top plate temperature in celsius
top_temp_C = top_temp-273.15
# Calculate the temperature difference from the best fit line data.
temp_diff = math.exp((slope * math.log(sspercent)) + intercept)
# Calculate the bottom plate temperature.
bottom_temp = top_temp_C - temp_diff
print '%.4f' % bottom_temp
# End of Program
