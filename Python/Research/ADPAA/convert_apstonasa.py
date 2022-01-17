#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/convert_apstonasa.py
#
# Name:
#   convert_apstonasa.py
#
# Purpose:  convert the data from an Aerosol Instrument Manager file to the
#           UND/NASA format.
#
# Syntax:
#   python convert_apstonasa.py APSfile
#
# Input Files: .txt files in the comma delimited format similar to the format
#   produced for SMPS files as outlined at
#   <http://atmoswiki.aero.und.edu/atmos/citation/instruments/smps/home>.
#
# Execution Example:
#   Linux example: python convert_apstonasa.py APS3321_151104i.txt
#
# Modification History:
#   2018/09/26 - Lance Wilson:  Created.
#   2018/09/27 - Lance Wilson:  Added comments, made some things more efficient.
#   2018/10/04 - Lance Wilson:  Added channel boundaries based on email between
#                               Charles Lo of TSI and David Delene: boundaries
#                               between midpoints A and B is (A*B)^(1/2).
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
import sys
import time

from adpaa import ADPAA

def help_message():
    print 'Syntax : python convert_apstonasa.py APSfile'
    print 'Example: python convert_apstonasa APS3321_151104i.txt'
    print '         produces file called "APS3321_141104i.raw"'
    exit()

for param in sys.argv:
    if param.startswith('-h') or param.startswith('--help'):
        help_message()

if len(sys.argv) > 1:
    apsfile = sys.argv[1]
else:
    help_message()

aps_obj = ADPAA()

# Read in the APS Comma Delimited File. 
aps_lines = open(apsfile, "r").readlines()

#---------------------------------------------------------------------------
# 	A) HEADER INFORMATION 
#---------------------------------------------------------------------------

# Define the header information 
density                = float(aps_lines[2].split(',')[-1])
stokes_correct         = str(aps_lines[3].split(',')[-1])
lower_channel_bound    = float(aps_lines[4].split(',')[-1])
upper_channel_bound    = float(aps_lines[5].split(',')[-1])

# Get initial day of year from the first row of data.
start_date = aps_lines[7].split(',')[1]
month, day, year = [int(var) for var in start_date.split('/')]
# Put the date in a format that is accepted by the ADPAA object.
file_date = '{:4d} {:02d} {:02d}'.format(2000+year, month, day)
initial_doy = float(datetime.datetime.strptime(file_date, '%Y %m %d').timetuple().tm_yday)

# Get initial time from the first row of data.
start_time = aps_lines[7].split(',')[2]
hour, minute, second = [int(var) for var in start_time.split(':')]

output_name = '{:02d}_{:02d}_{:02d}_{:2d}_{:02d}_{:02d}.raw'.format(year, month, day, hour, minute, second)

#---------------------------------------------------------------------------
# 	B) DEFINE VARIABLES/DATA
#---------------------------------------------------------------------------

# Define the variable array.
apsvar = aps_lines[6].split(',')

# Remove new lines and excess units from the list of variables.
for i in range(len(apsvar)):
    apsvar[i] = apsvar[i].split('(')[0]

# Number of header rows.
header_count = 0
# Increment the number of header rows until it finds a sample number of 1
#   (start of the data rows) (as of 2018, should be 7).
while aps_lines[header_count].split(',')[0] != '1':
    header_count += 1

# Define the number of data rows.
numrows = len(aps_lines)-header_count

# Define the middle of the bins. 
aps_midbins = []
for i in range(4,56):
    # The first midbin is <0.523, so must remove non-numerical characters.
    aps_midbins.append(float(''.join(c for c in apsvar[i] if c.isdigit() or c == '.')))
midbin_length = len(aps_midbins)

aps_list = []
# Fill the data array.
for i in range(numrows):
    aps_row = []
    line_arr = aps_lines[i+header_count].split(',')
    # Time (Seconds from midnight).
    temp_time = line_arr.pop(2)
    this_hour, this_min, this_sec = temp_time.split(':')
    this_sfm = aps_obj.hms2sfm(this_hour, this_min, this_sec)
    aps_row.append(this_sfm)

    # Date (Day of Year).
    temp_date = line_arr.pop(1)
    this_doy = initial_doy + this_sfm/86400.
    aps_row.append(this_doy)

    # Status Flags
    status_flags = line_arr.pop(-7).split()
    for flag in status_flags:
        # Status flags stay in order because they are inserted before entry -6.
        line_arr.insert(-6, flag)

    # Add in the rest of the data.
    for j in range(len(line_arr)):
        temp = line_arr[j].split('(')[0]

        if len(temp) > 0:
            try:
                aps_row.append(float(temp))
            except ValueError:
                # Ignore values that can't be converted to float since they are
                #   not accepted by the ADPAA object (should only affect the 
                #   'dN/dlogdP' column).
                continue
        else:
            aps_row.append(999999.9999)
    aps_list.append(aps_row)
