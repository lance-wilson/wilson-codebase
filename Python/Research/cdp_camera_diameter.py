#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/cdp_camera_diameter.py
#
# Name:
#   cdp_camera_diameter.py
#
# Purpose:
#   To calculate the diameter of cloud droplets from the glare images measured
#   by a cloud droplet probe (CDP) as used in the Wyoming droplet generator
#   experiment first conducted in May 2017.
#
# Syntax:
#   Single file: python cdp_camera_diameter.py ImageFile.jpg [Brightness Threshold] [Init. Width] [Save Path]
#   Multiple files: python cdp_camera_diameter.py Date-Time [Brightness Threshold] [Init. Width] [Save Path]
#
#   Input: A (or multiple) JPEG formatted image file(s).
#
#   Output: Printout of the average width in pixels for each image, and a
#           summary of the overall values: the number of valid values, the
#           mean and standard deviation of the um/pixel calculation, and the
#           mean size and standard deviation of the drop based on calibration
#           values, in um.
#           A plot of the drop diameters over time (only includes valid data,
#           so the time scale is based on index).
#
# Execution Example:
#       With images from a specific time and a whiteness threshold:
#           python cdp_camera_diameter.py 201705261752 252
#
#       With files from May 2017, whiteness threshold, and assumed diameter:
#           python cdp_camera_diameter.py 201705 255 28
#
# Modification History:
#   2017/06/13 - Lance Wilson:  Created.
#   2017/06/14 - Lance Wilson:  Updated help message conditions.
#   2017/06/21 - Lance Wilson:  Added code to search for secondary max.
#   2017/06/22 - Lance Wilson:  Expanded distance calculation to multiple lines.
#   2017/06/27 - Lance Wilson:  Added comments.
#   2017/06/29 - Lance Wilson:  Added comments.
#   2017/07/31 - Lance Wilson:  Added check for if there are no matching files.
#   2017/08/23 - Lance Wilson:  Added correct to check for help message.
#   2017/11/01 - Lance Wilson:  Added support for a whitest pixel with value
#                               less than 255 and error handling for occasions
#                               when there is not a pixel that meets the
#                               specified threshold for whiteness. Updated help
#                               message and comments.
#   2017/11/20 - Lance Wilson:  Added preliminary calculations of the actual
#                               width of the drop in each image. Added
#                               calculation for when there is only one row that
#                               meets the whiteness threshold.
#   2018/04/20 - Lance Wilson:  Changed the ratio of the values to um/pixel,
#                               calculated the actual drop widths (um) based on
#                               the standard calibrations for the instruments,
#                               updated header.
#   2018/10/31 - Lance Wilson:  Changed re.search to re.match when finding the
#                               relative dates and times so that it only looks
#                               for a match at the beginning of the file name
#                               (avoids an issue where, for example, 2018 would
#                               match 201706242018).
#   2018/11/01 - Lance Wilson:  Added comments and prepared for upload to ADPAA.
#
# Verification of Data:
#   [Pending]
#
# Copyright 2016, 2017, 2018 Lance Wilson, David Delene
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

from PIL import Image
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import re
from scipy import stats
import sys

def help_message():
    print '------------------------------------------------------------------'
    print 'SYNTAX:'
    print ('Syntax (single file): python cdp_camera_diameter.py ImageFile.jpg '
           '[Brightness Threshold] [Init. Drop Width] [Save Path]')
    print
    print ('Syntax (multiple files): python cdp_camera_diameter.py Date-Time '
           '[Brightness Threshold] [Init. Drop Width] [Save Path]')
    print '------------------------------------------------------------------'
    print 'EXAMPLES:'
    print 'Example: python cdp_camera_diameter.py 201705261752 252'
    print
    print 'Example 2: python cdp_camera_diameter.py 201705261752 255 28'
    print '------------------------------------------------------------------'
    print 'VARIABLE DEFINITIONS:'
    print ('\tImageFile.jpg/Date-Time: the dates and times of images to be '
           'used for the calculation of the mean diameter and the creation of '
           'the plot, anywhere from one file to years worth of data.')
    print ('\tFor example, 20170526181121241.jpg will use just that file, '
           'while 2017 will match all files starting with 2017 (that is, all '
           'data in the directory from 2017).')
    print
    print ('\tBrightness Threshold (optional): The brightness intensity '
           '(0-255) to use as the brightest boundary of the drop (default: '
           '255).')
    print
    print ('\tInitial Drop Width (optional): The expected width of a drop in '
           'micrometers. This is generally included in the name of the '
           'directory: for example, und15 would expect a value of 15.0 '
           '(default: 15.0).')
    print
    print ('\tSave Path (optional): The directory in which to save the plot '
           'of the drop diameters over time (default: \'./\' {the current '
           'directory}.)')
    print '------------------------------------------------------------------'
    print ('Note: to get a proper name for the output file, it is recommended'
           ' that this program be run from the directory containing the data '
           '(as of 2018/11/01).')
    print '------------------------------------------------------------------'

if (len(sys.argv) < 2):
  help_message()
  exit()

for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

# The brightness intensity used as the brightest boundary of the drop.
brightness_threshold = 255
if (len(sys.argv) > 2):
    brightness_threshold = int(sys.argv[2])

# The expected width of the drop in micrometers.
init_drop_width = 15.0
if (len(sys.argv) > 3):
    init_drop_width = float(sys.argv[3])

