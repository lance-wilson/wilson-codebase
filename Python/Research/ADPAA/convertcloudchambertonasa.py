#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/convertcloudchambertonasa.py
#
# Name:
#   convertcloudchambertonasa.py
#
# Purpose:  convert the data from the Michigan PI cloud chamber to the UND/NASA
#           format that can be plotted with cplot.
#
# Syntax:
#   python convertcloudchambertonasa.py [directory]
#
# Input Files: directory should contain .txt files containing data collected
#              by the Welas instrument.
#
# Execution Example:
#   Linux example: python convertcloudchambertonasa.py 20180620_AgI_neg11C_1
#
# Modification History:
#   2018/08/09 - Lance Wilson:  Created.
#   2018/09/18 - Lance Wilson:  Fixed day-of-year variable type error.
#   2018/11/06 - Lance Wilson:  Changed how columns of data are read and added
#                               columns with summations of blocks of data.
#   2018/12/13 - Lance Wilson:  Updated search for files to use to be more
#                               specific so it doesn't try to read in time
#                               series data.
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
    print 'Syntax : python convertcloudchambertonasa.py [directory]'
    print 'Example: python convertcloudchambertonasa.py 20180620_AgI_neg11C_1'
    print '         produces file called "20180620_AgI_neg11C_1.raw"'
    print ' If directory is included, files in that directory will be used.'
    print ' If no directory is included, it will be run on the current directory.'

for param in sys.argv:
    if param.startswith('-h') or param.startswith('--help'):
        help_message()
        exit()

# If there is a directory provided, the output file will use the provided name.
if len(sys.argv) > 1:
    dir_name = sys.argv[1]
    output_name = dir_name + '.raw'
# If no directory is provided, take the last directory in the full path to use
#   as the name of the output file.
else:
    print 'NOTICE: Using current directory. Run with -h for help.\n'
    dir_name = '.'
    current_dir = re.search('/(.+/)+(.+)', os.getcwd()).group(2)
    output_name = current_dir + '.raw'

# Sort the files in the data directory that end in .txt.
file_list = sorted([file_var for file_var in os.listdir(dir_name) if re.search('(\w+_)+(\d{4,})sec.txt', file_var)])
# Add the directory name to the beginning of each file name so that both cases
#   can be opened.
all_files = [dir_name + '/' + file_name for file_name in file_list]
row_num = len(all_files)

cloud_chamber = ADPAA()

# Use the first file to get the initial day and time of the data.
file_name = all_files[0]
with open(file_name) as chamber_file:
    header = chamber_file.readline()
    datetime_line = chamber_file.readline().split()
    # Get initial day of year from the header of the first file.
    initial_doy = float(datetime.datetime.strptime(datetime_line[0], '%m/%d/%Y').timetuple().tm_yday)
    # Split up the date so that it can be reorganized into YYYY MM DD format.
    file_date_arr = [int(var) for var in datetime_line[0].split('/')]
    file_date = '{:4d} {:02d} {:02d}'.format(file_date_arr[-1], file_date_arr[0], file_date_arr[1])
    # Use the rest of the line to get the initial time.
    file_start_time = datetime_line[1].split(':')
    initial_sfm = cloud_chamber.hms2sfm(file_start_time[0], file_start_time[1], file_start_time[2])

# Only the first and third columns have data that can't be calculated, so just
#   use those to get the boundaries of each bin.
# skip_footer is 13 because it appears that white space lines don't count in
#   the footer, but they do count in the header.
lower_bounds, upper_bounds = np.genfromtxt(file_name, skip_header = 4, skip_footer = 13, usecols = (0,2), unpack = True)
# Number of channels in the original data.
channel_num = len(lower_bounds)

data_list = []
for file_name in all_files:
    # Get the added seconds from the initial time from the file name.
    extra_sfm = float(re.search('./(\w+_)+(\d+)sec.txt', file_name).group(2))
    this_sfm = initial_sfm + extra_sfm

    # Calculate the day of year of the sample.
    this_doy =  initial_doy + (this_sfm/86400.0)

    # Get the fourth column of data, which contains the channel data for this file.
    this_data = list(np.genfromtxt(file_name, skip_header = 4, skip_footer = 13, usecols = 4))

    data_list.append([this_sfm] + [this_doy] + this_data)
data_array = np.array(data_list)

# Sum length will remain an integer, so that data that can't fill a set of 30
#   will be omitted.
block_size = 30
sum_length = (channel_num - 2)/block_size
sum_data = np.empty(shape=[row_num, sum_length])
lower_sum_bounds = []
upper_sum_bounds = []
for i in range(sum_length):
    sum_data[:,i] = [sum(data_array[j,block_size*i+2:block_size*i+block_size+2]) for j in range(row_num)]
    lower_sum_bounds.append(lower_bounds[block_size*i])
    upper_sum_bounds.append(upper_bounds[block_size*i+block_size-1])

total_data = np.concatenate((data_array, sum_data), axis = 1)
# Number of columns for the purposes of NV and VMISS is the number of columns,
#   not including the time variable. (In this case, channels plus the sum
#   channels plus the day of the year.)
column_num = channel_num + sum_length + 1

# Variables that need to be set: NV, VUNITS, VNAME, SNAME, MNAME, VMISS, data, VDESC
cloud_chamber.ORG = 'Michigan Technological University'
cloud_chamber.SNAME = 'Cloud Chamber Lab'
cloud_chamber.MNAME = 'Flare Testing'

short_names = ['Time', 'Date']
long_names = ['Date (Day of Year)']
unit_names = ['sfm', 'DOY'] + ['#'] * (channel_num + sum_length)

for i in range(channel_num):
    long_names.append('Welas OPC CH{:003d}_N ({:.3f} to {:.3f} um)'.format(i+1, lower_bounds[i], upper_bounds[i]))
    short_names.append('CH{:003d}_N'.format(i+1))

for j in range(sum_length):
    long_names.append('Welas OPC Sum of CH{:003d}_N through CH{:003d}_N ({:.3f} to {:.3f} um)'.format(block_size*j+1, block_size*j+block_size, lower_sum_bounds[j], upper_sum_bounds[j]))
    short_names.append('SUM{:003d}-{:003d}'.format(block_size*j+1, block_size*j+block_size))

cloud_chamber.VDESC = short_names
cloud_chamber.VNAME = long_names
cloud_chamber.VUNITS = unit_names

for i in range(0, len(cloud_chamber.VDESC)):
    # The data dictionary must have keys that contain the columns of the data.
    cloud_chamber.data[cloud_chamber.VDESC[i]] = total_data[:,i]

# Missing values for the channel data plus the day of the year.
cloud_chamber.VMISS = ['999999.9999'] * column_num
# Number of data columns plus the day of the year.
cloud_chamber.NV = column_num
cloud_chamber.VFREQ  = '0.10 Hz Data'

cloud_chamber.DATE = file_date
cloud_chamber.RDATE  = (time.strftime("%Y %m %d"))

cloud_chamber.name = output_name
cloud_chamber.WriteFile()
