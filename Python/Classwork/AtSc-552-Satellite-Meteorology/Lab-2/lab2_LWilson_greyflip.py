#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   lab2_LWilson_greyflip.py
#
# Purpose:
#   Grey flip the data in AVHRR channel 4.
#
# Syntax:
#   python lab2_LWilson_greyflip.py
#
#   Input: None.
#
#   Output: An image based on the data.
#
# Modification History:
#   2020/02/14 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

num_pixels = 500
num_lines = 500

# Get data from file, setting the type to bytes, and reshape based on the
#   number of pixels and lines.
data = (np.fromfile('lac_95236.S1707.CAL_TK.4', dtype=np.ubyte).reshape(num_pixels, num_lines))*100./255. + 180.

flipped_data = 255. - data

# Plot the images side-by-side for comparison.
fig = plt.figure()
fig.add_subplot(121)
plt.imshow(data, origin='lower', cmap='gray')#, vmin = 180, vmax = 330)
plt.title('Original')

fig.add_subplot(122)
plt.imshow(flipped_data, origin='lower', cmap='gray')#, vmin = 180, vmax = 330)
plt.title('Flipped')

plt.savefig('lab2_LWilson_greyflip.png', dpi=400)
#plt.show()
