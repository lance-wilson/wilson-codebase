#!/usr/bin/env python
#
# Name:
#   oneway-stable.py
#
# Purpose:
#   The purpose of this program is to solve the equation phi(x,t) = sin(x-ct)
#       using the one way wave equation (dphi/dt + c*dphi/dx = 0)
#       approximation. This version plots an stable solution, which means that
#       the errors in the calculation of the approximate solution remain
#       bounded and do not grow over time.
#
# Syntax:
#   python oneway-stable.py
#
#   Input: None.
#
#   Output: Interactive image file of the stable solution.
#
# Execution Example:
#   Linux example: python oneway-stable.py
#
# Modification History:
#   2017/10/23 - Lance Wilson:  Created.
#   2017/11/03 - Lance Wilson:  Began adding approximate solution.
#   2017/11/04 - Lance Wilson:  Added graphing of the approximate solution
#                               and made the graph smoother.
#   2017/11/05 - Lance Wilson:  Improved the approximate solution, cleaned up
#                               the structure and added comments.
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print 'Syntax/Example: python oneway-stable.py'

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

# Define the time steps and constants.
delta_x = 0.1
delta_t = 1.0
c = 0.05
# From the class notes, mu is defined as c*time_step/x_step.
mu = c * delta_t/delta_x
x_range = int(2.0*math.pi/delta_x)
time_max = 100.0

# Initialize the plot with interactivity.
fig = plt.figure()
plt.ion()

# Create array of the true solution with respect to x.
x_values = np.empty(x_range+1)
for x in range(x_range + 1):
    x_values[x] = x * delta_x
true_phi_values = np.sin(x_values)

approx_phi_values = np.empty(x_range+1)
# The first solution of the previous step is set to the true value.
prev_approx_phi_values = np.copy(true_phi_values)

time = 0.0
while (time < time_max):
    # Values for the exact solution.
    new_x_values = x_values - c*time
    true_phi_values = np.sin(new_x_values)

    if (time == 0.0):
        approx_phi_values = np.copy(true_phi_values)
    # From the class notes: the approximate solution is based on the one-way
    #   wave equation. This solution, using finite differences, is phi_j,n+1 =
    #   phi_j,n - mu*(phi_j,n - phi_j-1,n), where n indicates the value at the
    #   previous iteration, n+1 is at the time of the current iteration, j is
    #   at the current x point, and j-1 is the previous x point.
    else:
        for j in range(x_range+1):
            approx_phi_values[j] = prev_approx_phi_values[j] - mu*\
                (prev_approx_phi_values[j] - prev_approx_phi_values[j-1])

    prev_approx_phi_values = np.copy(approx_phi_values)

    # Time is incremented here so that the graph labels start from 1.
    time = time + delta_t

    plt.cla()
    plt.plot(x_values, true_phi_values, color='b', label=(\
             'True, Time '+str(time)))
    plt.plot(x_values, approx_phi_values, color = 'firebrick', label=(\
             'Approx, Time ' + str(time)))
    plt.xlabel('X Values')
    plt.xlim(0,2.0*math.pi)
    plt.xticks([0, math.pi/2.0, math.pi, 1.5*math.pi, 2.0*math.pi],\
        ['$0$', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'])
    plt.ylabel('Phi Values')
    plt.title(r'Stable Approximation of $\Phi$ = sin(x-ct)')
    plt.legend(loc='upper right')
    plt.pause(0.05)

    if (time == 100.0):
        plt.savefig('oneway-stable.png', dpi=400)

while True:
    plt.pause(0.05)
