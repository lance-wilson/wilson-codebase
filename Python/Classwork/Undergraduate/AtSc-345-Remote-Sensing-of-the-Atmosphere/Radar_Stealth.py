# Lance Wilson
# AtSc 345
# Purpose: Plots the maximum detectable range of aircraft with a range of cross-sectional areas.
# Modification History:
#   2016/10/26 - Lance Wilson: Written.

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

p_t = 1100000.
g = 10**3.4
p_r = 10**-11.4 * 10**-3
wavelength = 0.1
pi = 3.1415926535

coeff = (p_t*g*g*wavelength**2)/(64*pi**3*p_r)

sigma_list = range(1,1001)
sigma = np.array(sigma_list)
sigma = sigma/10.0

max_range = ((coeff*sigma)**0.25)/1000.0

plt.plot(sigma,max_range)
plt.xlabel('Cross-Sectional Area (m^2)')
plt.ylabel('Maximum Detectable Range (km)')
plt.title('Maxiumum Detectable Range of Stealth Aircraft')
plt.ylim(0,1000)
plt.savefig('Stealth_Plot.png', dpi=300)
