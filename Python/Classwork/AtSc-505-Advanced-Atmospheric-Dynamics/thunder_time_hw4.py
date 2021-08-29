#!/usr/bin/env python
#
# Name: thunder_time_hw4.py
#
# Purpose:  Determine how long it takes for thunder to reach you for a
#           lightning strike 1 km away at varying temperatures.
#

import matplotlib.pyplot as plt
import numpy as np

R = 287. # J kg^-1 K^-1
gamma = 1.4
distance = 1000. # m

temperature = np.arange(250,330,0.1)

times = distance/(np.sqrt(gamma*R*temperature))

plt.plot(temperature, times)
plt.title('Time for Thunder to Reach an Observer 1 km from\na Lightning Strike in Varying Temperature Conditions')
plt.xlabel(r'Temperature (K)')
plt.ylabel('Time (s)')
plt.savefig('thunder_time.png', dpi=500)
##plt.show()
