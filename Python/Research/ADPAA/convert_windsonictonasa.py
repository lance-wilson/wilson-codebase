#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/convert_windsonictonasa.py
#
# Name:
#   convert_windsonictonasa.py
#
# Purpose:  convert the data from the sonic anemometer to the UND/NASA format
#           that can be plotted with cplot, and be archived by date.
#
# Syntax:
#   python convert_windsonictonasa.py
#
# Input Files: text files created by the Gill Sonic Anemometer, named in the format "Wind [CH601]-##.txt".
#
# Output Files: NASA/UND formatted files, named YYYY_MM_DD_HH_mm_ss.windsonic.raw.
#
# Execution Example:
#   Linux example: python convert_windsonictonasa.py [start_file]
#
# Note: If you are processing large quantities of data, be aware that this
#       program uses approximately 2.15 GB of RAM per full year of one second
#       data.
#
# Modification History:
#   2018/12/06 - Lance Wilson:  Created.
#   2018/12/07 - Lance Wilson:  Completed output to file.
#   2018/12/11 - Lance Wilson:  Implemented more efficient use of memory.
#   2018/12/12 - Lance Wilson:  Fixed bugs where files without data were not
#                               handled correctly.
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
import pandas as pd
import re
import subprocess
import sys
import time

from adpaa import ADPAA

def help_message():
    print 'Syntax : python convert_windsonictonasa.py [start_file]'
    print 'Example: python convert_windsonictonasa.py '
    print '         produces files called "YY_MM_DD_HH_mm_ss.windsonic.raw"'
    print ('NOTE:  If you are processing large quantities of data, be aware '
           'that this program uses approximately 2.15 GB of RAM per full year '
           'of one second data.')

for param in sys.argv:
    if param.startswith('-h') or param.startswith('--help'):
        help_message()
        exit()

