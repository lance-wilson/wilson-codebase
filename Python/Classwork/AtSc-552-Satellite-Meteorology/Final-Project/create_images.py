#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   hdf4_to_image.py
#
# Purpose:
#   Convert data from various bands in HDF4 file to an image.
#
# Syntax:
#   python hdf4_to_image.py file_name bands
#   (Anaconda): runfile('{Path_to_file}/hdf4_to_image.py', args='file_name bands', wdir='{Path_to_file}')
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/04/04 - Lance Wilson:  Created.

from get_hdf4_data import read_hdf_file
#from get_hdf4_data import calc_brightness_temp
from PIL import Image
import numpy as np
import sys

def help_message():
    print('Syntax: python create_images.py filename band1 [bandn]')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/create_images.py\', args=\'filename band1 [bandn]\', wdir=\'{Path_to_file}\')')
    print('Note that bands 13 and 14 must have a specified sensitivity')
    print('E.g. 13lo or 13hi')
    sys.exit()

if len(sys.argv) <= 2:
    help_message()
    
#filename = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'
filename = sys.argv[1]
band_names = sys.argv[2:]

data_label = filename.split('.')[1]

# Wavelength midpoints are provided in the same order as in the combined set of
#   all data bands.
wavelengths_um = [0.645, 0.8585, 0.469, 0.555, 1.24, 1.64, 2.13, .4125, 0.443, 0.488, 0.531, 0.551, 0.667, 0.667, 0.678, 0.678, 0.748, 0.8695, 0.905, 0.936, 0.94, 1.375, 3.75, 3.959, 3.959, 4.05, 4.4655, 4.5155, 6.715, 7.325, 8.55, 9.73, 11.03, 12.02, 13.335, 13.635, 13.935, 14.235]

all_bands, all_band_names, all_scales, all_offsets, valid_range = read_hdf_file(filename)

for band_name in band_names:
    try:
        # Find the index where the band is located.
        band_index = all_band_names.index(band_name)
    except ValueError:
        print('Band {:s} was not found in file'.format(band_name))
        help_message()
    
    # Get data for this band.
    band_counts = all_bands[band_index]
    
    # Apply reflectance/radiance scale and offset for this band.
    band = all_scales[band_index] * (band_counts - all_offsets[band_index])
    # Convert data to a 0 to 255 range.
    max_value = all_scales[band_index] * (valid_range[1] - all_offsets[band_index])
    min_value = all_scales[band_index] * (valid_range[0] - all_offsets[band_index])
    band_range = max_value - min_value
    band_brightness = band * 255./band_range
    # Mask bad data.
    band_masked = np.ma.masked_where(band_counts > valid_range[1], band_brightness)
    
    img = Image.fromarray(band_masked.astype('uint8'))
    img.save('Training_Images/training{:s}_band_{:s}_{:f}um.png'.format(data_label, band_name, wavelengths_um[band_index]))