#!/usr/bin/env python
#
# An up-to-date version of this code can be found at:
#   https://sourceforge.net/p/adpaa/code/HEAD/tree/trunk/src/python_lib/vapor_func.py
#
# Name:
#   vapor_func
#
# Purpose:
#   Calculates the vapor pressure at a given temperature.  
#
# Syntax:
#   e = vapor_func(temp)
#     Input:  temp - temperature (K)
#     Output:  e - vapor pressure (mb)
#
# Execution Example:
#   e = vapor_func(293.15)
#   Gives e = 23.35846831
#
# Modification History:
#   2015/10/27 - Lance Wilson:  Written.
#   2016/01/15 - Lance Wilson:  Added comments.
#   2016/04/15 - David Delene:  Added comments.
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

def vapor_func(temp):
   # Use equation for saturation vapor pressure (e).
   #   e has units of mb.
   #   Temperature (temp) has units of K.
   # Reference:  Page 350, Smithsonian Meteorological Tables, 6th Revised Edition. 
   e = -7.90298*(373.16/temp-1.0)+5.02808*math.log10(373.16/temp)-1.3816e-7*(10.0**(11.344*(1.0-temp/373.16))-1.0)+8.1328e-3*(10.0**(3.49149*(1.0- 373.16/temp))-1.0)+math.log10(1013.246)

   return 10.0**e