# Setup the header for the NASA/UND file.
def setup_wind_obj(wind_obj, year, month, day):
    # Variables that need to be set: NV, VUNITS, VNAME, SNAME, MNAME, VMISS, data, VDESC
    wind_obj.SNAME = 'Gill WindSonic Sonic Anemometer'
    wind_obj.MNAME = 'Sonic Anemometer of University of North Dakota'
    wind_obj.XNAME = 'Date [Day of Year]'

    # Long variable names.
    wind_obj.VNAME = ['Wind Direction (Degrees)', 'Wind Speed (m/s)', 'Status Flag', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']
    # Short variable names.
    wind_obj.VDESC = ['Date','Wind_Dir', 'Speed', 'Flag', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']
    # Unit names.
    wind_obj.VUNITS = ['DOY', 'Degrees', 'm/s', 'None', 'Year', 'Month', 'Day', 'Hour', 'Minute', 'Second']

    # Missing values for the data (except the time series variable).
    wind_obj.VMISS = [str(missing_code)] * (column_num - 1)
    # Number of data columns.
    wind_obj.NV = column_num
    wind_obj.VFREQ  = '1 Hz Data'

    file_date = '{:4d} {:02d} {:02d}'.format(int(year), int(month), int(day))

    # Start date of the file.
    wind_obj.DATE = file_date
    # Date of creation of file.
    wind_obj.RDATE  = (time.strftime("%Y %m %d"))

    # Name of the file.
    output_name = '{:4d}_{:02d}_{:02d}_00_00_00.windsonic.raw'.format(int(year), int(month), int(day))
    wind_obj.name = output_name

    return wind_obj

# Store the data and write the NASA/UND file.
def finalize_wind_obj(wind_obj, data_arr):
    for i in range(0, len(wind_obj.VDESC)):
        # The data dictionary must have keys that contain the columns of the data.
        wind_obj.data[wind_obj.VDESC[i]] = data_arr[:,i]

    wind_obj.WriteFile()
    return

# Get all files in the directory.
file_list = os.listdir('.')
# Only keep files that are made by the sonic anemometer program.
file_list = [file_name for file_name in file_list if file_name.startswith('Wind')]

# Sort the "Wind [CH601]-##.txt" files numerically. 
file_split = [re.split('\W+', file_name) + [file_name] for file_name in file_list]
file_df = pd.DataFrame(data=file_split, columns=['Word', 'Loc', 'Sort', 'Ext', 'Original'])
file_df.set_index('Sort', inplace = True)
file_df.index = file_df.index.astype(int)
sorted_files = file_df.sort_index()

# Check to see if user wanted to start at a specific file.
if len(sys.argv) > 1:
    start_file = sys.argv[1]
    print 'Processing files beginning with \"{:s}\"...'.format(start_file)
    # Only keep files that we want to use.
    start_index = re.split('\W+', start_file)[2]
    sorted_files = sorted_files.loc[int(start_index):]
else:
    print 'Processing all files in directory...'

missing_code = 999999.9999

node_address = 'Q'
array_size = 0
for index in sorted_files.index:
    # Count all the lines that start with the node adress of the instrument.
    #   "|| true" allows it to keep going even if the file is empty.
    array_size += int(subprocess.check_output("grep -c '^{:s}' \"{:s}\" || true".format(node_address, sorted_files['Original'][index]), shell = True))
print 'Finished calculating size of data.'

direction = np.empty([array_size], dtype=float)
speed = np.empty([array_size], dtype=float)
flag = np.empty([array_size], dtype=float)
# Will store the time stamps as a string for now to save memory. 
time_stamps = np.empty([array_size], dtype='|S19')

# Index for the full arrays.
j = 0
for index in sorted_files.index:
    with open(sorted_files['Original'][index], 'r') as this_file:
        if index % 1000 == 0:
            print 'Progress:  Processing file ' + sorted_files['Original'][index]
        # Header lines.
        file_title = this_file.readline()
        instrument_name = this_file.readline()
        out_format = this_file.readline()
        open_time = this_file.readline()
        # Skip empty line.
        this_file.readline()

        this_data = this_file.readlines()
        # If there is no actual data besides close statement, don't try to add
        #   data to the arrays.
        if len(this_data) <= 1:
            continue
        # Remove the "Log file closed" lines from the end of the file.
        while this_data[-1].startswith('Log file'):
            close_time = this_data.pop()

        # Separate the data on commas.
        line_list = [line.strip().split(',') for line in this_data]
        date_times = [value[6] for value in line_list]

        # Count through indices backwards.
        for i in range(len(date_times) - 2, -1, -1):
            # Since the anemometer software frequently freezes, the times
            #   often skip, so the assumption is made that the last time in the
            #   file is correct, and that one second measurements were made for
            #   the full file.
            if date_times[i] != (datetime.datetime.strptime(date_times[i+1], '%m/%d/%Y %H:%M:%S') - datetime.timedelta(seconds = 1)).strftime('%m/%d/%Y %H:%M:%S'):
                date_times[i] = (datetime.datetime.strptime(date_times[i+1], '%m/%d/%Y %H:%M:%S') - datetime.timedelta(seconds = 1)).strftime('%m/%d/%Y %H:%M:%S')

        # Add the data from this file to the arrays.
        for i in range(len(line_list)):
            if line_list[i][1]:
                direction[j] = float(line_list[i][1])
            else:
                direction[j] = missing_code
            if line_list[i][2]:
                speed[j] = float(line_list[i][2])
            else:
                speed[j] = missing_code
            flag[j] = float(line_list[i][4])
            time_stamps[j] = date_times[i]
            j += 1

print 'Finished reading data. Outputting data to file.'

column_num = 10
# Initial time for the setup of the first file.
first_datetime = datetime.datetime.strptime(time_stamps[0], '%m/%d/%Y %H:%M:%S')
first_year = first_datetime.year
first_month = first_datetime.month
first_day = first_datetime.day
this_day = first_day
previous_day = first_day
# Initial file setup.
this_data = []
wind_obj = ADPAA()
wind_obj = setup_wind_obj(wind_obj, first_year, first_month, first_day)
for i in range(len(time_stamps)):
    # Expand the current time stamps into separate variables.
    this_month, this_day, this_year, this_hour, this_minute, this_second = [float(value) for value in re.split('\D+', time_stamps[i])]
    base_doy = float(datetime.datetime.strptime(time_stamps[i], '%m/%d/%Y %H:%M:%S').timetuple().tm_yday)
    this_sfm = wind_obj.hms2sfm(this_hour, this_minute, this_second)
    this_doy = base_doy + this_sfm/86400.

    # If this is a new day, write the previous file and set up a new one.
    if this_day != previous_day:
        data_arr = np.array(this_data)
        finalize_wind_obj(wind_obj, data_arr)

        this_data = []
        wind_obj = ADPAA()
        wind_obj = setup_wind_obj(wind_obj, this_year, this_month, this_day)

    # Create a new row of data.
    this_row = np.array([this_doy, direction[i], speed[i], flag[i], this_year, this_month, this_day, this_hour, this_minute, this_second])
    this_data.append(this_row)
    previous_day = this_day

# Write the final file.
data_arr = np.array(this_data)
finalize_wind_obj(wind_obj, data_arr)
