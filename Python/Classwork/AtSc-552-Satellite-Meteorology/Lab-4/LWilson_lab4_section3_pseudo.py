#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_lab4_section3_pseudo.py
#
# Purpose:
#   Plot a pseudocolor image of a band of MODIS data.
#
# Syntax:
#   python LWilson_lab4_section3_pseudo.py band number_colors
#   (Anaconda): runfile('{Path_to_file}/LWilson_lab4_section3_pseudo.py', args='band number_colors', wdir='{Path_to_file}')
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/03/29 - Lance Wilson:  Created.

from PIL import Image
from pyhdf.SD import *
import numpy as np
import sys

def help_message():
    print('Syntax: python LWilson_lab4_section3_pseudo.py band number_colors')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/LWilson_lab4_section3_pseudo.py\', args=\'band number_colors\', wdir=\'{Path_to_file}\')')
    print('Note that bands 13 and 14 must have a specified sensitivity')
    print('E.g. 13lo or 13hi')
    sys.exit()
    
def calc_brightness_temp(radiance, wavelength_um):
    h = 6.626e-34      #Planck's  Constant
    k = 1.381e-23      #Boltzmann's Constant
    c = 2.988e8        #Speed of Light
    
    wavelength_meters = wavelength_um * 1e-6

    term1 = (2. * h * c**2)/(radiance * wavelength_meters**4 * wavelength_um)
    term2 = np.log(term1 + 1)
    term3 = (h*c)/(k*wavelength_meters)
    brightness_temp = term3/term2
    return brightness_temp

if len(sys.argv) <= 2:
    help_message()
    
band_name = sys.argv[1]
number_colors = int(sys.argv[2])

filename = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'

# Wavelength midpoints are provided in the same order as in the combined set of
#   all data bands.
wavelengths_um = [0.645, 0.8585, 0.469, 0.555, 1.24, 1.64, 2.13, .4125, 0.443, 0.488, 0.531, 0.551, 0.667, 0.667, 0.678, 0.678, 0.748, 0.8695, 0.905, 0.936, 0.94, 1.375, 3.75, 3.959, 3.959, 4.05, 4.4655, 4.5155, 6.715, 7.325, 8.55, 9.73, 11.03, 12.02, 13.335, 13.635, 13.935, 14.235]

# Set up a starting list of colors that will be used in the final image.
#   Based on the colors in the powerpoint.
color_table = np.array([[127,127,127], [0,0,120], [0,0,255], [0,255,0], [255,255,0], [255,50,0], [255,0,0], [255,255,255]])

# List of actual indices in the color_table.
x_vals = np.linspace(0, len(color_table)-1, len(color_table))
# List of indices where the color values should be interpolated.
x_vals_interp = np.linspace(0, len(color_table)-1, number_colors)

# Interpolate the color table so that there are as many color values as the
#   user specified.
color_table_interp = np.empty((number_colors,3), 'uint8')
for i in range(3):
    color_table_interp[:,i] = np.interp(x_vals_interp, x_vals, color_table[:,i])

# Open the HDF4 file.
hdffile = SD(filename)

# Get the data for the reflective bands at 1 km resolution.
bands_8to19and26_obj = hdffile.select('EV_1KM_RefSB')
bands_8to19and26 = bands_8to19and26_obj.get()
band_names_8to19and26 = bands_8to19and26_obj.attributes()['band_names']

# Get the data for the thermal emissive bands at 1 km resolution.
bands_20to36_obj = hdffile.select('EV_1KM_Emissive')
bands_20to36 = bands_20to36_obj.get()
band_names_20to36 = bands_20to36_obj.attributes()['band_names']

# Get the data for the reflective bands aggregated from 500 m resolution.
bands_3to7_obj = hdffile.select('EV_500_Aggr1km_RefSB')
bands_3to7 = bands_3to7_obj.get()
band_names_3to7 = bands_3to7_obj.attributes()['band_names']

# Get the data for the reflective bands aggregated from 500 m resolution.
bands_1to2_obj = hdffile.select('EV_250_Aggr1km_RefSB')
bands_1to2 = bands_1to2_obj.get()
band_names_1to2 = bands_1to2_obj.attributes()['band_names']

all_bands = np.concatenate((bands_1to2,bands_3to7,bands_8to19and26,bands_20to36))
all_band_names = (band_names_1to2 + ',' + band_names_3to7 + ',' + band_names_8to19and26 + ',' + band_names_20to36).split(',')

# Combine all the scaling and offset values into one list so they can be more
#   easily accessed later.
all_scales = bands_1to2_obj.attributes()['reflectance_scales'] + bands_3to7_obj.attributes()['reflectance_scales'] + bands_8to19and26_obj.attributes()['reflectance_scales'] + bands_20to36_obj.attributes()['radiance_scales']
all_offsets = bands_1to2_obj.attributes()['reflectance_offsets'] + bands_3to7_obj.attributes()['reflectance_offsets'] + bands_8to19and26_obj.attributes()['reflectance_offsets'] + bands_20to36_obj.attributes()['radiance_offsets']

# Just taking the ones for band 1 and 2 because they should all be the same.
valid_range = bands_1to2_obj.attributes()['valid_range']

try:
    # Find the index where the required band is located.
    band_index = all_band_names.index(band_name)
except ValueError:
    print('Band was not found in file')
    help_message()

# Get data for just the required band.
band_counts = all_bands[band_index]

# Apply reflectance/radiance scale and offset for band.
band = all_scales[band_index] * (band_counts - all_offsets[band_index])
# Convert data to a 0 to 255 range.
max_value = all_scales[band_index] * (valid_range[1] - all_offsets[band_index])
min_value = all_scales[band_index] * (valid_range[0] - all_offsets[band_index])
value_range = max_value - min_value
band_brightness = band * 255./value_range
# Mask bad data for band.
band_masked = np.ma.masked_where(band_counts > valid_range[1], band_brightness)

# Brightness value thresholds to divide the original brightness data.
v1 = np.linspace(0, 255, number_colors+1, endpoint=True)

# Set up the array to hold RGB values to be plotted.
rgbArray = np.ma.zeros((all_bands[0].shape[0],all_bands[0].shape[1],3), 'uint8')
# Modify the color values so that there are only the set number of colors in
#   the final output.
for i in range(number_colors):
    subset = np.where((band_masked < v1[i+1]) & (band_masked >= v1[i]))
    row_indices = subset[0]
    column_indices = subset[1]
    rgbArray[row_indices,column_indices,:] = color_table_interp[i]

# Combine three channels into one array that can be plotted as a color image.
img = Image.fromarray(rgbArray)
img.save('LWilson_lab4_pseudocolor_band_{:s}_{:d}colors.png'.format(band_name, number_colors))
