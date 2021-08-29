#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_lab4_section3.py
#
# Purpose:
#   Plot an RGB true color image using three MODIS bands.
#
# Syntax:
#   python LWilson_lab4_section3.py red_band green_band blue_band
#   (Anaconda): runfile('{Path_to_file}/LWilson_lab4_section3_true.py', args='red_band green_band blue_band', wdir='{Path_to_file}')
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/03/28 - Lance Wilson:  Created.

from PIL import Image
from pyhdf.SD import *
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print('Syntax: python lab4_section3.py red_band green_band blue_band')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/LWilson_lab4_section3_true.py\', args=\'red_band green_band blue_band\', wdir=\'{Path_to_file}\')')
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

if len(sys.argv) <= 3:
    help_message()
    
red_band_name = sys.argv[1]
green_band_name = sys.argv[2]
blue_band_name = sys.argv[3]

filename = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'

# Wavelength midpoints are provided in the same order as in the combined set of
#   all data bands.
wavelengths_um = [0.645, 0.8585, 0.469, 0.555, 1.24, 1.64, 2.13, .4125, 0.443, 0.488, 0.531, 0.551, 0.667, 0.667, 0.678, 0.678, 0.748, 0.8695, 0.905, 0.936, 0.94, 1.375, 3.75, 3.959, 3.959, 4.05, 4.4655, 4.5155, 6.715, 7.325, 8.55, 9.73, 11.03, 12.02, 13.335, 13.635, 13.935, 14.235]

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
    # Find the index where the required bands are located.
    red_band_index = all_band_names.index(red_band_name)
    green_band_index = all_band_names.index(green_band_name)
    blue_band_index = all_band_names.index(blue_band_name)
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
img = Image.fromarray(rgbArray)
img.save('LWilson_lab4_truecolor_bands_{:s}_{:s}_{:s}.png'.format(red_band_name, green_band_name, blue_band_name))

# Plot the individual colors with the combined form.
fig = plt.figure()
fig.add_subplot(221)
plt.imshow(red_band_masked, cmap='Reds', vmin = 0, vmax = 255)
plt.title('Red')

fig.add_subplot(222)
plt.imshow(green_band_masked, cmap='Greens', vmin = 0, vmax = 255)
plt.title('Green')

fig.add_subplot(223)
plt.imshow(blue_band_masked, cmap='Blues', vmin = 0, vmax = 255)
plt.title('Blue')

fig.add_subplot(224)
plt.imshow(rgbArray, vmin = 0, vmax = 255)
plt.title('True Color')

plt.savefig('LWilson_lab4_truecolor_components.png', dpi=400)
#plt.show()