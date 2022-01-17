#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/python_lib/line_calc.py
#
# Name:
#   line_calc
#
# Purpose:
#   Calculates the slope and intercept of a best fit line of
#   supersaturation percentage vs. temperature difference from the
#   provided temperature
#
# Syntax:
#   (slope,intercept) = line_calc(temp)
#     Input:
#        temp - Top Plate temperature (K)
#
#     Output:
#        slope - The slope of the best-fit line.
#        intercept - The intercept of the best-fit line.
#
# Execution Example:
#   (slope,intercept) = line_calc(283.15)
#   Gives (slope, intercept) = (1.4211972852326162, 2.3323638161940381)
#
# Modification History:
#   2015/10/27 - Lance Wilson:  Written.
#   2016/01/13 - Lance Wilson:  Cut out graphing and other unnecessary code
#   2016/02/01 - Lance Wilson:  Added comments.
#   2016/02/19 - Lance Wilson:  Clarified variable names, converted for loops
#                               to while loops, changed return type to tuple.
#   2016/02/29 - Lance Wilson:  Added comments, clarified use of variables.
#   2016/03/02 - Lance Wilson:  Unnecessary global variables converted to local
#   2016/03/04 - Lance Wilson:  Added explanation of np.poly1d and np.polyfit
#   2016/04/15 - David Delene:  Added comments.
#   2016/04/18 - Lance Wilson:  Modified to only take one top plate temp at a time
#   2016/04/27 - Lance Wilson:  Added error handling for input temperature.
#   2016/04/29 - Lance Wilson:  Modified array indexing.
#   2016/05/04 - Lance Wilson:  Streamlined storage of slope and intercept
#
# Copyright 2016 David Delene
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

import math
import numpy as np
from vapor_func import vapor_func

def line_calc(temp):

    # Check if temperature is large enough to work with function.
    if (temp < 72.5):
        print ('Reminder: input temperatures must be in Kelvin\nReturning '
               'zeroes for %.2f Celsius\n' % (temp - 273.15))
        return (0,0)
 
    # deltaT_data stores temperature difference data points
    deltaT_data = np.zeros((120)) # Array of size 120

    # ccnss_data stores supersaturation percentage data points
    ccnss_data = np.zeros((120)) # Array of size 120

    # Index for arrays.
    x = 0

    # Temperature change from input temperature
    # Starts at 0.1 because ln(0) is not defined.
    deltaT = 0.1

    # Creates data for temperature differences and CCN supersaturation percentages
    while (deltaT < 12.0):
        # Saturation vapor pressure for top plate
        eT = vapor_func(temp)

        # Saturation vapor pressure for bottom plate
        eB = vapor_func(temp-deltaT)

        # Saturation vapor pressure for average of top & bottom plate temperatures.
        eM = vapor_func((temp+(temp-deltaT))/2.0)

        # Calculate the supersaturation percentage for the above vapor pressures.
        # Equation from ?
        ccnss = ((((eT + eB)/2.0)/eM)-1.0)*100.0

        # Store the natural log of temperature difference in an array.
        deltaT_data[x] = math.log(deltaT)

        # Store the natural log of supersaturation percentage in an array.
        ccnss_data[x] = math.log(ccnss)

        x += 1
        deltaT += 0.1
    # Find the slope and intercept of the line.
    # np.polyfit creates a least-squares fit of deltaT_data and 
    #   ccnss_data of order 1, and returns the coefficients.
    slope,intercept = np.polyfit(ccnss_data, deltaT_data, 1)

    return (slope, intercept)
