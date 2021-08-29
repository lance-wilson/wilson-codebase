#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   get_hdf4_data.py
#
# Purpose:
#   Read data from an HDF4 file containing MODIS data and return a combined
#   array containing all the bands.
#
# Syntax:
#   from get_hdf4_data import read_hdf_file
#   from get_hdf4_data import calc_brightness_temp
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/04/04 - Lance Wilson:  Created.

from pyhdf.SD import *
import numpy as np

# Read data from an HDF4 file containing Terra MODIS data.
def read_hdf_file(filename):
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
    
    return (all_bands, all_band_names, all_scales, all_offsets, valid_range)

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