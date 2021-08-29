#!/usr/bin/env python3
#
# Name:
#   Nonlinear_graph_func.py
#
# Purpose:
#   Function of the nonlinear graph that did not need to be plotted for this
#   assignment since it is still unstable.
#
# Syntax:
#   from Nonlinear_graph_func import nonlinear_graph
#
#   Input: None.
#
#   Output: Plot of the centered difference and the exact solution.
#
# Modification History:
#   2019/02/22 - Lance Wilson:  Created.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Part 2: Nonlinear advection.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def nonlinear_graph(grid_intervals, filtered=True):
    x_range = np.linspace(0, 4.*math.pi, num=grid_intervals+1)
    x_step = 4.*math.pi/grid_intervals   # Meters
    c = 0.1   # m/s
    time_step = 0.5*x_step/(11.*c)   # Seconds

    # Centered difference arrays.
    u_cent = np.zeros([grid_intervals+1])
    # Initial condition (just need x since initial time = 0).
    u_cent_old = np.power(np.sin(x_range), 6)
    u_cent_old_old = np.zeros([grid_intervals+1])

    current_time = 0.

    # Initialize the plot with interactivity.
    fig = plt.figure()
    plt.ion()

    while (current_time < 30.):
        # Exact solution for comparison.
        u_exact = np.power(np.sin(x_range - (u_cent + c)*current_time), 6)
        for j in range(1,grid_intervals):
            mu = (u_cent_old[j] + c)*time_step/x_step
            # Centered Difference.
            if (current_time == 0.):
                u_cent[j] = u_cent_old[j] - mu * (u_cent_old[j+1] - u_cent_old[j-1])
            else:
                u_cent[j] = u_cent_old_old[j] - mu * (u_cent_old[j+1] - u_cent_old[j-1])

        # Apply a fourth order Shapiro filter.
        if filtered:
            for j in range(2, grid_intervals-1):
                u_cent[j] = (1./16.)*(-1.*u_cent[j-2] + 4.*u_cent[j-1] + 10.*u_cent[j] + + 4.*u_cent[j+1] - u_cent[j+2])

        # Copy data into old arrays for next time step.
        current_time += time_step
        u_cent_old_old = np.copy(u_cent_old)
        u_cent_old = np.copy(u_cent)

        plt.cla()
        plt.plot(x_range, u_exact, label=r'Exact u=sin$\mathregular{^6}$(x-ct)', color='Blue')
        plt.plot(x_range, u_cent, label='Leapfrog', color='Red')
        plt.xlim(0, 4.*math.pi)
        plt.xticks([0, math.pi, 2.0*math.pi, 3.0*math.pi, 4.0*math.pi],\
            ['$0$', r'$\mathregular{\pi}$', r'$2\mathregular{\pi}$', r'$3\mathregular{\pi}$', r'$4\mathregular{\pi}$'])
        plt.legend(loc='best')

        plt.xlabel('x (m)')
        plt.ylabel(r'u(x,t) (m $\mathregular{s^{-1}}$)')
        ##plt.show()
        plt.pause(0.05)

    if filtered:
        plt.title('{:2d} Grid Intervals, Nonlinear, Filtered'.format(grid_intervals, mu))
        plt.savefig('Q1_Grid_{:2d}_filtered.png'.format(grid_intervals), dpi=400)
    else:
        plt.title('{:2d} Grid Intervals, Nonlinear, Unfiltered'.format(grid_intervals, mu))
        plt.savefig('Q1_Grid_{:2d}_unfiltered.png'.format(grid_intervals), dpi=400)
    plt.close()
