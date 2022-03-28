#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/CCNCactivationsize.py
#
# Name:
#   CCNCactivationsize.py
#
# Purpose:
#   To calculate the activation size of the DMT cloud condensation nuclei
#   counter based on laboratory data.
#
# Syntax:
#   python CCNCactivationsize.py arg1 arg2 arg3 arg4
#
#   Input NASA/UND formatted Files:
#       arg1 - A "postprocessing" formatted Nasafile, with optical particle
#              counter bin from POLCAST radar analysis. Must contain data
#              categories called "dccnConc" and "Time". 
#              An example file name is "16_04_06_00_00_00.serialc.dmtccnc.raw".
#       arg2 - A "cpc" formatted Nasafile with one only one particle count bin,
#              from in lab data collection. Must contain data categories
#              called "Mea3771Conc" and "Time".
#              An example file name is "10_04_06_18_15_48.cpc3771.raw".
#       arg3 - A "interval" formatted Nasafile which contains the time
#              intervals over which to calculate average counts and ratios.
#              Must have a "StartTime" and "SamEndTime" data category.
#              An example file name is "16_04_06_18_37_00.sizeintervals.raw".
#       arg4 - A previously existing optional argument that
#              represents the correction factor, which will be value
#              between 0 and 1.
#
#   Output Files:
#       Outputs a NASA/UND formatted ASCII file.
#
# Execution Example:
#   Linux example: python CCNCactivationsize.py /nas/ral/NorthDakota/Year2016/DMT076_LabData/20160406_181548/PostProcessing/16_04_06_00_00_00.serialc.dmtccnc.raw /nas/ral/NorthDakota/Year2016/DMT076_LabData/20160406_181548/CPC_Data/16_04_06_18_15_48.cpc3771.raw /nas/ral/NorthDakota/Year2016/DMT076_LabData/20160406_181548/Intervals/16_04_06_18_37_00.sizeintervals.raw
#
#   Windows example: python CCNCactivationsize.py {airborne_network_drive}:\ral\NorthDakota\Year2016\DMT076_LabData\20160406_181548\PostProcessing\16_04_06_00_00_00.serialc.dmtccnc.raw {airborne_network_drive}:\ral\NorthDakota\Year2016\DMT076_LabData\20160406_181548\CPC_Data\16_04_06_18_15_48.cpc3771.raw {airborne_network_drive}:\ral\NorthDakota\Year2016\DMT076_LabData\20160406_181548\Intervals\16_04_06_18_37_00.sizeintervals.raw
#   Airborne_network_drive example: Z
#
# Modification History:
#   2016/05/24 - Lance Wilson:  Created.
#   2016/05/25 - Lance Wilson:  Added file output, added comments.
#   2016/05/26 - Lance Wilson:  Modified comments, added warning handling,
#                               streamlined retrieval of data.
#   2016/05/31 - Lance Wilson:  Added summing of ccn_count bins, looped to
#                               add all time intervals, removed warning
#                               handling, added comments.
#   2016/06/01 - Lance Wilson:  Added CCN ratios as keys to one of the original
#                               NasaFile objects.
#   2016/06/06 - Lance Wilson:  Added modifications to header in Nasafileout.
#   2016/06/07 - David Delene:  Changed name and added comments.
#   2016/06/08 - Lance Wilson:  Modified comments, added help message, added
#                               command-line arguments.
#   2016/06/09 - Lance Wilson:  Changed variable used for calculation from
#                               postProcessing, modified comments, added
#                               checking for missing value codes.
#   2016/06/15 - Lance Wilson:  Checked verification, modified comments.
#   2016/06/16 - Lance Wilson:  Streamlined masking of missing value codes.
#   2016/06/20 - Lance Wilson:  Added header modifications.
#   2016/06/22 - Lance Wilson:  Removed test output files, added standard dev.
#   2016/06/27 - Lance Wilson:  Modified standard deviation formula, converted
#                               range for time_index to be calculated variable.
#   2016/06/28 - Lance Wilson:  Added second verification for standard dev.
#   2016/06/29 - Lance Wilson:  Modified comments and help message. Added
#                               handling for KeyErrors
#   2016/06/30 - Lance Wilson:  Modified CPC data variable being collected,
#                               Updated verification.
#   2016/07/18 - Lance Wilson:  Added file output names based on input files.
#   2016/07/26 - Lance Wilson:  Added missing interval error handling.
#   2016/09/21 - Lance Wilson:  Added calculations for the ratio modified by a
#                               correction factor and added the correction
#                               factor as an optional argument.
#   2016/09/23 - Lance Wilson:  Added the corrected ratio as a variable in the
#                               output NasaFile, added comments.
#   2016/09/28 - Lance Wilson:  Correct insertion of variable names into header.
#   2018/11/20 - Lance Wilson:  Updated to use ADPAA module instead of
#                               deprecated NasaFile and NasaFileOut.
#
# Verification of Data:
#   Used command "cplot2 16_04_06_00_00_00.serialc.dmtccnc.raw" to determine
#   that the average CCN count value over the time interval 67020 to 67440
#   seconds had the average value of 12.6354 and a standard deviation of
#   4.0584. A second command ("cplot2 16_04_06_18_15_48.cpc3771.raw") was used
#   to determine that the average CPC count over this intervals was 238.3107
#   with a standard deviation of 9.6847. The CCN/CPC ratio was manually
#   calculated from this to be 0.053020699. Standard Deviation of the ratio
#   was manually calculated from the formula provided at the source listed in
#   the code to be 0.017165640. (Verificaton as of June 30, 2016).
#
# Copyright 2016, 2018 Lance Wilson, David Delene
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
import sys
from adpaa import ADPAA

