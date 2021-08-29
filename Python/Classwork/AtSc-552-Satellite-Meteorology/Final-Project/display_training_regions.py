#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   display_training_regions.py
#
# Purpose:
#   Display colored blocks in the regions used for training.
#
# Syntax:
#   python display_training_regions.py file_name bands
#   (Anaconda): runfile('{Path_to_file}/display_training_regions.py', args='file_name bands', wdir='{Path_to_file}')
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/04/18 - Lance Wilson:  Created.

from get_hdf4_data import read_hdf_file
import glob
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print('Syntax: python display_training_regions.py filename band1 [bandn]')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/display_training_regions.py\', args=\'filename band1 [bandn]\', wdir=\'{Path_to_file}\')')
    print('Note that bands 13 and 14 must have a specified sensitivity')
    print('E.g. 13lo or 13hi')
    sys.exit()

if len(sys.argv) <= 3:
    help_message()
    
filename = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'
#filename = sys.argv[1]
training_set = sys.argv[2]
band_names = sys.argv[3:]

# Wavelength midpoints are provided in the same order as in the combined set of
#   all data bands.
wavelengths_um = [0.645, 0.8585, 0.469, 0.555, 1.24, 1.64, 2.13, .4125, 0.443, 0.488, 0.531, 0.551, 0.667, 0.667, 0.678, 0.678, 0.748, 0.8695, 0.905, 0.936, 0.94, 1.375, 3.75, 3.959, 3.959, 4.05, 4.4655, 4.5155, 6.715, 7.325, 8.55, 9.73, 11.03, 12.02, 13.335, 13.635, 13.935, 14.235]

all_bands, all_band_names, all_scales, all_offsets, valid_range = read_hdf_file(filename)

try:
    # Find the index where the required bands are located.
    red_band_index = all_band_names.index(band_names[0])
    green_band_index = all_band_names.index(band_names[1])
    blue_band_index = all_band_names.index(band_names[2])
except ValueError:
    print('Band was not found in file')
    help_message()

# Get data for just the bands needed.
red_band_counts = all_bands[red_band_index]
green_band_counts = all_bands[green_band_index]
blue_band_counts = all_bands[blue_band_index]

# Apply reflectance/radiance scale and offset for red band.
red_band = all_scales[red_band_index] * (red_band_counts - all_offsets[red_band_index])
# Convert data to a 0 to 255 range.
red_max_value = all_scales[red_band_index] * (valid_range[1] - all_offsets[red_band_index])
red_min_value = all_scales[red_band_index] * (valid_range[0] - all_offsets[red_band_index])
red_range = red_max_value - red_min_value
red_band_brightness = red_band * 255./red_range
# Mask bad data for red band.
red_band_masked = np.ma.masked_where(red_band_counts > valid_range[1], red_band_brightness)

# Apply reflectance/radiance scale and offset for green band.
green_band = all_scales[green_band_index] * (green_band_counts - all_offsets[green_band_index])
# Convert data to a 0 to 255 range.
green_max_value = all_scales[green_band_index] * (valid_range[1] - all_offsets[green_band_index])
green_min_value = all_scales[green_band_index] * (valid_range[0] - all_offsets[green_band_index])
green_range = green_max_value - green_min_value
green_band_brightness = green_band * 255./green_range
# Mask bad data for green band.
green_band_masked = np.ma.masked_where(green_band_counts > valid_range[1], green_band_brightness)

# Apply reflectance/radiance scale and offset for blue band.
blue_band = all_scales[blue_band_index] * (blue_band_counts - all_offsets[blue_band_index])
# Convert data to a 0 to 255 range.
blue_max_value = all_scales[blue_band_index] * (valid_range[1] - all_offsets[blue_band_index])
blue_min_value = all_scales[blue_band_index] * (valid_range[0] - all_offsets[blue_band_index])
blue_range = blue_max_value - blue_min_value
blue_band_brightness = blue_band * 255./blue_range
# Mask bad data for blue band.
blue_band_masked = np.ma.masked_where(blue_band_counts > valid_range[1], blue_band_brightness)

# Combine three channels into one array that can be plotted as a color image.
rgbArray = np.ma.zeros((all_bands[0].shape[0],all_bands[0].shape[1],3), 'uint8')
rgbArray[:,:,0] = red_band_masked
rgbArray[:,:,1] = green_band_masked
rgbArray[:,:,2] = blue_band_masked

# Get a list of files containing signatures.
signature_files = glob.glob('Signature_Files/signatures_class{:s}_*.txt'.format(training_set))
info_classes = [filename.split('.')[0].split('_')[-1] for filename in signature_files]

# Color table with RGB values matches the labels in color_table2
#   These can be found with np.array(matplotlib.colors.to_rgb(color))*255
color_table = np.array([[255,0,0], [0,0,255], [0,128,0], [128,0,128], [255,165,0], [255,192,203], [255,255,0], [0,0,0]])
#color_table = np.array([[127,127,127], [0,0,120], [0,0,255], [0,255,0], [255,255,0], [255,50,0], [255,0,0], [255,255,255]])/255
color_table2 = np.array(['red', 'blue', 'green', 'purple', 'orange', 'pink', 'yellow', 'black'])

# List of actual indices in the color_table.
x_vals = np.linspace(0, len(color_table)-1, len(color_table))
# List of indices where the color values should be interpolated.
x_vals_interp = np.linspace(0, len(color_table)-1, len(signature_files))

# Interpolate the color table so that there are as many color values as the
#   user specified.
color_table_interp = np.empty((len(signature_files),3), 'uint8')
for i in range(3):
    color_table_interp[:,i] = np.interp(x_vals_interp, x_vals, color_table[:,i])

handles = []
for i, filename in enumerate(signature_files):
    signature_indices = np.loadtxt(filename).astype(np.int)
    
    #if len(signature_indices) == 2:
    #    signature_indices = signature_indices.reshape((1,2))

    for pair in signature_indices:
        rgbArray[pair[0], pair[1], :] = np.ma.array(color_table[i])
    
    #plt.plot(0,0, c=color_table2[i], label=info_classes[i])
    handles.append(mlines.Line2D([], [], color=color_table2[i], marker='.',  markersize=15))
    
plt.imshow(rgbArray)
plt.legend(handles=handles, labels=info_classes, handlelength=0.5, loc=(1.04,0.5), ncol=1)
#plt.legend(handlelength=0.5, loc=(1.04,0.5))
plt.savefig('training_map_set{:s}.png'.format(training_set), dpi=800)

