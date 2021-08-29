#!/usr/bin/env python3
#
# Name:
#   FDDiffusion.py
#
# Purpose:
#   To plot the centered and upstream difference approximations for the scalar
#   advection equation, where the exact solution is u(x,t) = sin^6(x-ct), for
#   time >= 30 seconds at two different grid resolutions.
#
# Syntax:
#   Single file: python FDDiffusion.py
#
#   Input: None.
#
#   Output: Two plots containing the comparisons between the exact solution and
#           the approximations at the two grid intervals.
#           Two plots showing how the plot looks when made unstable.
#
# Modification History:
#   2019/02/11 - Lance Wilson:  Created.

import math
import matplotlib.pyplot as plt
import numpy as np

grid_intervals_a = 20
grid_intervals_b = 40

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Part 1: Finite Difference
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def finite_graph(grid_intervals, stable=True):
    x_range = np.linspace(0, 4.*math.pi, num=grid_intervals+1)
    x_step = 4.*math.pi/grid_intervals   # Meters
    c = 0.1   # m/s
    time_step = 0.5*x_step/c   # Seconds
    # For unstable case, multiply the stable time step for courant number 0.5
    #   by a number greater than 2.0.
    if not stable:
        # The constant can be anything greater than 2, using 62.1 to
        #   exaggerate the effect on the graph.
        time_step = 62.1*time_step   
    mu = c*time_step/x_step

    # Centered difference arrays.
    u_cent = np.zeros([grid_intervals+1])
    # Initial condition (just need x since initial time = 0).
    u_cent_old = np.power(np.sin(x_range), 6)
    u_cent_old_old = np.zeros([grid_intervals+1])

    # Upstream difference arrays.
    u_up = np.zeros([grid_intervals+1])
    # Initial condition (just need x since initial time = 0).
    u_up_old = np.power(np.sin(x_range), 6)

    current_time = 0.

    while (current_time < 30.):
        # Exact solution for comparison.
        u_exact = np.power(np.sin(x_range - c*current_time), 6)
        for j in range(1,grid_intervals):
            # Centered Difference.
            if (current_time == 0.):
                u_cent[j] = u_cent_old[j] - mu * (u_cent_old[j+1] - u_cent_old[j-1])
            else:
                u_cent[j] = u_cent_old_old[j] - mu * (u_cent_old[j+1] - u_cent_old[j-1])

            # Upstream Difference.
            u_up[j] = u_up_old[j] - mu * (u_up_old[j] - u_up_old[j-1])

        current_time += time_step
        # Copy values into old areas for next time step.
        u_cent_old_old = np.copy(u_cent_old)
        u_cent_old = np.copy(u_cent)
        u_up_old = np.copy(u_up)

    # Plotting
    plt.plot(x_range, u_exact, label=r'Exact u=sin$\mathregular{^6}$(x-ct)', color='Blue')
    plt.plot(x_range, u_cent, label='Leapfrog', color='Red')
    plt.plot(x_range, u_up, label='Upstream', color='Green')
    plt.xlim(0, 4.*math.pi)
    # Set x tick marks to be in terms of pi.
    plt.xticks([0, math.pi, 2.0*math.pi, 3.0*math.pi, 4.0*math.pi],\
        ['$0$', r'$\mathregular{\pi}$', r'$2\mathregular{\pi}$', r'$3\mathregular{\pi}$', r'$4\mathregular{\pi}$'])
    plt.legend(loc='upper left')

    plt.xlabel('x (m)')
    plt.ylabel(r'u(x,t) (m $\mathregular{s^{-1}}$)')

    if stable:
        plt.title('{:2d} Grid Intervals, Courant Number = {:.1f}'.format(grid_intervals, mu))
        plt.savefig('Q1_Grid_{:2d}.png'.format(grid_intervals), dpi=400)
    else:
        plt.title('Unstable, {:2d} Grid Intervals, Courant Number = {:.2f}'.format(grid_intervals, mu))
        plt.savefig('Q1_Grid_{:2d}_unstable.png'.format(grid_intervals), dpi=400)
    plt.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 20 Grid Intervals, Courant Number = 0.5
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
finite_graph(grid_intervals_a)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 20 Grid Intervals, Unstable Version
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
finite_graph(grid_intervals_a, stable=False)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 40 Grid Intervals, Courant Number = 0.5
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
finite_graph(grid_intervals_b)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# 40 Grid Intervals, Unstable Version
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
finite_graph(grid_intervals_b, stable=False)