aps_data = np.array(aps_list)

file_length = len(aps_data[0]) - 1

channel_bounds = [lower_channel_bound, aps_midbins[0]]
for i in range(1, len(aps_midbins)-1):
    # Boundary between midpoints A and B is sqrt(A*B), as described in email
    #   communication between David Delene and Charles Lo (TSI).
    next_bound = math.sqrt(aps_midbins[i] * aps_midbins[i+1])
    channel_bounds.append(next_bound)
channel_bounds.append(upper_channel_bound)

# Variables that need to be set: NV, VUNITS, VNAME, SNAME, MNAME, VMISS, data, VDESC
aps_obj.SNAME = 'APS 3321'
aps_obj.MNAME = 'ICE Flare Data'

# Unit Names
aps_obj.VUNITS = (['sfm', 'DOY', 'None'] + ['#/cm^3'] * midbin_length + 
              ['#', '#', '#', 'sec', 'kPa', 'l/min', 'l/min', 'volts', 'volt', '#', '#', '#', 'Volts', 'Volts', 'amps', 'Volts', 'C', 'C', 'Volts'] +
              ['None'] * len(status_flags) +
              ['um', 'um', 'um', 'um', 'Std.Dev', '#/cm^3'])

# Short variable names
aps_obj.VDESC = (['Time', 'Date', 'SampleNum'] + ['CH{:02d}_N'.format(i+1) for i in range(midbin_length)] +
               ['Event1', 'Event2', 'Event3', 'DeadTime', 'InletPT', 'TotFlow', 'SheaFlow', 'InVolt0', 'InVolt1', 'InLev0', 'InLev1', 'InLev2', 'LasPw', 'LasCur', 'ShePVolt', 'TotPVolt', 'BoxTemp', 'PhotoTemp', 'PhotoVolt'] +
               ['Flag{:d}'.format(i+1) for i in range(len(status_flags))] +
               ['Median', 'Mean', 'GeoMean', 'Mode', 'GeoStDev', 'TotalConc'])

# Long variable names
aps_obj.VNAME = (['Date (Day of Year)', 'Sample Number'] +
              ['APS Channel {:02d}_N ({:.3f} to {:.3f} um)'.format(i+1, channel_bounds[i], channel_bounds[i+1]) for i in range(midbin_length)] +
              ['APS Event 1', 'APS Event2', 'APS Event3', 'APS Dead Time', 'APS Inlet APS Pressure Total', 'APS Total Flow', 'APS SheathFlow', 'APS Analog Input Voltage 0', 'APS Analog Input Voltage 1', 'APS Digital Input Level0', 'APS Digital Input level 1', 'APS Digital Input Level2', 'APS Laser Power', 'APS LaserCurrent', 'APS Sheath Pump Voltage', 'APS Total Pump Voltage', 'APS Box Temperature', 'APS Avalanch Photo Diode Temperature', 'APS Avalanch PhotoDiode Voltage'] +
              ['Status Flag {:d}'.format(i+1) for i in range(len(status_flags))] +
              ['APS Median (um)', 'APS Mean (um)', 'APS Geo. Mean (um)', 'APS Mode (um)', 'APS Geo. Std. Dev.', 'Total Concentration (#/cm3)'])

for i in range(0, len(aps_obj.VDESC)):
    # The data dictionary must have keys that contain the columns of the data.
    aps_obj.data[aps_obj.VDESC[i]] = aps_data[:,i]

# Missing values for the all data except the time.
aps_obj.VMISS = ['999999.9999'] * (file_length)
# Total number of columns.
aps_obj.NV = file_length + 1
# Frequency of data is every 2 minutes, 15 seconds.
aps_obj.VFREQ  = '0.0074 Hz Data'

aps_obj.DATE = file_date
aps_obj.RDATE  = (time.strftime("%Y %m %d"))

aps_obj.name = output_name
aps_obj.WriteFile()