def help_message():
    print 'Syntax: python CCNCactivationsize.py arg1 arg2 arg3 arg4\n'
    print ('Purpose: To calculate the activations size of the DMT cloud '
           'condensation nuclei counter based on laboratory data.\n')
    print ('arg1 - A "postprocessing" formatted Nasafile, with optical '
           'particle counter bins from POLCAST radar analysis. Must have a '
           'data category for "Time" and "dccnConc".\n\t'
           'Example file name: "16_04_06_00_00_00.serialc.dmtccnc.raw"\n')
    print ('arg2 - A "cpc" formatted Nasafile with one only one particle count '
           'bin, from in lab data collection. Must have data categories for '
           '"Time" and "Mea3771Conc".\n\tExample file name: '
           '"10_04_06_18_15_48.cpc3771.raw"\n')
    print ('arg3 - A "interval" formatted Nasafile which contains the time '
           'intervals over which to calculate average counts and ratios. Must '
           'have a "StartTime" and "SamEndTime".\n\t'
           'Example file name: "16_04_06_18_37_00.sizeintervals.raw"\n')
    print ('arg4 - Optional argument that represents the correction factor, '4
           'which will be value between 0 and 1.\n')

for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h')):
        help_message()
        exit()

if (len(sys.argv) < 4):
    help_message()
    exit()

# Set file names from command-line arguments.
dmtccnc_file = sys.argv[1]
cpc_file = sys.argv[2]
interval_file = sys.argv[3]

# Set the correction factor (must be between 0 and 1, defaults to 0).
cor_factor = 0.0
if (len(sys.argv) == 5):
    cor_factor = float(sys.argv[4])

# Create ADPAA objects from the input files.
postProcess = ADPAA()
cpc = ADPAA()
intervals = ADPAA()

postProcess.ReadFile(dmtccnc_file)
cpc.ReadFile(cpc_file)
intervals.ReadFile(interval_file)

key_list = intervals.data.keys()
key = key_list[0]
# Set number of time intervals.
time_interval = len(intervals.data[key])

ccn_ratio = np.zeros([time_interval])
cor_ratio = np.zeros([time_interval])
ratio_std = np.zeros([time_interval])

