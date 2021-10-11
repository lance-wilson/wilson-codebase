#!/usr/bin/env python
#
# Name:
#   winds.py
#
# Purpose:
#   The purpose of this program is to take two data files containing true air
#       speed, heading, beta angle, and east and north ground velocity, and
#       calculating the relative errors that result from using a Taylor Series
#       approximation of Sine and Cosine versus the defined functions in the
#       math library. The program will then output the relative errors to two
#       output files, and then create two plots showing the relative errors up
#       to a 120 degree heading angle.
#
# Syntax:
#   python winds.py
#
#   Input: Data concerning winds from winds_1.dat and winds_2.dat.
#
#   Output: Two output files containing the heading angle, as well as the
#           relative errors of the East-West and North-South Wind components,
#           the magnitude of the wind, and the wind direction. Also, two plots
#           of these relative errors. 
#
# Execution Example:
#   Linux example: python winds.py
#
# Modification History:
#   2017/09/15 - Lance Wilson:  Created.
#   2017/09/19 - Lance Wilson:  Added case 1 using defined sine and cosine.
#   2017/09/20 - Lance Wilson:  Added case 2
#
# Verification of Data:   
#
# Copyright 2017 Lance Wilson

import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def taylorSin(x):
    # sin(x) ~= x - x^3/3! + x^5/5! - x^7/7!
    return (x - math.pow(x,3)/math.factorial(3) + math.pow(x,5)/math.factorial(5) - math.pow(x,7)/math.factorial(7))

def taylorCos(x):
    # cos(x) ~= 1 - x^2/2! + x^4/4! - x^6/6!
    return (1 - math.pow(x,2)/math.factorial(2) + math.pow(x,4)/math.factorial(4) - math.pow(x,6)/math.factorial(6))

infile1 = open('winds_1.dat', 'r')
infile2 = open('winds_2.dat', 'r')

# Take in the header from the file.
header1_names = infile1.readline().split()
header1_units = infile1.readline().split()
header2_names = infile2.readline().split()
header2_units = infile2.readline().split()

true_air_speed1 = []
heading1 = []
beta1 = []
ground_x1 = []
ground_y1 = []
true_air_speed2 = []
heading2 = []
beta2 = []
ground_x2 = []
ground_y2 = []

heading1_radians = []
heading2_radians = []
beta1_radians = []
beta2_radians = []

wind_dir_true1 = []
wind_dir_true2 = []
wind_mag_true1 = []
wind_mag_true2 = []

U_true1 = []
V_true1 = []
U_true2 = []
V_true2 = []

U_approx1 = []
V_approx1 = []
U_approx2 = []
V_approx2 = []

wind_dir_approx1 = []
wind_mag_approx1 = []
wind_dir_approx2 = []
wind_mag_approx2 = []

relative_u1_err = []
relative_u2_err = []
relative_v1_err = []
relative_v2_err = []
relative_wind_mag1_err = []
relative_wind_mag2_err = []
relative_wind_dir1_err = []
relative_wind_dir2_err = []

# Import the data from the two files.
for line in infile1:
    true_air_speed1.append(float(line.split()[0]))
    heading1.append(float(line.split()[1]))
    beta1.append(float(line.split()[2]))
    ground_x1.append(float(line.split()[3]))
    ground_y1.append(float(line.split()[4]))
infile1.close()

for line in infile2:
    true_air_speed2.append(float(line.split()[0]))
    heading2.append(float(line.split()[1]))
    beta2.append(float(line.split()[2]))
    ground_x2.append(float(line.split()[3]))
    ground_y2.append(float(line.split()[4]))
infile2.close()

# Convert the heading and beta angles to radians.
for x in range(0,len(heading1)):
    heading1_radians.append(math.radians(heading1[x]))
    beta1_radians.append(math.radians(beta1[x]))
    heading2_radians.append(math.radians(heading2[x]))
    beta2_radians.append(math.radians(beta2[x]))

# Equations: U = -1.0 * true_air_speed * sin(heading + beta) + ground_x
#            V = -1.0 * true_air_speed * cos(heading + beta) + ground_y
#            wind_dir = atan2(-U, -V) (radians)
#            wind_mag = sqrt(U^2 + V^2)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Case 1, with standard sine and cosine functions.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
for x in range(0,len(heading1)):
    U_true1.append(-1.0 * true_air_speed1[x] * math.sin(heading1_radians[x] + beta1_radians[x]) + ground_x1[x])
    V_true1.append(-1.0 * true_air_speed1[x] * math.cos(heading1_radians[x] + beta1_radians[x]) + ground_y1[x])
    wind_dir_true1.append(math.degrees(math.atan2(-1.0*U_true1[x],-1.0*V_true1[x])))
    wind_mag_true1.append(math.sqrt(math.pow(U_true1[x],2) + math.pow(V_true1[x],2)))

for x in range(0,len(heading2)):
    U_true2.append(-1.0 * true_air_speed2[x] * math.sin(heading2_radians[x] + beta2_radians[x]) + ground_x2[x])
    V_true2.append(-1.0 * true_air_speed2[x] * math.cos(heading2_radians[x] + beta2_radians[x]) + ground_y2[x])
    wind_dir_true2.append(math.degrees(math.atan2(-1.0*U_true2[x],-1.0*V_true2[x])))
    wind_mag_true2.append(math.sqrt(math.pow(U_true2[x],2) + math.pow(V_true2[x],2)))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Case 2, with taylor series approximations of sine and cosine functions.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