# The directory path leading to where the plot should be saved.
path = './'
if (len(sys.argv) > 4):
    path = sys.argv[4]
    if not path.endswith('/'):
        path = path + '/'

# The dates and times of images to be used for the calculation of the mean
#   diameter and the creation of the plot.
imagetime = str(sys.argv[1])
allfile = sorted(os.listdir('.'))
filelist = []
# Find all files in the directory that start with the imagetime.
for picture in allfile:
    if (re.match(imagetime, picture)):
        filelist.append(picture)

if not filelist:
    print 'No files with this prefix.'
    exit()

# Output header information.
print 'Mean Pixel Widths for Date and Time ' + imagetime.split('.')[0] + ':'
print 'Time' + '\t\t\tMean Width\tMin Width\tMax Width\tum/Pixel'

pixel_conversion = 0.775 # um/pixel

pixel_means = []
drop_sizes = []
for imagefile in filelist:
    time = imagefile.split('.')[0]
    im = Image.open(imagefile)

    # Convert image to array.
    pixel_arr = np.array(im)

    # We only really want to calculate distances where there is an obvious axis;
    #   Uses the brightness threshold for this value.
    #   First index of this return is an array of rows with white pixels.
    #   (The second index would be the columns where this is true.)
    search_area = np.where(pixel_arr >= brightness_threshold)[0]
    if search_area.any():
        start = search_area[0]
        end = search_area[-1]
    else:
        print time + '\tNo pixels meet the brightness threshold for this file.'
        continue
    # If there is only one bright value, increment end so that the array will
    #   have length 1.
    if (start == end):
        end = end + 1

    # Create empty array for the set of pixel distances.
    pixel_distance = np.empty(shape=[end-start])
    # Variable for the rows within the search area that have a maximum
    #   brightness intensity that is less than the specified threshold.
    low_between_rows = 0

    for row in range(start, end):
    ##for row in search_area:
        index = row - start - low_between_rows

        # Ignore the rows that are within the search area but have a maximum
        #   brightness intensity less than the specified threshold.
        if max(pixel_arr[row]) < brightness_threshold:
            low_between_rows += 1
            # Replace the initial pixel_distance array with one that is one
            #   element smaller, but contains the already calculated values.
            pixel_distance_replace = np.empty(shape=[len(pixel_distance)-1])
            pixel_distance_replace[0:index] = pixel_distance[0:index]
            pixel_distance = np.copy(pixel_distance_replace)
            continue

        # Find the locations of the brightest pixels in each row.
        max_indices = np.where(pixel_arr[row] == brightness_threshold)[0]
        # If there are too many values that exceed the brightness threshold
        #   there will not be a discrete maximum, and will result in errors in
        #   later calculations.
        if (len(max_indices) > 7):
            print time + '\tThe brightness threshold is too low to obtain\n'+\
                  '\t\t\tvalid data. (Brightest area is too wide.)'
            break
        # Set up arrays for the two halves of the picture.
        left_arr = pixel_arr[row][:max_indices[0]-5]
        right_arr = pixel_arr[row][max_indices[-1]+5:]

        # Check to see if the secondary brightness axis is to the left or the
        #   right of the main one.
        if (max(left_arr) > max(right_arr)):
            other_max = max(left_arr)
            out_index = 0
        else:
            other_max = max(right_arr)
            out_index = -1

        # Find the location of the secondary maximum.
        second_index = np.where(pixel_arr[row] == other_max)[0]
        pixel_distance[index] = math.fabs(max_indices[len(max_indices)/2] - second_index[out_index])

    # Need a second check of whether there is a discrete maximum, otherwise
    #   the bad data will be printed out.
    if (len(max_indices) <= 5):
        print time + '\t%2.5f' % np.mean(pixel_distance) + '\t' +\
              str(min(pixel_distance)) + '\t\t' + str(max(pixel_distance))\
              + '\t\t%2.3f' % (init_drop_width/np.mean(pixel_distance))
        pixel_means.append(init_drop_width/np.mean(pixel_distance))
        drop_sizes.append(np.mean(pixel_distance)*pixel_conversion)

print 'Valid values:        %5d' % len(pixel_means)
print 'Mean (um/pixel):     %2.3f' % np.mean(pixel_means)
print 'Standard Deviation:  %2.3f' % np.std(pixel_means)
print 'Mean Size (um):      %2.3f' % np.mean(drop_sizes)
print 'Standard Deviation:  %2.3f' % np.std(drop_sizes)

# Currently getting the origin of the data from the working directory.
drop_label = os.getcwd().split('/')[-1]

x_range = np.arange(len(drop_sizes))
plt.scatter(x_range, drop_sizes)
m, b, r_value, p_value, std_err = stats.linregress(x_range, drop_sizes)
y_values = m * x_range + b
plt.plot(x_range, y_values, color='red', label=('r = %.2f' % r_value))
plt.title('Drops from ' + drop_label + ' with Diameter %.3f $\mathregular{\mu}$m $\mathregular{\pm}$ %.3f $\mathregular{\mu}$m\nTime Range from ' % (np.mean(drop_sizes), np.std(drop_sizes)) + filelist[0].split('.')[0] + ' to ' + filelist[-1].split('.')[0])
plt.xlabel('Relative time (s)')
plt.xlim(-25,len(drop_sizes)+25)
plt.ylabel('Droplet Diameter ($\mathregular{\mu}$m)')
plt.legend()
plt.savefig(path + 'DropSize' + drop_label + '.png', dpi=400)
