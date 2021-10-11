#!/usr/bin/env python3
#
# Purpose:
#   Code segment for integrating the nonlinear advection equation
#   du/dt + (u+c)du/dx = 0 using the leapfrog scheme.
#
# Modification History:
#   2019/02/22 - Lance Wilson:  Created.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Part 2: Nonlinear advection.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
grid_intervals = 20
x_range = np.linspace(0, 4.*math.pi, num=grid_intervals+1)
x_step = 4.*math.pi/grid_intervals   # Meters
c = 0.1   # m/s
time_step = 0.5*x_step/c   # Seconds

# Centered difference arrays.
u_cent = np.zeros([grid_intervals+1])
# Initial condition (just need x since initial time = 0).
u_cent_old = np.power(np.sin(x_range), 6)
u_cent_old_old = np.zeros([grid_intervals+1])

current_time = 0.

while (current_time < 30.):
    for j in range(1,grid_intervals):
        mu = (u_cent_old[j] + c)*time_step/x_step
        # Centered Difference.
        if (current_time == 0.):
            u_cent[j] = u_cent_old[j] - mu * (u_cent_old[j+1] - u_cent_old[j-1])
        else:
            u_cent[j] = u_cent_old_old[j] - mu * (u_cent_old[j+1] - u_cent_old[j-1])

    if filtered:
        for j in range(2, grid_intervals-1):
            u_cent[j] = (1./16.)*(-1.*u_cent[j-2] + 4.*u_cent[j-1] + 10.*u_cent[j] + + 4.*u_cent[j+1] - u_cent[j+2])

    current_time += time_step
    u_cent_old_old = np.copy(u_cent_old)
    u_cent_old = np.copy(u_cent)