# Time_index specifies which size interval to use (from intervals object).
time_index = 0
while (time_index < time_interval):
    try:
        # Find value of index where time is at this start time.
        start = np.where(postProcess.data['Time'] == 
                         intervals.data['StartTime'][time_index])
        # Convert the tuple return to an array. Array is converted to integer
        #   automatically because it has size of 1.
        start = start[0]

        # Find value of index where time is at this start time.
        end = np.where(postProcess.data['Time'] == 
                       intervals.data['SamEndTime'][time_index])
        # Convert the tuple return to an array. Array is converted to integer
        #   automatically because it has size of 1.
        end = end[0]

        # Mask missing values.
        postProcess.mask_MVC()

        # Calculate the mean ccn count for the this time interval.
        try:
            ccn_count = np.mean(postProcess.data['dccnConc'][start:end])
            ccn_std = np.std(postProcess.data['dccnConc'][start:end])
        # TypeError indicates that the specified start or end time interval was
        #   not found in the postProcessing data.
        except TypeError:
            print 'Specified time interval in the Interval file was not found in the postProcessing file.'
            exit()

        # Find value of index where time is at this start time.
        start = np.where(cpc.data['Time'] == 
                        intervals.data['StartTime'][time_index])
        # Convert the tuple return to an array. Array is converted to integer
        #   automatically because it has size of 1.
        start = start[0]

        # Find value of index where time is at this end time.
        end = np.where(cpc.data['Time'] == intervals.data['SamEndTime'][time_index])
        # Convert the tuple return to an array. Array is converted to integer
        #   automatically because it has size of 1.
        end = end[0]

        # Mask missing values.
        cpc.mask_MVC()

        # Calculate the mean cpc count for the this time interval.
        try:
            cpc_count = np.mean(cpc.data['Mea3771Conc'][start:end])
            cpc_std = np.std(cpc.data['Mea3771Conc'][start:end])
        # TypeError indicates that the specified start or end time interval was not found in the CPC data.
        except TypeError:
            print 'Specified time interval in the Interval file was not found in the CPC file.'
            exit()
    except KeyError:
        print 'Required keys were not provided in NasaFile.\n'
        help_message()
        exit()

    ccn_ratio[time_index] = ccn_count/cpc_count
    # Formula for the corrected ratio is taken from equation 2 of Section
    #   2.3.1.2 of "Calibration and measurement uncertainties of a continuous-
    #   flow cloud condensation nuclei counter (DMT-CCNC): CCN activation of
    #   ammonium sulfate and sodium chloride aerosol particles in theory and
    #   experiment", page 1156 of Atmospheric Chemistry and Physics, 8, 2008.
    #   Found at http://www.atmos-chem-phys.net/8/1153/2008/acp-8-1153-2008.pdf
    cor_ratio[time_index] = ((ccn_count - cpc_count * cor_factor)/(cpc_count - cpc_count * cor_factor))
    # Formula for standard deviation found on page 45, section 13-3 (e) of
    #   "Experimentation: An Introduction to Measurement Theory and Experiment
    #   Design", 2nd Edition, by D.C. Baird
    ratio_std[time_index] = ccn_ratio[time_index] * math.sqrt(math.pow(\
        (ccn_std/ccn_count), 2) + math.pow((cpc_std/cpc_count), 2))
    time_index += 1

# Edit general header info
# Add to number of lines in header.
intervals.NLHEAD += 3
# Add to number of variables.
intervals.NV += 3

# Scaling factors.
intervals.VSCAL.extend(['1.0000'])
intervals.VSCAL.extend(['1.0000'])
intervals.VSCAL.extend(['1.0000'])

# Missing value codes.
intervals.VMISS.extend(['999999.9999'])
intervals.VMISS.extend(['999999.9999'])
intervals.VMISS.extend(['999999.9999'])

# Add longvariable description.
intervals.VNAME.extend(['Aerosol CCN/CPC Ratio [none]'])
intervals.VNAME.extend(['Aerosol CCN/CPC Ratio Standard Deviation [none]'])
intervals.VNAME.extend(['Corrected Aerosol Ratio [none]'])

# Add units for new variables.
intervals.VUNITS.extend(['none'])
intervals.VUNITS.extend(['none'])
intervals.VUNITS.extend(['none'])
# Add short names for new variables.
intervals.VDESC.extend(['CCN_Ratio'])
intervals.VDESC.extend(['StandDev'])
intervals.VDESC.extend(['Cor_Ratio'])

# Add new data to ADPAA object.
intervals.data['CCN_Ratio'] = ccn_ratio
intervals.data['StandDev'] = ratio_std
intervals.data['Cor_Ratio'] = cor_ratio

# Take full file name from arguments.
dmtccnc_filename = sys.argv[1]
# Find right-most instance of directory path.
if (sys.platform.startswith('win')):
    dir_val = dmtccnc_filename.rfind('\\')
else:
    dir_val = dmtccnc_filename.rfind('/')
# File name is everything to the right of that.
dmtccnc_string = dmtccnc_filename[dir_val+1:]
# Split strings on periods.
dmtccnc_strings = dmtccnc_string.split('.')
# Date is the first string in that list.
date_string = dmtccnc_strings[0]
outstring = date_string + '.testccncpcratio.raw'
intervals.WriteFile(outstring)

