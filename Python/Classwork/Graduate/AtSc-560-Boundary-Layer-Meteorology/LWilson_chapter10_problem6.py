#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   chapter10_problem6.py
#
# Purpose:
#   Calculate and plot u'w'_bar and w'theta_v'_bar from 0 to 50 meters using
#   data from chapter 5, problem 26. Problem 10.6 in "An Introduction to
#   Boundary Layer Meteorology" by Roland B. Stull
#
# Syntax:
#   python3 chapter10_problem6.py
#
# Modification History:
#   2020/04/07 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

k_m = 5.    # m^2 s^-1
k_h = k_m   # This is an assumption made for this problem.

height = np.array([0., 10., 20., 30., 40., 50., 60.])
theta_v_bar = np.array([293., 292., 292., 294., 298., 300., 301.])
u_bar = np.array([2., 7., 7., 8., 10., 14., 15.])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Using centered difference for all values except 0 to 10 m (where forward
#   difference is used).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
height_grad = np.gradient(height)
theta_v_grad = np.gradient(theta_v_bar)
u_bar_grad = np.gradient(u_bar)

# From equation 10.7.3
uw_prime = -1.*k_m*u_bar_grad/height_grad

# Equation 10.7.2
wtheta_prime = -1.*k_h*theta_v_grad/height_grad

plt.plot(uw_prime[:-1], height[:-1], label=r"$\overline{u'w'}$")
plt.plot(wtheta_prime[:-1], height[:-1], label=r"$\overline{w'\theta_v'}$")
plt.title('Problem 10, Problem 6, Centered Difference')
plt.xlabel('Kinematic flux (K m/s or m$^2$/s$^2$)')
plt.ylabel('Height (m)')
plt.legend()
#plt.show()
plt.savefig('ch10_6_centered.png', dpi=400)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Using forward difference for all values.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
height_grad2 = np.diff(height)
theta_v_grad2 = np.diff(theta_v_bar)
u_bar_grad2 = np.diff(u_bar)

# From equation 10.7.3
uw_prime2 = -1.*k_m*u_bar_grad2/height_grad2

# Equation 10.7.2
wtheta_prime2 = -1.*k_h*theta_v_grad2/height_grad2

plt.figure()
plt.plot(uw_prime2, height[:-1], label=r"$\overline{u'w'}$")
plt.plot(wtheta_prime2, height[:-1], label=r"$\overline{w'\theta_v'}$")
plt.title('Problem 10, Problem 6, Forward Difference')
plt.xlabel('Kinematic flux (K m/s or m$^2$/s$^2$)')
plt.ylabel('Height (m)')
plt.legend()
#plt.show()
plt.savefig('ch10_6_forward.png', dpi=400)
