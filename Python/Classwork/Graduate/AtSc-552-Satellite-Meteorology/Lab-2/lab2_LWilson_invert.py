#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   lab2_LWilson_invert.py
#
# Purpose:
#   Create a vertically inverted image of AVHRR data.
#
# Syntax:
#   python lab2_LWilson_invert.py
#
#   Input: None.
#
#   Output: The inverted image.
#
# Modification History:
#   2020/02/14 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

num_pixels = 500
num_lines = 500

# Get data from file, setting the type to bytes, and reshape based on the
#   number of pixels and lines.
data = (np.fromfile('lac_95236.S1707.CAL_TK.1', dtype=np.ubyte).reshape(num_pixels, num_lines))*100./255.

# Allocate array for the inverted data.
inverted_data = np.empty([num_lines, num_pixels])

last_index = len(data) - 1

for row in range(last_index + 1):
    inverted_data[row] = data[last_index-row]

# Plot the images side-by-side for comparison.
fig = plt.figure()
fig.add_subplot(121)
plt.imshow(data, origin='lower')
plt.title('Original')

fig.add_subplot(122)
plt.imshow(inverted_data, origin='lower')
plt.title('Inverted')

plt.savefig('lab2_LWilson_invert.png', dpi=400)
#plt.show()

