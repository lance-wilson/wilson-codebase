#!/usr/bin/env python3
#
# Name:
#   swath_images.py
#
# Purpose:  Output images of the the 2D variables from CM1 (e.g. sws2 'max
#           windspeed at lowest level, translated with moving domain')
#
# Syntax: 
#   python3 swath_images.py version_number variable start_time end_time
#
#   Input: 
#
# Execution Example:
#   python3 swath_images.py v5 sws2 5970 8670
#
# Modification History:
#   2022/06/29 - Lance Wilson:  Created
#

from calc_file_num_offset import calc_file_offset

from netCDF4 import Dataset
from netCDF4 import MFDataset

import atexit
import matplotlib.pyplot as plt
import numpy as np
import sys

mandatory_arg_num = 4

if len(sys.argv) > mandatory_arg_num:
    version_number = sys.argv[1]
    variable = sys.argv[2]
    start_time = float(sys.argv[3])
    end_time = float(sys.argv[4])
else:
    print('Model version number, variable, and/or start/end time of plots was not specified.')
    print('Syntax: python3 swath_images.py model_version_number variable start_time end_time')
    print('Example: python3 swath_images.py v5 sws2 5970 8670')
    print('Currently supported version numbers: v3, 10s, v4, v5')
    sys.exit()

if version_number.startswith('v'):
    run_number = int(version_number[-1])
else:
    run_number = 3

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# User-Defined Input/Output Directories and Constants
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
model_dir = '75m_100p_{:s}/'.format(version_number)
output_dir = model_dir + 'swath_images/'

# How frequency to show output plots (every N files).
file_frequency = 30

# Minimum and maximum values to use for the color scale.
min_val = 0.0
max_val = 100.0
val_interval = 10.0

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Plot the surface swath.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
file_num_offset = calc_file_offset(version_number, start_time)
file_num_end = calc_file_offset(version_number, end_time)

for file_num in range(file_num_offset, file_num_end+1, file_frequency):
    file_name = model_dir + 'JS_75m_run{:d}_{:06d}.nc'.format(run_number, file_num)
    ds = Dataset(file_name)

    file_time = int(ds.variables['time'][0])

    sfc_swath = np.copy(ds.variables[variable][0][::-1,:])

    title_string = getattr(ds.variables[variable], 'def').title()
    unit_string = ds.variables[variable].units

    ds.close()

    # File name for outputing raw image of the surface swath.
    image_file_name = output_dir + 'swath_{:s}_{:s}_nc{:d}_time{:d}.png'.format(version_number, variable, file_num, file_time)
    #plt.imsave(image_file_name, sfc_swath, vmin=min_val, vmax=max_val)

    plt.figure()
    fig1 = plt.imshow(sfc_swath, interpolation='none', vmin=min_val, vmax=max_val)
    plt.title(title_string.replace(',', '\n'))
    plt.xlabel('E-W Grid Points', fontsize = 16)
    plt.ylabel('N-S Grid Points', fontsize = 16)

    cticks = np.arange(min_val, max_val+val_interval, val_interval)
    bar = plt.colorbar(fig1, ticks=cticks)
    bar.set_label('{:s} ({:s})'.format(title_string.split(' ')[1], unit_string), fontsize = 16)

    # File name for labelled plot with colorbar.
    image_file_name_labelled = output_dir + 'swath_{:s}_{:s}_nc{:d}_time{:d}_labels.png'.format(version_number, variable, file_num, file_time)
    #plt.savefig(image_file_name_labelled, dpi=400)
    plt.show()

