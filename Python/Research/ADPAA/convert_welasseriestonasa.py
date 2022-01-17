#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/convert_welasseriestonasa.py
#
# Name:
#   convert_welasseriestonasa.py
#
# Purpose:  convert time series data from the Michigan PI cloud chamber to the
#           UND/NASA format that can be plotted with cplot.
#
# Syntax:
#   python convert_welasseriestonasa.py file_name
#
# Input Files: directory should contain .txt files containing time series data
#              collected by the Welas instrument.
#
# Execution Example:
#   Linux example: python convert_welasseriestonasa.py 20180620_AgI_neg11C_1_droplets_10sec.txt
#                  Creates "20180620_AgI_neg11C_1_droplets_10sec.raw"
#
# Modification History:
#   2018/12/13 - Lance Wilson:  Created.
#
# Copyright Dave Delene, Lance Wilson 2018
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
#

import numpy as np
import re
import sys
import time

from adpaa import ADPAA

def help_message():
    print 'Syntax : python convert_welasseriestonasa.py file_name'
    print 'Example: python convert_welasseriestonasa.py 20180620_AgI_neg11C_1_droplets_10sec.txt'
    print '         produces file called "20180620_AgI_neg11C_1_droplets_10sec.raw"'

for param in sys.argv:
    if param.startswith('-h') or param.startswith('--help'):
        help_message()
        exit()

if len(sys.argv) > 1:
    file_name = sys.argv[1]
else:
    help_message()
    exit()

welas_obj = ADPAA()

# Get the date data was collected, the frequency of the data, and an output
#   file name from the original file name.
match = re.search('((\w+_)+(\d+)sec).txt', file_name)
if match:
    output_name = match.group(1) + '.raw'
    file_name_date = match.group(2).split('_')[0]
    # Get the frequency of the data.
    data_interval = float(match.group(3))
    # Format the date the data was collected into the ADPAA format.
    file_date = '{:4d} {:02d} {:02d}'.format(int(file_name_date[0:4]), int(file_name_date[4:6]), int(file_name_date[6:]))
else:
    print 'File date or data interval could not be calculated from file name.'
    exit()

# Get time, N analyzed, N total, and Sum concentration.
file_data = np.genfromtxt(file_name, skip_header = 1, usecols = (0, 8, 9, 15))
column_num = len(file_data[0])

# Variables that need to be set: NV, VUNITS, VNAME, SNAME, MNAME, VMISS, data, VDESC
welas_obj.ORG = 'Michigan Technological University'
welas_obj.SNAME = 'Cloud Chamber Lab'
welas_obj.MNAME = 'Flare Testing'

welas_obj.XNAME = 'Time [seconds]; seconds from the starting time of the file'

# Short variable names.
welas_obj.VDESC = ['Time', 'NAnalyzed', 'NTotal', 'Sum_dCn']
# Long variable names.
welas_obj.VNAME = ['N Analyzed (#)', 'N Total (#)', 'Sum (dCn) (#/cm^3)']
# Unit names.
welas_obj.VUNITS = ['seconds', '#', '#', '#/cm^3']

for i in range(0, len(welas_obj.VDESC)):
    # The data dictionary must have keys that contain the columns of the data.
    welas_obj.data[welas_obj.VDESC[i]] = file_data[:,i]

# Missing values for the non-time values.
welas_obj.VMISS = ['999999.9999'] * (column_num - 1)
# Number of data columns.
welas_obj.NV = column_num

welas_obj.VFREQ  = '{:.3f} Hz Data'.format(1/data_interval)

# Date the data was collected.
welas_obj.DATE = file_date
# Date the NASA/UND file was created.
welas_obj.RDATE  = (time.strftime("%Y %m %d"))

welas_obj.name = output_name
welas_obj.WriteFile()
