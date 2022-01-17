#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/convert_ndarbcontonasa.py
#
# Name:
#   convert_ndarbcontonasa.py
#
# Purpose:  convert the data from a North Dakota Agricultural Weather Network
#           (NDAWN) CSV file into the NASA/ADPAA format.
#
# Syntax:
#   python convert_ndawntonasa.py [file]
#
# Input Files: A .csv file containing rainfall data from NDAWN station(s).
#              Currently expects data columns in this order: Station Name,
#              Latitude, Longitude, Elevation, Year, Month, Day, Rainfall,
#              Rainfall Flag
#
# Execution Example:
#   Linux example: python convert_ndawntonasa.py ndawn_Bowman.csv
#                  Produces file called "1990_06_01-2018_08_29.rainfall.raw"
#
# Modification History:
#   2018/10/23 - Lance Wilson:  Created.
#   2018/11/09 - Lance Wilson:  Added output to file.
#   2018/11/10 - Lance Wilson:  Added comments.
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

import datetime
import math
import numpy as np
import os
import re
import sys
import time

from adpaa import ADPAA

def help_message():
    print 'Syntax : python convert_ndawntonasa.py [file]'
    print 'Example: python convert_ndawntonasa.py ndawn_Bowman.csv'
    print '         produces file called "1990_06_01-2018_08_29.rainfall.raw"'
    exit()

for param in sys.argv:
    if param.startswith('-h') or param.startswith('--help'):
        help_message()

if len(sys.argv) > 1:
    ndawn_file = sys.argv[1]
else:
    help_message()

ndawn_obj = ADPAA()
missing_code = 999999.9999

# Get information from the header.
with open(ndawn_file) as ndawn_data:
    org_name_header = ndawn_data.readline()
    date_range_line = ndawn_data.readline()
    flag_glossary = ndawn_data.readline()
    var_name_line = ndawn_data.readline()
    unit_name_line = ndawn_data.readline()

# Get the month, day, and year from the line with the date range.
date_range_match = re.search('.* for (\w*) (\d{1,2}) (\d{4}) to (\w*) (\d{1,2}) (\d{4})', date_range_line)
if date_range_match:
    # Must convert the month name to a number.
    start_month = time.strptime(date_range_match.group(1), '%B').tm_mon
    start_day = date_range_match.group(2)
    start_year = date_range_match.group(3)
    # Must convert the month name to a number.
    end_month = time.strptime(date_range_match.group(4), '%B').tm_mon
    end_day = date_range_match.group(5)
    end_year = date_range_match.group(6)

    # Will output the start date of the file to the NASA file.
    file_date = '{:4d} {:02d} {:02d}'.format(int(start_year), int(start_month), int(start_day))
    # Output name is currently based on the range of dates in the file.
    output_name = '{:4d}_{:02d}_{:02d}-{:4d}_{:02d}_{:02d}.rainfall.raw'.format(int(start_year), int(start_month), int(start_day), int(end_year), int(end_month), int(end_day))
else:
    print 'Cannot determine output name from range in file.'
    exit()

# Get data from the file.
latitude, longitude, year_list, month_list, day_list, rainfall = np.genfromtxt(ndawn_file, skip_header = 5, usecols = (1, 2, 4, 5, 6, 7), unpack = True, delimiter = ',')
# Rainfall flag needs to be handled separately so that it is read as a string.
flag = np.genfromtxt(ndawn_file, skip_header = 5, usecols = (8), delimiter = ',', dtype = str)

row_num = len(year_list)

doy_arr = np.empty(shape=[row_num])
julian_arr = np.empty(shape=[row_num])
# Calculate the day of the year and julian date for each entry.
for i in range(row_num):
    this_date = '{:4d} {:02d} {:02d}'.format(int(year_list[i]), int(month_list[i]), int(day_list[i]))
    doy_arr[i] = float(datetime.datetime.strptime(this_date, '%Y %m %d').timetuple().tm_yday)
    julian_arr[i] = ndawn_obj.calculate_jul_date(dt=[str(year_list[i])[2:4], month_list[i], day_list[i], 0, 0, 0])
    # Replace missing rainfall measurements withs the missing value code.
    if flag[i] == 'M':
        rainfall[i] = missing_code

# Combine the 1D data arrays into a 2D array that is formatted like the output.
total_data = np.column_stack((julian_arr, doy_arr, year_list, latitude, longitude, rainfall))
column_num = len(total_data[0])

# Variables that need to be set: NV, VUNITS, VNAME, SNAME, MNAME, VMISS, data, VDESC
ndawn_obj.SNAME = 'Rain Gauge Measurement'
ndawn_obj.MNAME = 'North Dakota Agricultural Weather Network'
ndawn_obj.XNAME = 'Julian Date [Days]'

# Long variable names.
ndawn_obj.VNAME = ['Date (Day of Year)', 'Calendar Year', 'Latitude (degrees)', 'Longitude (degrees)', 'Daily Rainfall (inches)']
# Short variable names.
ndawn_obj.VDESC = ['JulDay', 'Date', 'Year', 'Latitude', 'Longitude', 'Rainfall']
# Unit names.
ndawn_obj.VUNITS = ['Days', 'DOY', 'Year', 'Degrees', 'Degrees', 'Inches']

for i in range(0, len(ndawn_obj.VDESC)):
    # The data dictionary must have keys that contain the columns of the data.
    ndawn_obj.data[ndawn_obj.VDESC[i]] = total_data[:,i]

# Missing values for the data (except the time series variable).
ndawn_obj.VMISS = [str(missing_code)] * (column_num - 1)
# Number of data columns.
ndawn_obj.NV = column_num
ndawn_obj.VFREQ  = 'Daily Data'

ndawn_obj.DATE = file_date
ndawn_obj.RDATE  = (time.strftime("%Y %m %d"))

ndawn_obj.name = output_name
ndawn_obj.WriteFile()
