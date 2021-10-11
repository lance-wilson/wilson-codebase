#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_lab4_section2.py
#
# Purpose:
#   Calculate the mean and variance of the reflectance of band 2 and the
#   radiance of band 32 of MODIS.
#
# Syntax:
#   python LWilson_lab4_section2.py
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/03/26 - Lance Wilson:  Created.

from LWilson_lab4_mean_func import mean_func
from LWilson_lab4_variance import variance_func
from pyhdf.SD import *
import numpy as np

def calc_brightness_temp(radiance, wavelength_meters, wavelength_um):
    h = 6.626e-34      #Planck's  Constant
    k = 1.381e-23      #Boltzmann's Constant
    c = 2.988e8        #Speed of Light

    term1 = (2. * h * c**2)/(radiance * wavelength_meters**4 * wavelength_um)
    term2 = np.log(term1 + 1)
    term3 = (h*c)/(k*wavelength_meters)
    brightness_temp = term3/term2
    return brightness_temp

filename = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'

# Open the HDF4 file.
hdffile = SD(filename)

# Get the data for the reflective bands at 1 km resolution.
bands_8to19and26_obj = hdffile.select('EV_1KM_RefSB')
bands_8to19and26 = bands_8to19and26_obj.get()
band_names_8to19and26 = bands_8to19and26_obj.attributes()['band_names'].split(',')

# Get the data for the thermal emissive bands at 1 km resolution.
bands_20to36_obj = hdffile.select('EV_1KM_Emissive')
bands_20to36 = bands_20to36_obj.get()
band_names_20to36 = bands_20to36_obj.attributes()['band_names'].split(',')

# Get the data for the reflective bands aggregated from 500 m resolution.
bands_3to7_obj = hdffile.select('EV_500_Aggr1km_RefSB')
bands_3to7 = bands_3to7_obj.get()
band_names_3to7 = bands_3to7_obj.attributes()['band_names'].split(',')

# Get the data for the reflective bands aggregated from 250 m resolution.
bands_1to2_obj = hdffile.select('EV_250_Aggr1km_RefSB')
bands_1to2 = bands_1to2_obj.get()
band_names_1to2 = bands_1to2_obj.attributes()['band_names'].split(',')

# Find the index where the required bands are located.
band_2_index = band_names_1to2.index('2')
band_32_index = band_names_20to36.index('32')

# Get data for just the two bands needed.
band_2_counts = bands_1to2[band_2_index]
band_32_counts = bands_20to36[band_32_index]

# Get reflectance scale and offset for band 2.
band_2_reflectance_scale = bands_1to2_obj.attributes()['reflectance_scales'][band_2_index]
band_2_reflectance_offset = bands_1to2_obj.attributes()['reflectance_offsets'][band_2_index]

# Get reflectance scale and offset for band 2.
band_32_radiance_scale = bands_20to36_obj.attributes()['radiance_scales'][band_2_index]
band_32_radiance_offset = bands_20to36_obj.attributes()['radiance_offsets'][band_32_index]

# Get reflectance for band 2.
band_2 = band_2_reflectance_scale * (band_2_counts - band_2_reflectance_offset)

# Mask the bad values in the array.
band_2_valid_range = bands_1to2_obj.attributes()['valid_range']
band_2_masked = np.ma.masked_where(band_2_counts > band_2_valid_range[1], band_2)

# Calculate the mean for band 2.
# Value is right, but takes too long in Anaconda, will use np.mean for testing code
band_2_mean = mean_func(band_2_masked)
#band_2_mean = np.mean(band_2_masked)
print('Band  2 Mean: {:13.4f}'.format(band_2_mean))

# Calculate variance for band 2.
band_2_variance = variance_func(band_2_masked, band_2_mean)
#band_2_variance = np.var(band_2_masked)
print('Band  2 Variance: {:9.4f}'.format(band_2_variance))

# Get radiance for band 32.
band_32_radiance = band_32_radiance_scale * (band_32_counts - band_32_radiance_offset)
band_32_wavelength_meters = 12.02e-6
band_32_wavelength_um = 12.02
# Get brightness temperatures for band 32.
band_32 = calc_brightness_temp(band_32_radiance, band_32_wavelength_meters, band_32_wavelength_um)

# Mask the bad values in the array.
band_32_valid_range = bands_20to36_obj.attributes()['valid_range']
band_32_masked = np.ma.masked_where(band_32_counts > band_32_valid_range[1], band_32)

# Calculate the mean for band 32.
band_32_mean = mean_func(band_32_masked)
#band_32_mean = np.mean(band_32_masked)
print('Band 32 Mean: {:13.4f}'.format(band_32_mean))

# Calculate variance for band 32.
band_32_variance = variance_func(band_32_masked, band_32_mean)
#band_32_variance = np.var(band_32_masked)
print('Band 32 Variance: {:9.4f}'.format(band_32_variance))

hdffile.end()
