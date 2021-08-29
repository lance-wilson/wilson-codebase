#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   convert_data2image.py
#
# Purpose:
#   Take the data from AVHRR channel 1 and output an image that can be read by
#   future programs.
#
# Syntax:
#   python convert_data2image.py
#
#   Input: None.
#
#   Output: An image based on the data.
#
# Modification History:
#   2020/03/05 - Lance Wilson:  Created.

from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy

num_pixels = 500
num_lines = 500

# Get data from file, setting the type to bytes, and reshape based on the
#   number of pixels and lines.
# For this lab, leaving the original brightness values intact.
data = (np.fromfile('../Lab 2/lac_95236.S1707.CAL_TK.1', dtype=np.ubyte).reshape(num_pixels, num_lines))

im = Image.fromarray(data).transpose(method=Image.FLIP_TOP_BOTTOM)
im.save('channel.png')
