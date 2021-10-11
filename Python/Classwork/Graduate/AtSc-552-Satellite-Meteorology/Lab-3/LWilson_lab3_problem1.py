#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   lab3_problem1.py
#
# Purpose:
#   Take a 2D image and increase the contrast using linear contrast stretching.
#
# Syntax:
#   python lab3_problem1.py imagefile
#
# Modification History:
#   2020/03/05 - Lance Wilson:  Created.

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys

y1 = 0
y2 = 255

if len(sys.argv) <= 1:
    print('Syntax: python lab3_problem1.py imagefile')
    exit()

# Open the image, convert it to grayscale if necessary.
picture = Image.open(sys.argv[1]).convert('L')
#picture = Image.open(sys.argv[1])
data = np.array(picture)

old_min = np.min(data)
old_max = np.max(data)

stretched_data = np.empty(data.shape)

# Use the linear contrast stretch formula to create a new image array.
for (i, row) in enumerate(data):
    for (j, value) in enumerate(row):
        stretched_data[i,j] = y1 + (y2 - y1) * (value - old_min)/(old_max - old_min)

# Plot the images side-by-side for comparison.
fig = plt.figure()
fig.add_subplot(121)
# Use the same max and min value for the colormap for both images to show the
#   difference in contrast.
#plt.imshow(data, origin='lower', cmap='gray', vmin = y1, vmax = y2)
plt.imshow(data, cmap='gray', vmin = y1, vmax = y2)
plt.title('Original')

fig.add_subplot(122)
#plt.imshow(stretched_data, origin='lower', cmap='gray', vmin = y1, vmax = y2)
plt.imshow(stretched_data, cmap='gray', vmin = y1, vmax = y2)
plt.title('Linear Contrast Stretch')

plt.savefig('lab3_contrast_stretch.png', dpi=400)
#plt.show()

