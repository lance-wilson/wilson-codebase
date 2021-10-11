# Lance Wilson
# AtSc 353
# 4/11/2017
#
# Summary: Plot the equilibrium temperature of the Earth as a function of albedo.

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

sigma = 5.67e-8  # Watts/(meter^2*Kelvin^4)
# Solar Constant
S_0 = 1368.0       # Watts/meter squared

# Albedo
alpha = np.arange(1001)/1000.0

temp_e = ((S_0*(1-alpha))/(4.0*sigma))**0.25

plt.plot(alpha,temp_e)
plt.xlabel('Albedo (percent)')
plt.ylabel('Temperature (Kelvin)')
plt.title('Variance of Equilibrium Temperature from Albedo')
plt.savefig('Albedo_Temp.png', dpi=300)
plt.close()

