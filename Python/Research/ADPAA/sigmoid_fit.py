#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/scripts_python/sigmoid_fit.py
#
# Name:
#   sigmoid_fit.py
#
# Purpose:
#   To calculate the sigmoidal fit of a set of CCN/CPC ratio data.
#
# Syntax:
#   python sigmoid_fit.py arg1 arg2
#
#   Input NASA/UND formatted Files:
#       arg1 - A UND/NASA ASCII file which contains data to be fitted to.
#           An example file name is "16_04_06_00_00_00.ccncpcmultsubratio.raw".
#       arg2 - The name of the key of the variable for which the sigmoidal
#              fit will be calculated.
#
# Execution Example:
#   Linux example: python sigmoid_fit.py 16_04_06_00_00_00.ccncpcratio.raw CCN_Ratio
#
# Modification History:
#   2016/07/05 - Lance Wilson:  Created.
#   2016/07/19 - Lance Wilson:  Added curve_fit function for fitting.
#   2016/07/26 - Lance Wilson:  Modified adjust_time variable to work with any
#                               size interval file.
#   2016/07/28 - Lance Wilson:  Added graph of 50% point of the sigmoid
#                               function.
#   2016/08/02 - Lance Wilson:  Added and updated comments. Added calculated
#                               divisor to adjust_time variable.
#   2016/08/08 - Lance Wilson:  Added calculated bounds to graph.
#   2016/09/14 - Lance Wilson:  Added legend to graph.
#   2016/09/30 - Lance Wilson:  Changed x-axis to terms of particle size.
#   2016/10/10 - Lance Wilson:  Added new particle size range to produce a
#                               smoother graph.
#   2016/10/17 - Lance Wilson:  Added the error function calculation.
#   2016/10/19 - Lance Wilson:  Corrected the error function.
#   2016/10/21 - Lance Wilson:  Added error catching for bad keys in the
#                               original file or searched for argument.
#   2016/10/26 - Lance Wilson:  Added error function to graph.
#   2016/11/30 - Lance Wilson:  Improved graph center axis "zero point" with
#                               ratio data as reference.
#   2016/12/02 - Lance Wilson:  Shifted graph so it corresponds with the
#                               actual particle sizes.
#   2016/12/05 - Lance Wilson:  Adjust half point lines on graph.
#   2016/12/07 - Lance Wilson:  Updated comments.
#   2018/11/19 - Lance Wilson:  Converted lists to arrays for file output,
#                               updated help message and comments.
#
# Verification of Data:
#   (Pending)
#
# Copyright 2016 Lance Wilson, David Delene
# This program is distributed under the terms of the GNU General Public License
#
# This file is part of Airborne Data Processing and Analysis (ADPAA).
#
# ADPAA is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ADPAA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ADPAA.  If not, see <http://www.gnu.org/licenses/>.

from nasafile import NasaFile
from nasafileout import NasaFileOut
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.special import erf
import traceback
import re
from adpaa import ADPAA

def help_message():
    print 'Syntax: python sigmoid_fit.py filename var_name\n'
    print 'Purpose: To calculate the sigmoidal fit of a set of data.\n'
    print ('arg1 - The name of the UND/NASA formatted file. Requires a key '
           'named StartTime\n')
    print ('arg2 - The key for the variable that the sigmoidal fit is '
               'calculated for.\n')
    print ('arg3 - The name to be used for the output file NASA/UND file.\n')

# Sigmoid function used by scipy.optimize.curve_fit.
def sigmoid(x, a, k, c):
    y = a / (1.0 + np.exp(-1.0*k*(x))) + c
    return y

for param in sys.argv:
	if param.startswith('-h'):
		help_message()
		exit()

if (len(sys.argv) < 3):
    help_message()
    exit()

# File name.
ratio_in_file = sys.argv[1]
# Significant variable.
sig_var = sys.argv[2]

ratio_file = ADPAA()
ratio_file.ReadFile(ratio_in_file)

try:
    time_data = np.array(ratio_file.data['StartTime'])
    ratio_data = np.array(ratio_file.data[sig_var])
    particle_size = np.array(ratio_file.data['GenPar_Size'])
    stand_dev = np.array(ratio_file.data['StandDev'])
    delta_t = np.array(ratio_file.data['Delta_T'])
    pres = np.array(ratio_file.data['Pressure'])
