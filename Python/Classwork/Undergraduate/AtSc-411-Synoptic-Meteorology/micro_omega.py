#!/usr/bin/env python
#
# Name:
#   micro_omega.py
#
# Purpose:
#   The purpose of this program is to determine the vertical velocity in
#       microbars/second diagnosed from a Q vector field given by Q1 = Q1_sc +
#       exp{-[(x-x_c)^2 + (y-y_c)^2]/k_d}[0.5*Q_sdc(x-x_c)] and Q2 = Q2_sc +
#       exp{-[(x-x_c)^2 + (y-y_c)^2]/k_d}[0.5*Q_sdc(y-y_c)].
#
# Syntax:
#   python micro_omega.py
#
#   Input: None.
#
#   Output: Text file titled microQ.txt, which contains vertical velocity in
#       ubar/s and is formatted in rows of 7 columns; an image file graphically
#       illustrating the omega field using a filled contour plot; an image file
#       graphically illustrating the omega field using an unfilled contour plot.
#
# Execution Example:
#   Linux example: python micro_omega.py
#
# Modification History:
#   2017/11/07 - Lance Wilson:  Created.
#   2017/11/12 - Lance Wilson:  Output to file added, changed to microbars.
#   2017/11/18 - Lance Wilson:  Added unfilled contour plot and comments.
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print 'Syntax/Example: python micro_omega.py'

def deriv_Q1(x_index, y_index):
    x = (x_index * distance_step) - 500.0
    y = (y_index * distance_step) - 500.0
    # Derivative calculated from question 1.
    dQ1_dx = math.exp(-1.0*(math.pow((x-x_c),2)+math.pow((y-y_c),2))/k_d) * 0.5 * Q_sdc * (1.0-2.0*math.pow((x-x_c),2)/k_d)
    return dQ1_dx

def deriv_Q2(x_index, y_index):
    x = (x_index * distance_step) - 500.0
    y = (y_index * distance_step) - 500.0
    # Derivative calculated from question 1.
    dQ2_dy = math.exp(-1.0*(math.pow((x-x_c),2)+math.pow((y-y_c),2))/k_d) * 0.5 * Q_sdc * (1.0-2.0*math.pow((y-y_c),2)/k_d)
    return dQ2_dy

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

x_c = 0.0
y_c = 0.0
R = 287.0 # J kg^-1 K^-1
pressure = 850.0 # mb
stable_param = 0.02 # m^2 s^-2 mb^-2
scale_factor = R/(stable_param*pressure) * 1000.0 # ub/K
k_d = 36932.99 # km^2
Q_sdc = -5.0e-8 # K s^-1 km^-2
distance_step = 25.0 # km
d_step_squared = math.pow(distance_step,2)

omega = np.zeros([41,41])
omega_old = np.zeros([41,41])

residual = np.zeros([41,41])
residual[10,10] = 15.0

while (np.amax(abs(residual)) >= 0.01): # ubar/s
    for x in range(1,len(omega[0])-1):
        for y in range(1,len(omega[0])-1):
            # Equation 4 of the assignment, units: ub s^-1 Km^-2.
            Q_div = -2.0*scale_factor*(deriv_Q1(x,y) + deriv_Q2(x,y))
            # Equation 7 of the assignment.
            residual[x][y] = omega_old[x-1][y] + omega_old[x+1][y] + omega_old[x][y-1] + omega_old[x][y+1] - 4.0*omega_old[x][y] - d_step_squared*Q_div
            # Equation 8 of the assignment.
            omega[x][y] = omega_old[x][y] + 0.25*residual[x][y]

    omega_old = np.copy(omega)

outfile = open ('microQ.txt', 'w')

outfile.write('                       AtSc 411: Synoptic Meteorology\n')
outfile.write('           Q Vector Programming Homework--Python Output\n\n')
outfile.write('%10.3f %10.3f = xc and yc of analysis grid\n' % (x_c, y_c))
outfile.write('%10.3f %10.3f = deltax and deltay of analysis grid\n' % (distance_step*(len(omega[0])-1), distance_step*(len(omega[0])-1)))
outfile.write('%10.3f %10.3f = dx and dy of analysis grid\n' % (distance_step, distance_step))
outfile.write('%10d %10d = nx and ny of analysis grid\n' % (len(omega[0]), len(omega[0])))

columns = 7
for k in range(0, int(math.ceil(float(len(omega[0]))/float(columns)))):
    outfile.write('\n')
    max_column = k*columns + columns - 1

    if (max_column > (len(omega) - 1)):
        max_column = len(omega) - 1

    outfile.write('The values for columns %4d to %4d are:\n\n' % ((k*columns + 1), (max_column + 1)))

    for j in range(0, len(omega)):
        for i in range(k*columns, max_column + 1):
            outfile.write(' %10.4f' % omega[i][j])
        outfile.write('\n')
    outfile.write('\n')

outfile.close()

# Filled contour plot.
x_range = np.array(range(-500,501,25)).astype(float)
y_range = np.array(range(-500,501,25)).astype(float)
v = np.linspace(-15.0, 1.05, endpoint=True)
c1 = plt.contourf(x_range, y_range, omega, v)
plt.title(r'Contour of Vertical Velocity ($\mu$b/s)')
plt.xlabel('North-South Distance (km)')
plt.ylabel('East-West Distance (km)')

cbar = plt.colorbar(c1)
cbar.set_label(r'$\omega$ ($\mu$b/s)')

plt.savefig('Q_omega_filled.png', dpi=400)
plt.clf()

# Unfilled contour plot.
x_range = np.array(range(-500,501,25)).astype(float)
y_range = np.array(range(-500,501,25)).astype(float)
# First interval spacing is useful for the values near the center of the graph.
v1 = np.linspace(-15.0, 1.05, 10, endpoint=True)
# Second interval spacing is useful for resolving the edge contours.
v2 = np.logspace(-15.0, 1.05, endpoint=True)
c2 = plt.contour(x_range, y_range, omega, v1)
c3 = plt.contour(x_range, y_range, omega, v2)

plt.title(r'Contour of Vertical Velocity ($\mu$b/s)')
plt.xlabel('North-South Distance (km)')
plt.ylabel('East-West Distance (km)')
plt.clabel(c2, inline=1, fontsize=10)
plt.clabel(c3, inline=1, fontsize=10)

cbar = plt.colorbar(c2)
cbar.set_label(r'$\omega$ ($\mu$b/s)')

plt.savefig('Q_omega.png', dpi=400)
