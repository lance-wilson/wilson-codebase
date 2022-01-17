#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/convert_ndarbcontonasa.py
#
# Name:
#   convert_ndarbcontonasa.py
#
# Purpose:  convert the data from a North Dakota Atmospheric Research Board
#           Cooperative Observer Network (NDARBCON) CSV file into the
#           NASA/ADPAA format.
#
# Syntax:
#   python convert_ndarbcontonasa.py [file]
#
# Input Files: directory should contain .csv files.
#
# Execution Example:
#   Linux example: python convert_ndarbcontonasa.py Bowman_county_active_precip.csv
#
# Modification History:
#   2018/10/23 - Lance Wilson:  Created.
#   2018/11/19 - Lance Wilson:  Organized data by Julian Date.
#   2018/11/20 - Lance Wilson:  Added file output.
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
import numpy as np
import sys
import time

from adpaa import ADPAA

def help_message():
    print 'Syntax : python convert_ndarbcontonasa.py [file]'
    print 'Example: python convert_ndarbcontonasa.py Bowman_county_active_precip.csv'
    print '         produces file called "1977_06_01-2018_07_31.ndarb.raw"'

for param in sys.argv:
    if param.startswith('-h') or param.startswith('--help'):
        help_message()
        exit()

if len(sys.argv) > 1:
    ndarb_file = sys.argv[1]
else:
    help_message()

ndarb_obj = ADPAA()
missing_code = 999999.9999

# Get the dates from the file.
date_list = np.genfromtxt(ndarb_file, skip_header = 1, usecols = 4, delimiter = ',', dtype=str)
row_num = len(date_list)

# Calculate the julian dates for each line.
doy_arr = np.empty(shape=[row_num])
julian_arr = np.empty(shape=[row_num])
year_arr = np.empty(shape=[row_num])
for i in range(row_num):
    doy_arr[i] = float(datetime.datetime.strptime(date_list[i], '%Y-%m-%d').timetuple().tm_yday)
    split_date = date_list[i].split('-')
    year_arr[i] = split_date[0]
    this_month = split_date[1]
    this_day = split_date[2]
    julian_arr[i] = ndarb_obj.calculate_jul_date(dt=[str(year_arr[i])[2:4], this_month, this_day, 0, 0, 0])

# Get the range of years found in the file.
start_year = min(year_arr)
end_year = max(year_arr)
first_dates_index = np.where(year_arr == start_year)[0]
last_dates_index = np.where(year_arr == end_year)[0]
start_month = int(datetime.datetime.strptime(date_list[first_dates_index[0]], '%Y-%m-%d').timetuple().tm_mon)
start_day = int(datetime.datetime.strptime(date_list[first_dates_index[0]], '%Y-%m-%d').timetuple().tm_mday)
end_month = int(datetime.datetime.strptime(date_list[last_dates_index[-1]], '%Y-%m-%d').timetuple().tm_mon)
end_day = int(datetime.datetime.strptime(date_list[last_dates_index[-1]], '%Y-%m-%d').timetuple().tm_mday)

# Will output the start date of the file to the NASA file.
file_date = '{:4d} {:02d} {:02d}'.format(int(start_year), start_month, start_day)
# Output name is currently based on the range of dates in the file.
output_name = '{:4d}_{:02d}_{:02d}-{:4d}_{:02d}_{:02d}.ndarb.raw'.format(int(start_year), start_month, start_day, int(end_year), end_month, end_day)

# Get the main data from the file.
site_num, id_num, latitude, longitude, rainfall = np.genfromtxt(ndarb_file, skip_header = 1, usecols = (0,1,2,3,5), delimiter = ',', unpack = True)

# Check for any missing values in the rainfall data.
for i in range(len(rainfall)):
    if np.isnan(rainfall[i]):
        rainfall[i] = missing_code

data = []
unique_julian = []

# Sort the data by julian date.
for julian_day in sorted(julian_arr):
    this_julian = julian_day
    if this_julian not in unique_julian:
        this_day_indices = np.where(julian_arr == this_julian)[0]
        unique_julian.append(this_julian)

        for j in this_day_indices:
            this_row = [this_julian, year_arr[j], doy_arr[j], site_num[j], id_num[j], latitude[j], longitude[j], rainfall[j]]
            data.append(this_row)

# Need a numpy array to get the columns of the data for the dictionary.
data_arr = np.array(data)

column_num = len(data[0])

# Variables that need to be set: NV, VUNITS, VNAME, SNAME, MNAME, VMISS, data, VDESC
ndarb_obj.SNAME = 'Rain Gauge Measurement'
ndarb_obj.MNAME = 'North Dakota Atmospheric Research Board Cooperative Observer Network'
ndarb_obj.XNAME = 'Julian Date [Days]'

# Long variable names.
ndarb_obj.VNAME = ['Calendar Year', 'Date (Day of Year)', 'Site Number', 'Site ID Number', 'Latitude (degrees)', 'Longitude (degrees)', 'Daily Rainfall (inches)']
# Short variable names.
ndarb_obj.VDESC = ['JulianDay', 'Year', 'Date', 'Site_Number', 'ID_Number', 'Latitude', 'Longitude', 'Rainfall']
# Unit names.
ndarb_obj.VUNITS = ['Days', 'Year', 'DOY', 'None', 'None', 'Degrees', 'Degrees', 'Inches']

for i in range(0, len(ndarb_obj.VDESC)):
    # The data dictionary must have keys that contain the columns of the data.
    ndarb_obj.data[ndarb_obj.VDESC[i]] = data_arr[:,i]

# Missing values for the data (except the time series variable).
ndarb_obj.VMISS = [str(missing_code)] * (column_num - 1)
# Number of data columns.
ndarb_obj.NV = column_num
ndarb_obj.VFREQ  = 'Daily Data'

# Start date of the file.
ndarb_obj.DATE = file_date
# Date of creation of file.
ndarb_obj.RDATE  = (time.strftime("%Y %m %d"))

# Name of the file.
ndarb_obj.name = output_name
ndarb_obj.WriteFile()
