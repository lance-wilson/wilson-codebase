#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   create_signatures.py
#
# Purpose:
#   Get the indices in an image that are signatures of a particular
#   informational class.
#
# Syntax:
#   python create_signatures.py filename mode info_class
#
# Modification History:
#   2020/04/11 - Lance Wilson:  Created.

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
import sys

def help_message():
    print('Syntax: python create_signatures.py filename mode info_class training_set')
    print('Modes: box or pixels')
    sys.exit()

if len(sys.argv) <= 3:
    help_message()

filename = 'Training_Images/' + sys.argv[1]
mode = sys.argv[2]
info_class = sys.argv[3]
training_set = sys.argv[4]

#band = filename.split('.')[0].split('_')[2]

picture = Image.open(filename).convert('L')
data = np.array(picture)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(data, cmap='gray')

coords = []

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata

    global coords
    # Reversing order so that it can be accessed better by arrays later.
    coords.append((iy, ix))

    return

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()

#fig.canvas.mpl_disconnect(cid)

# Define the signature region using four corners.
if (mode == 'box'):
    points = np.asarray(coords[-4:])
    xmax = int(np.round(np.max(points[:,0])))
    xmin = int(np.round(np.min(points[:,0])))
    ymax = int(np.round(np.max(points[:,1])))
    ymin = int(np.round(np.min(points[:,1])))
    path = Path(points)
    poss_points = np.array([(i,j) for i in range(xmin,xmax) for j in range(ymin,ymax)])
    signature_indices = poss_points[np.where(path.contains_points(poss_points))]

# Define the signature by clicking each pixel.
if (mode == 'pixels'):   
    zooms = input('# of Zooms (-1 to cancel):')
    signature_indices = np.array(coords[int(zooms):])
    if zooms == '-1':
        exit()

#np.savetxt('signatures_band{:s}_class{:s}.txt'.format(band, info_class), signature_indices, fmt='%d')
np.savetxt('Signature_Files/signatures_class{:s}_{:s}.txt'.format(training_set, info_class), signature_indices, fmt='%d')
    
