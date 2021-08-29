#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   Homework_4_7.py
#
# Purpose:
#   Plot the vertical profile of temperature change due to advection between
#   2310 and 2230 CDT for the temperature change in Figure 3.10 of An
#   Introduction to Boundary Layer Meteorology by Roland Stull.
#
# Syntax:
#   python3 Homework_4_7.py
#
# Modification History:
#   2020/02/27 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

# Ruler values are measured in centimeters from 0 on the graph in the textbook.
temp_ruler_values = np.array([-0.4, -0.33, -0.4, -0.35, -0.33, -0.3, -0.35, -0.25, -0.25, -0.2, -0.15, -0.1, -0.05, 0., 0., 0., 0.35, 0.35])
temp_multiplication_factor = 5./0.85
temp_diffs = temp_ruler_values * temp_multiplication_factor

pressure_ruler_values = np.array([0.05, 0.25, 0.45, 0.7, 0.85, 1.05, 1.3, 1.6, 1.85, 2.1, 2.33, 2.5, 2.75, 2.95, 3.25, 3.45, 3.75, 4.])
pressure_mult_factor = 50./1.15
pressure = 950. - pressure_ruler_values * pressure_mult_factor

figure_b_mult_factor = 10./.9
figure_b_time_factor = 1.5/24.

turbulence_ruler_values = np.array([-1.75, -1.25, -.8, -0.55, -.375, -.25, -.07, -.05, -.02, -.01, -.01, -.005, 0., 0., 0., 0., 0., 0.])
turbulence = turbulence_ruler_values * figure_b_mult_factor * figure_b_time_factor

radiation_ruler_values = np.array([-.25, -.24, -.23, -.22, -.21, -.21] + [-0.2] * 12)
radiation = radiation_ruler_values * figure_b_mult_factor * figure_b_time_factor

subsidence_ruler_values = np.array([0., 0.1, 0.15, 0.2, 0.25, 0.25, 0.33, 0.35, 0.4, 0.42, 0.45, 0.5, 0.58, 0.6, 0.68, 0.8, 1.13, 1.55])
subsidence = subsidence_ruler_values * figure_b_mult_factor * figure_b_time_factor

advection = temp_diffs - turbulence - radiation - subsidence

# The following three lines are so that the grid can be behind the dots.
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.set_axisbelow(True)
plt.plot(advection, pressure)
plt.grid()
plt.title('Problem 7: Vertical Profile of Advection Contribution')
plt.xlabel('Temperature ($\degree$C)')
plt.ylabel('Pressure (mb)')
plt.gca().invert_yaxis()

#plt.show()
plt.savefig('problem_7.png', dpi=400)
