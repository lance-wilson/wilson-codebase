#!/usr/bin/env python3
#
# Name:
#   lab1_LWilson_display.py
#
# Purpose:
#   To display an AVHRR image.
#
# Syntax:
#   python lab1_LWilson_display.py
#
#   Input: None.
#
#   Output: An image based on the data.
#
# Modification History:
#   2020/01/30 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

num_pixels = 500
num_lines = 500

# Get data from file, setting the type to bytes, and reshape based on the
#   number of pixels and lines.
data = (np.fromfile('lac_95236.S1707.CAL_TK.2', dtype=np.ubyte).reshape(num_pixels, num_lines))*100./255.
#data2 = np.fromfile('lac_95236.S1707.CAL_TK.2', dtype='b').reshape(num_pixels, num_lines)
#data3 = np.fromfile('lac_95236.S1707.CAL_TK.2', dtype='b')*100./255.
#data4 = np.fromfile('lac_95236.S1707.CAL_TK.2', dtype='b')

# Plot the image.
plt.imshow(data, origin='lower')
plt.show()

