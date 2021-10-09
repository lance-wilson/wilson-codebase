#!/usr/bin/env python
#
# Name:
#   dynamic_pressure.py
#
# Purpose:
#   The purpose of this program is to determine the dynamic perturbation
#   pressure field in Pascals of a rotating mesocyclone using the equation
#   [Horizontal Laplacian]p'_d = -rho_bar_v*[(du/dx)^2 + (dv/dy)^2] -
#   2*rho_bar_dv*(du/dy * dv/dx)
#
# Syntax:
#   python dynamic_pressure.py
#
#   Input: None.
#
#   Output: Text file titled rotate.txt, which contains dynamical perturbation
#       pressure in Pa/km^2 and is formatted in rows of 7 columns; an image
#       file graphically illustrating the dynamic pressure perturbation field
#       using a filled contour plot; an image file graphically illustrating the
#       dynamic pressure perturbation field using an unfilled contour plot.
#
# Execution Example:
#   Linux example: python dynamic_pressure.py
#
# Modification History:
#   2018/03/22 - Lance Wilson:  Created from micro_omega.py.
#   2018/04/05 - Lance Wilson:  Adjusted a few negative signs and the residual.
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print 'Syntax/Example: python dynamic_pressure.py'

def deriv_u_x(x_index, y_index):
    x = (x_index * distance_step) - 15.0
    y = (y_index * distance_step) - 15.0
    # Derivative calculated from question 1.
    du_dx = math.exp(-1.0*(math.pow((x-x_c),2)+math.pow((y-y_c),2))/k_d) *  zeta_c * (x-x_c)*(y-y_c)/k_d
    return du_dx

def deriv_u_y(x_index, y_index):
    x = (x_index * distance_step) - 15.0
    y = (y_index * distance_step) - 15.0
    # Derivative calculated from question 1.
    du_dy = math.exp(-1.0*(math.pow((x-x_c),2)+math.pow((y-y_c),2))/k_d) *  zeta_c * (-0.5 + math.pow((y-y_c),2)/k_d)
    return du_dy

def deriv_v_y(x_index, y_index):
    x = (x_index * distance_step) - 15.0
    y = (y_index * distance_step) - 15.0
    # Derivative calculated from question 1.
    dv_dy = math.exp(-1.0*(math.pow((x-x_c),2)+math.pow((y-y_c),2))/k_d) * -1. * zeta_c * (x-x_c)*(y-y_c)/k_d
    return dv_dy

def deriv_v_x(x_index, y_index):
    x = (x_index * distance_step) - 15.0
    y = (y_index * distance_step) - 15.0
    # Derivative calculated from question 1.
    dv_dx = math.exp(-1.0*(math.pow((x-x_c),2)+math.pow((y-y_c),2))/k_d) * zeta_c * (0.5 - math.pow((x-x_c),2)/k_d)
    return dv_dx

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

u_translate = 10.0 # m s^-1
x_c = 0.0
y_c = 0.0
pressure = 500.0 # mb
rho_bar_dv = 0.691462 # kg m^-3
k_d = 36.0674 # km^2
zeta_c = 1.0e-2 # s^-1
distance_step = 1.0 # km
d_step_squared = math.pow(distance_step,2)

p_d = np.zeros([31,31])
p_d_old = np.zeros([31,31])

residual = np.zeros([31,31])
residual[10,10] = 15.0

p_prime = np.zeros([31,31])
for x in range(1,len(p_d[0])-1):
    for y in range(1,len(p_d[0])-1):
        # Equation 2 of the assignment, units: hPa Km^-2. (Multiply by 1000000 to convert to Km^2, divide by 100 to convert to hPa)
        p_prime[x][y] = (-1.0*rho_bar_dv*(deriv_u_x(x,y)**2 + deriv_v_y(x,y)**2) - 2.0*rho_bar_dv*(deriv_u_y(x,y)*deriv_v_x(x,y)))*10000.

while (np.amax(abs(residual)) >= 0.0001): # hPa
    for x in range(1,len(p_d[0])-1):
        for y in range(1,len(p_d[0])-1):
            # Equation 5 of the assignment.
            residual[x][y] = p_d_old[x-1][y] + p_d_old[x+1][y] + p_d_old[x][y-1] + p_d_old[x][y+1] - 4.0*p_d_old[x][y] - d_step_squared*p_prime[x][y]
            # Equation 6 of the assignment.
            p_d[x][y] = p_d_old[x][y] + 0.25*residual[x][y]

    p_d_old = np.copy(p_d)

outfile = open ('rotate.txt', 'w')

outfile.write('                       AtSc 460: Mesoscale Meteorology\n')
outfile.write('                   Dynamic Perturbation Pressure Homework\n\n')
outfile.write('%10.3f %10.3f = xc and yc of analysis grid\n' % (x_c, y_c))
outfile.write('%10.3f %10.3f = deltax and deltay of analysis grid\n' % (distance_step*(len(p_d[0])-1), distance_step*(len(p_d[0])-1)))
outfile.write('%10.3f %10.3f = dx and dy of analysis grid\n' % (distance_step, distance_step))
outfile.write('%10d %10d = nx and ny of analysis grid\n' % (len(p_d[0]), len(p_d[0])))

columns = 7
for k in range(0, int(math.ceil(float(len(p_d[0]))/float(columns)))):
    outfile.write('\n')
    max_column = k*columns + columns - 1

    if (max_column > (len(p_d) - 1)):
        max_column = len(p_d) - 1

    outfile.write('The values for columns %4d to %4d are:\n\n' % ((k*columns + 1), (max_column + 1)))

    for j in range(0, len(p_d)):
        for i in range(k*columns, max_column + 1):
            outfile.write(' %10.4f' % p_d[i][j])
        outfile.write('\n')
    outfile.write('\n')

outfile.close()

# Filled contour plot.
x_range = np.array(range(-15,16,1)).astype(float)
y_range = np.array(range(-15,16,1)).astype(float)
####v = np.linspace(-15.0, 1.05, endpoint=True)
####c1 = plt.contourf(x_range, y_range, p_d, v)
c1 = plt.contourf(x_range, y_range, p_d)
plt.title('Contour of Dynamic Perturbation Pressure (mb)')
plt.xlabel('East-West Distance (km)')
plt.ylabel('North-South Distance (km)')


cbar = plt.colorbar(c1)
cbar.set_label('Dynamic p\' (mb)')

plt.savefig('Dynamic_P_filled.png', dpi=400)
plt.clf()

# Unfilled contour plot.
x_range = np.array(range(-15,16,1)).astype(float)
y_range = np.array(range(-15,16,1)).astype(float)
# First interval spacing is useful for the values near the center of the graph.
v1 = np.linspace(-1.6, 0, 9, endpoint=True)
# Range is in powers of 10 (the default base -> range(base^start,base^end)).
v2 = np.logspace(-4.1, -1, num=10, endpoint=True)
c2 = plt.contour(x_range, y_range, p_d, v1)
c3 = plt.contour(x_range, y_range, p_d, v2)
####c2 = plt.contour(x_range, y_range, p_d)

plt.title('Contour of Dynamic Perturbation Pressure (mb)')
plt.xlabel('East-West Distance (km)')
plt.ylabel('North-South Distance (km)')
plt.clabel(c2, inline=1, fontsize=10)
plt.clabel(c3, inline=1, fontsize=10)

cbar = plt.colorbar(c2)
cbar.set_label('Dynamic P\' (mb)')

plt.savefig('Dynamic_P.png', dpi=400)
