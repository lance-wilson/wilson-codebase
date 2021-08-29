#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   lab3_problem2.py
#
# Purpose:
#   Take a 2D image and increase the contrast using histogram equalization.
#
# Syntax:
#   python lab3_problem2.py imagefile
#
# Modification History:
#   2020/03/06 - Lance Wilson:  Created.

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys

y1 = 0
y2 = 255

if len(sys.argv) <= 1:
    print('Syntax: python lab3_problem2.py imagefile')
    exit()

# Open the image, convert it to grayscale (if necessary), and convert it to a numpy array.
picture = Image.open(sys.argv[1]).convert('L')
data = np.array(picture)

num_pixels = data.size
num_brightness = y2-y1+1

equalized_data = np.empty(data.shape)
histogram = np.zeros(num_brightness)
cumulative_histogram = np.zeros(num_brightness)
new_brightness = np.empty(num_brightness)

# First get the regular histogram of the image.
for row in data:
    for value in row:
        histogram[value] += 1

# Calculate the cumulative histogram.
# Using the hard coded version since it timed the fastest (~1e-4 vs 6e-4).
histogram_sum = 0
for i in range(len(cumulative_histogram)):
    histogram_sum += histogram[i]
    cumulative_histogram[i] += histogram_sum

# Calculate the new brightness values.
for (k, value) in enumerate(cumulative_histogram):
    new_brightness[k] = round(((num_brightness-1.)/num_pixels) * value)

# Use the new brightness values corresponding to each old value to get the new
#   equalized image.
for (m, row) in enumerate(data):
    for (n, value) in enumerate(row):
        equalized_data[m,n] = new_brightness[value]

# Plot the images side-by-side for comparison.
fig = plt.figure()
fig.add_subplot(121)
# Use the came max and min value for the colormap for both images to show the
#   difference in contrast.
plt.imshow(data, cmap='gray', vmin = y1, vmax = y2)
plt.title('Original')

fig.add_subplot(122)
plt.imshow(equalized_data, cmap='gray', vmin = y1, vmax = y2)
plt.title('Histogram Equalized')

plt.savefig('lab3_histogram_equalized.png', dpi=400)
#plt.show()