for x in range(0,len(heading1)):
    U_approx1.append(-1.0 * true_air_speed1[x] * taylorSin(heading1_radians[x] + beta1_radians[x]) + ground_x1[x])
    V_approx1.append(-1.0 * true_air_speed1[x] * taylorCos(heading1_radians[x] + beta1_radians[x]) + ground_y1[x])
    wind_dir_approx1.append(math.degrees(math.atan2(-1.0*U_approx1[x],-1.0*V_approx1[x])))
    wind_mag_approx1.append(math.sqrt(math.pow(U_approx1[x],2) + math.pow(V_approx1[x],2)))

for x in range(0,len(heading2)):
    U_approx2.append(-1.0 * true_air_speed2[x] * taylorSin(heading2_radians[x] + beta2_radians[x]) + ground_x2[x])
    V_approx2.append(-1.0 * true_air_speed2[x] * taylorCos(heading2_radians[x] + beta2_radians[x]) + ground_y2[x])
    wind_dir_approx2.append(math.degrees(math.atan2(-1.0*U_approx2[x],-1.0*V_approx2[x])))
    wind_mag_approx2.append(math.sqrt(math.pow(U_approx2[x],2) + math.pow(V_approx2[x],2)))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculation of the Relative Errors.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
for x in range(0,len(U_true1)):
    # Relative Error = abs(true - approx)/true.
    relative_u1_err.append(abs(U_true1[x] - U_approx1[x])/abs(U_true1[x]))
    relative_u2_err.append(abs(U_true2[x] - U_approx2[x])/abs(U_true2[x]))
    try:
        relative_v1_err.append(abs(V_true1[x] - V_approx1[x])/abs(V_true1[x]))
    except ZeroDivisionError:
        relative_v1_err.append(abs(V_true1[x] - V_approx1[x])/1.0)
    relative_v2_err.append(abs(V_true2[x] - V_approx2[x])/abs(V_true2[x]))
    relative_wind_mag1_err.append(abs(wind_mag_true1[x] - wind_mag_approx1[x])/abs(wind_mag_true1[x]))
    relative_wind_mag2_err.append(abs(wind_mag_true2[x] - wind_mag_approx2[x])/abs(wind_mag_true2[x]))
    relative_wind_dir1_err.append(abs(wind_dir_true1[x] - wind_dir_approx1[x])/abs(wind_dir_true1[x]))
    relative_wind_dir2_err.append(abs(wind_dir_true2[x] - wind_dir_approx2[x])/abs(wind_dir_true2[x]))

#^^^^^^^^^^^^^^^^^
# Output to files.
#^^^^^^^^^^^^^^^^^
outfile1 = open('winds_1.out', 'w')
outfile2 = open('winds_2.out', 'w')

# Format specifiers are added to help make the file look nice.
outfile1.write('%-15s %-17s %-25s %-20s %-15s\n' % ('Heading (deg)', 'Rel. X-comp err', 'Rel. Y-comp err', 'Rel. Magnitude Err', 'Rel. Dir. Error'))
outfile2.write('%-15s %-17s %-17s %-20s %-15s\n' % ('Heading (deg)', 'Rel. X-comp err', 'Rel. Y-comp err', 'Rel. Magnitude Err', 'Rel. Dir. Error'))

for x in range(0,len(heading1)):
    outfile1.write('%-15.8f %-17.8f %-25.8f %-20.8f %-15.8f\n' % (heading1[x], relative_u1_err[x], relative_v1_err[x], relative_wind_mag1_err[x], relative_wind_dir1_err[x]))

for x in range(0,len(heading2)):
    outfile2.write('%-15.8f %-17.8f %-17.8f %-20.8f %-15.8f\n' % (heading2[x], relative_u2_err[x], relative_v2_err[x], relative_wind_mag2_err[x], relative_wind_dir2_err[x]))

outfile1.close()
outfile2.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Ploting the relative errors, winds_1.dat.
# Only plot data from 0 to 120 degrees.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
plt.plot(heading1[:120], relative_u1_err[:120], label='East-West Component Relative Error')
plt.plot(heading1[:120], relative_v1_err[:120], label='North-South Component Relative Error')
plt.plot(heading1[:120], relative_wind_mag1_err[:120], label='Wind Magnitude Relative Error')
plt.plot(heading1[:120], relative_wind_dir1_err[:120], label='Wind Direction Relative Error')
plt.yscale('log')
plt.title('Relative Error of Wind Components, Magnitudes, and Directions Resulting\nfrom Using a Taylor Series Approximation of Sine and Cosine, File 1.')
plt.xlabel('Heading (degrees)')
plt.ylabel('Relative Error')
plt.legend(loc='best')
plt.savefig('winds_1.png', dpi=400)
plt.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Ploting the relative errors, winds_2.dat.
# Only plot data from 0 to 120 degrees.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
plt.plot(heading2[:120], relative_u2_err[:120], label='East-West Component Relative Error')
plt.plot(heading2[:120], relative_v2_err[:120], label='North-South Component Relative Error')
plt.plot(heading2[:120], relative_wind_mag2_err[:120], label='Wind Magnitude Relative Error')
plt.plot(heading2[:120], relative_wind_dir2_err[:120], label='Wind Direction Relative Error')
plt.yscale('log')
plt.title('Relative Error of Wind Components, Magnitudes, and Directions Resulting\nfrom Using a Taylor Series Approximation of Sine and Cosine, File2.')
plt.xlabel('Heading (degrees)')
plt.ylabel('Relative Error')
plt.legend(loc='best')
plt.savefig('winds_2.png', dpi=400)