except KeyError:
    # Store the traceback error message in a string variable.
    error_string = traceback.format_exc()
    # Use regular expressions to search for the key in the line wih an error.
    error_key = re.search('\[\'?(\w*)\'?\]', error_string)
    print 'The key ' + error_key.group(0) + ' was not found in the data file.'
    exit()

# Target is the mean of the ccn/cpc ratio data.
target = (max(ratio_data)+min(ratio_data))/2.0
# Index of the ratio_data that is closest to the target.
midpar_index = np.argmin(np.abs(ratio_data - target))
# Middle particle, the particle size at the index of the target.
midpar = particle_size[midpar_index]
divisor = (max(particle_size)- min(particle_size))/10.0
# adjust_size is an equivalent array of particle sizes that are centered
#   around zero (which is necessary for curve_fit to find the correct
#   sigmoid fit).
#   adjust_size is equivalent to 10 times the differences from the mean of
#   each particle size, divided by the range of particle sizes.
adjust_size = (particle_size - midpar)/divisor

# Calculates coefficients and covariance matrix of a curve based on the
#   programmer-defined sigmoid function, the adjusted time interval, and the
#   ratio data.
points= np.array([.99])
points_b= np.repeat(points, (len(ratio_data)-1))
sigma_init= np.array([0.01])
full_sigma= np.append(sigma_init, points_b)
#full_sigma2= np.append(full_sigma, sigma_init)
coeffs, pcov = curve_fit(sigmoid, adjust_size, ratio_data, sigma= full_sigma)
#coeffs, pcov = curve_fit(sigmoid, adjust_size, ratio_data)

# Find 50% points.
# Ratio data 50% point.
half_value = (max(ratio_data) + min(ratio_data))/2.0
# Adjust_size 50% point.
half_point = math.log((coeffs[0]/(half_value-coeffs[2])) - 1.0)/(-1.0*coeffs[1])
# Actual particle size 50% point (formula for adjust_size solved
#   for particle_size).
half_size = (half_point * divisor) + midpar

print half_value
print half_size

# Defining array for activation size output
half_size_arr = np.array([half_size]*len(time_data))
# Calculate the error function of the data.
err_fit = (max(ratio_data)/2.0) * (1.+erf((particle_size-midpar)/(stand_dev * math.sqrt(2))))

# Create an array of more closely spaced sizes for a smoother graph.
adjust_size2 = np.arange(((min(particle_size)-midpar)/divisor),((max(particle_size)-midpar)/divisor),0.25)
# Range step for particle_size2, to give the two arrays equal lengths
#   (required by matplotlib).
size_continuity = (max(particle_size)-min(particle_size))/len(adjust_size2)
# More closely spaced particle size.
particle_size2 = np.arange(min(particle_size), max(particle_size), size_continuity)

# Graph the particle_size high-resolution array on the x-axis, and the
#   sigmoid_fit of the adjust_size data on the y-axis (equivalent of
#   shifting the data to the correct x-values).
plt.plot(particle_size2,(coeffs[0] / (1.0 + np.exp(-1.0*coeffs[1]*(adjust_size2))))+coeffs[2], label='Best-Fit Curve')
# Add a scatter plot of the original data for comparison.
plt.scatter(particle_size, ratio_data, label='Measurements')
plt.plot([-10.0, 0.0, 200.0], [half_value, half_value, half_value], label='Activation Ratio')
#plt.scatter(particle_size, err_fit, label='Error fit function', color='orange')
plt.plot([half_size, half_size, half_size], [-1.0, 0, 1.5], label='Activation Size')
plt.title('Temperature Gradient of '+str(delta_t[1])+' degrees C at '+'{:5.5}'.format(str(pres[1]))+' mb', **titlefont)
plt.xlabel('Particle Size (nm)', **font)
plt.ylabel('CCN/CPC Ratio', **font)
plt.xlim(min(particle_size)-5, max(particle_size)+5)
#plt.ylim(min(min(err_fit), min(ratio_data))-0.05, max(max(err_fit), max(ratio_data))+0.05)
plt.ylim((min(ratio_data)-0.05), 1.05)
plt.yticks(np.arange(0.0, 1.1, 0.1))
plt.legend(loc='best')
plt.text(half_size+2, 0, '%.2f'%(half_size)+' nm', color='red', fontsize=14, style='italic', fontweight= 'bold')
plt.show()
