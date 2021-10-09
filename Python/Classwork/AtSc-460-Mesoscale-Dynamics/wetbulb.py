#!/usr/bin/env python
#
# Name:
#   wetbulb.py
#
# Purpose:
#   The purpose of this program is to calculate the wet bulb temperature along pseudoadiabats at the 1050, 850, 500, and 100 hPa levels for the pseudoequivalent potential temperatures 253.15, 283.15, and 313.15 K.
#   Utilizes equations from Davies-Jones (2008) and Bolton (1980).
#
# Syntax:
#   python wetbulb.py
#
#   Input: None.
#
#   Output: 
#
# Execution Example:
#   Linux example: python wetbulb.py
#
# Modification History:
#   2017/01/27 - Lance Wilson:  Created.
#   2017/02/02 - Lance Wilson:  Adjusted equations to match units.
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

# Constants
p_0 = 1000.         # hPa
lambda_ = 3.504     # c_pd / R_d
base_temp = 273.15  # Kelvin, constant C in Davies-Jones
A = 2675            # Kelvin

def help_message():
    print 'Syntax/Example: python wetbulb.py'

def pi(pressure):
    return math.pow((pressure/p_0),1./lambda_)

# Equation 4.3 in Davies-Jones (2008).
def k1(pressure):
    return -38.5*(pi(pressure)**2) + 137.81*pi(pressure) - 53.737

# Equation 4.4 in Davies-Jones (2008).
def k2(pressure):
    return -4.392*(pi(pressure)**2) + 56.831*pi(pressure) - 0.384

def D(pressure):
    return math.pow((0.1859*pressure/p_0 + 0.6512), -1)

# Poisson's equation of potential temperature.
def temp_equiv(theta, pressure):
    return theta*pi(pressure)

def sat_mix_ratio(pressure, temp):
    return 0.622 * e_s(temp)/(pressure - e_s(temp))

# Equation 10 of Bolton (1980).
def e_s(temp):
    return 6.112*math.exp((17.67*(temp-273.15))/((temp-273.15) + 243.5))

# Equation 43 of Bolton (1980).
def bolton_theta(temp, pressure, mix_ratio):
    # Assumes the saturated mixing ratio is the same as the mixing ratio
    #   and that the temperature is the wet-bulb temperature is the LCL
    #   temperature because the air is saturated on a pseudoadiabat.
    return (temp*math.pow((1000./pressure), 0.2854*(1-0.28e-3*mix_ratio)) *\
            math.exp(((3.376/temp) - 0.00254) * mix_ratio*\
            (1. + 0.81e-3*mix_ratio)))

# Paragraph after 3.7.
# d lne_s(T_k)/dT_k = ab/(T_k - C + b)^2, a = 17.67, b = 243.5 K, C = 273.15 K
def dlne_sdT_E(temp):
    a = 17.67
    b = 243.5  # K
    return (a*b)/(temp - base_temp + b)**2

# Direct derivative of (1/e_s)*d/dT(e_s)
def deriv_ln_es(temp):
    return 17.67*(1-(temp-273.15))/((temp-273.15)+243.5)**2

thetas = np.array([253.15, 283.15, 313.15])
pressures = np.array([1050., 850., 500., 100.])
wet_bulbs = np.empty([3,4])
theta_eps = np.empty([3,4])

for x in range(len(thetas)):
    for y in range(len(pressures)):
        equiv_temp = temp_equiv(thetas[x], pressures[y])
        D_value = D(pressures[y])
        compare_value = math.pow((base_temp/equiv_temp), lambda_)
        k1_value = k1(pressures[y])
        k2_value = k2(pressures[y])
        sat_mix_value = sat_mix_ratio(pressures[y], equiv_temp)

        z = 0

        if (compare_value > D_value and compare_value >= 1.):
            wet_bulb_temp = equiv_temp - base_temp - (A*sat_mix_value/\
            ##                (1+A*sat_mix_value*dlne_sdT_E(equiv_temp)))
                              (1+A*sat_mix_value*deriv_ln_es(equiv_temp)))
            z=1

        elif (compare_value >= 1. and compare_value <= D_value):
            wet_bulb_temp = k1_value - k2_value*compare_value

            z=2

        elif (compare_value >= 0.4 and compare_value < 1.):
            wet_bulb_temp = (k1_value - 1.21) - (k2_value - 1.21)*compare_value

            z=3

        elif (compare_value < 0.4):
            wet_bulb_temp = (k1_value - 2.66) - (k2_value - 1.21)\
                            *compare_value + 0.58/compare_value

            z=4

        #print z, k1_value, k2_value, equiv_temp, wet_bulb_temp
        #print sat_mix_value

        wet_bulbs[x][y] = wet_bulb_temp + 273.15

        theta_ep = bolton_theta(wet_bulbs[x][y], pressures[y], sat_mix_value)

        theta_eps[x][y] = theta_ep

print 'Wet-bulb Temperatures (K)'
print 'Pressure (hPa)      1050    850     500     100'
for x in range(len(thetas)):
    print 'Theta = {:.2f} K   '.format(thetas[x]),
    for y in range(len(pressures)):
        print '%.2f ' % wet_bulbs[x][y],
    print

print
print 'Equivalent Potential Temperatures (K)'
print 'Pressure (hPa)               1050    850     500     100'
for x in range(len(thetas)):
    print 'Expected Theta = {:.2f} K   '.format(thetas[x]),
    for y in range(len(pressures)):
        print '%.2f ' % theta_eps[x][y],
    print
