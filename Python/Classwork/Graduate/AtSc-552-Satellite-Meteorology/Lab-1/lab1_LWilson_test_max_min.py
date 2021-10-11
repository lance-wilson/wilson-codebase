#!/usr/bin/env python3
#
# Name:
#   lab1_LWilson_test_max_min.py
#
# Purpose:
#   Calculate the maximum and minimum values of AVHRR data fields using the
#   max_min_func function.
#
# Syntax:
#   python lab1_LWilson_test_max_min.py
#
# Modification History:
#   2020/01/30 - Lance Wilson:  Created.

from lab1_LWilson_max_min_func import max_min_func
import numpy as np

num_pixels = 500
num_lines = 500

latitude = np.fromfile('lac_95236.S1707.CAL_TK.lat', dtype=np.short).reshape(num_pixels, num_lines)/100.

longitude = np.fromfile('lac_95236.S1707.CAL_TK.lon', dtype=np.short).reshape(num_pixels, num_lines)/100.

solar_zenith_angle = np.fromfile('lac_95236.S1707.CAL_TK.sza', dtype=np.ubyte).reshape(num_pixels, num_lines)

viewing_zenith_angle = np.fromfile('lac_95236.S1707.CAL_TK.vza', dtype=np.ubyte).reshape(num_pixels, num_lines)

relative_azimuth = np.fromfile('lac_95236.S1707.CAL_TK.azm', dtype=np.ubyte).reshape(num_pixels, num_lines)

print('Variable{:>22s}{:>12s}'.format('Maximum', 'Minimum'))
print('Latitude:{:21.2f} {:11.2f}'.format(*max_min_func(latitude)))
print('Longitude:{:20.2f} {:11.2f}'.format(*max_min_func(longitude)))
print('Solar Zenith Angle:{:11.2f} {:11.2f}'.format(*max_min_func(solar_zenith_angle)))
print('Viewing Zenith Angle:{:9.2f} {:11.2f}'.format(*max_min_func(viewing_zenith_angle)))
print('Relative Azimuth:{:13.2f} {:11.2f}'.format(*max_min_func(relative_azimuth)))















