#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   chapter7_problem7.py
#
# Purpose:
#   Use values of Q* (net radiation) to find dT_g/dt to find the temperature
#   of the ground surface and the net radiation into the ground (Q_g) using
#   the force restore method. Problem 7.7 in "An Introduction to Boundary
#   Layer Meteorology by Roland B. Stull.
#
# Syntax:
#   python3 chapter7_problem7.py
#
# Modification History:
#   2020/04/07 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

c_g = 1.3e6         # J m^-3 K^-1
t_m = 293.          # K
t_air = 293.        # K
a_fr_day = 3e-4     # s^-1
a_fr_night = 1e-4   # s^-1
nu_g = 2.4e-7       # m^2 s^-1
period = 86400      # s

d_s = np.sqrt((nu_g*period)/(4.*np.pi))
c_ga = c_g * d_s

# Local times from the problem (changing 02 to 26 for better plotting).
local_time = np.array([4., 6., 8., 10., 12., 14., 16., 18., 20., 22., 24., 26.])
# Changing signs of all values based on errata.
Q_star = np.array([80., 20., -100., -300., -500., -600., -400., -50., 120., 110., 100., 90.])

# List of actual indices in the array.
x_vals = np.linspace(0, len(local_time)-1, len(local_time))
# List of indices where the array should be interpolated.
x_vals_interp = np.linspace(0, len(local_time)-1, len(local_time)*8-7)
# Interpolate local time to 15 minute intervals.
local_time_interp = np.interp(x_vals_interp, x_vals, local_time)
#local_time_interp2 = np.arange(4., 26.25, 0.25)

# Interpolate Q* to the same 15 minute intervals.
q_star_interp = np.interp(x_vals_interp, x_vals, Q_star)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Incorrect attempt using 2 hour time steps.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
t_g = 293.  # K

for i, q_star in enumerate(Q_star[1:]):
    dTg_dt = -1.*q_star/c_ga + (2.*np.pi/period)*(t_m - t_g) - a_fr_day*(t_g-t_air)
    t_g = t_g + dTg_dt*3600.*(local_time[i+1] - local_time[i])
    q_g = -1.*(c_ga*dTg_dt + (2.*np.pi*c_ga/period)*(t_g - t_m))
    print(local_time[i+1], q_star, dTg_dt, t_g, q_g)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Correct attempt using 15 minute interpolated data.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
print('\nInterpolated:')

t_g = np.empty(len(q_star_interp))
q_g = np.empty(len(q_star_interp))
t_g[0] = 293.  # K

# Loop starts at index 1 to skip the first step.
for i, q_star in enumerate(q_star_interp[1:]):
    # Equation 7.6.3b, with different a_fr values as defined in the text.
    #   Calculates values for the current time step using the previous ground
    #   temperature.
    if t_g[i] >= t_air:
        dTg_dt = -1.*q_star/c_ga + (2.*np.pi/period)*(t_m - t_g[i]) - a_fr_day*(t_g[i]-t_air)
    if t_g[i] < t_air:
        dTg_dt = -1.*q_star/c_ga + (2.*np.pi/period)*(t_m - t_g[i]) - a_fr_night*(t_g[i]-t_air)
    # Simple calculation of new ground temperature using
    #   t_g_new = t_g_old + delta_t*dT_g/dt
    t_g[i+1] = t_g[i] + dTg_dt*3600.*(local_time_interp[i+1] - local_time_interp[i])
    # Equation 7.6.3c
    q_g[i+1] = -1.*(c_ga*dTg_dt + (2.*np.pi*c_ga/period)*(t_g[i+1] - t_m))
    print(local_time_interp[i+1], q_star, dTg_dt, t_g[i+1], q_g[i+1])

plt.plot(local_time_interp[1:], q_g[1:])
plt.title('Flux into the Ground')
plt.xlabel('Local Time (hours)')
plt.ylabel('Q$_G$ (J m$^{-2}$ s$^{-1}$)')
#plt.show()
plt.savefig('ch7_7_flux.png', dpi=400)

plt.figure()
plt.plot(local_time_interp[1:], t_g[1:])
plt.title('Ground Temperature')
plt.xlabel('Local Time (hours)')
plt.ylabel('T$_G$ (K)')
#plt.show()
plt.savefig('ch7_7_temp.png', dpi=400)

