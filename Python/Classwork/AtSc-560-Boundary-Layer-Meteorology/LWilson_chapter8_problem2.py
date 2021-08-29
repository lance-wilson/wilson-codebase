#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_chapter8_problem2.py
#
# Purpose: 
#   Calculate the structure function and 2/3rds power fit of the same
#   data from problem 8.1.
#
# Syntax:
#   python3 LWilson_chapter8_problem2.py
#
# Modification History:
#   2020/04/30 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

measurements = np.array([5.5, 6.3, 7.4, 3.3, 3.8, 5.9, 6.1, 5.7, 6.3, 7.1, 4.8, 3.1, 2.1, 2.4, 3.0])
N = len(measurements)
structure_fn = np.empty(N)
structure_parameter = np.empty(N)

# Equation 8.3.1a
for j in range(N):
    structure_fn[j] = np.sum((measurements[:N-j] - measurements[j:N])**2)/(N-j)
    structure_parameter[j] = structure_fn[j]/(j)**(2./3.)

#power_fit = structure_parameter * np.arange(N)**(2/3)
power_fit = np.mean(structure_parameter[1:]) * np.arange(N)**(2/3)

fig = plt.figure()
fig.add_subplot(211)
plt.plot(structure_fn)
plt.xlabel('Lag (s)')
plt.ylabel('Turbulence Velocity')
plt.title('Structure Function')

fig.add_subplot(212)
plt.plot(structure_fn)
plt.plot(power_fit)
plt.xlabel('Lag (s)')
plt.ylabel('Turbulence Velocity')
plt.title('Two Thirds Power Fit')

fig.tight_layout()
#plt.show()
plt.savefig('LWilson_ch8_2.png', dpi=400)

