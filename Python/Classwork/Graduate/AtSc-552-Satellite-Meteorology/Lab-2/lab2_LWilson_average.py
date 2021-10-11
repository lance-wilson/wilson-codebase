#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   lab2_LWilson_average.py
#
# Purpose:
#   Create a spatial average of AVHRR channel 1 of any given size.
#
# Syntax:
#   python lab2_LWilson_average.py new_pixel_size
#
#   Input: None.
#
#   Output: An image based on the data.
#
# Modification History:
#   2020/02/14 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np
import sys

num_pixels = 500
num_lines = 500

def help_message():
    print('Syntax: lab2_LWilson_average.py new_pixel_size')
    print('\tNew pixel size must be an integer between 1 and {:d}'.format(min([num_pixels, num_lines])))
    exit()

# See if the user asked for help.
for arg in sys.argv:
    if '-h' in arg or '-H' in arg:
        help_message()

if len(sys.argv) < 2:
    help_message()

# Check that the argument can be interpreted as an integer.
try:
    new_pixel_size = int(sys.argv[1])
except ValueError:
    print('New Pixel Size was not an integer.')
    help_message()

# Check if the averaging size is not smaller than one pixel or larger than the full image.
if new_pixel_size < 1 or new_pixel_size > num_pixels or new_pixel_size > num_lines:
    print('New pixel size outside of acceptable range')
    help_message()

# Get data from file, setting the type to bytes, and reshape based on the
#   number of pixels and lines.
data = (np.fromfile('lac_95236.S1707.CAL_TK.1', dtype=np.ubyte).reshape(num_pixels, num_lines))*100./255.

avg_num_rows = int(num_pixels/new_pixel_size)
avg_num_pixels = int(num_lines/new_pixel_size)

# Create an array to hold the averaged data.
averaged_data = np.empty([avg_num_rows, avg_num_pixels])

# Loop over both rows and pixels in each row.
for i in range(avg_num_rows):
    for n in range(avg_num_pixels):
        # Grab a chunk of data containing the pixels to be averaged.
        data_chunk = data[new_pixel_size*i:new_pixel_size*i + new_pixel_size,new_pixel_size*n:new_pixel_size*n + new_pixel_size]
        # Calculate the average of the pixels in the chunk. 
        sum_value = 0
        for row in data_chunk:
            for value in row:
                sum_value += value
        average_value = sum_value/data_chunk.size
        averaged_data[i,n] = average_value

# Plot the images side-by-side for comparison.
# vmin and vmax are set arbitrarily to ensure that the images have the same scale.
fig = plt.figure()
fig.add_subplot(121)
plt.imshow(data, origin='lower', vmin = 0, vmax = 45)
plt.title('Original')

fig.add_subplot(122)
plt.imshow(averaged_data, origin='lower', vmin = 0, vmax = 45)
plt.title('Spatially Averaged')

plt.savefig('lab2_LWilson_spatial_average.png', dpi=400)
#plt.show()

