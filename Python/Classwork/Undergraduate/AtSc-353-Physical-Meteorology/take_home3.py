# Lance Wilson
# AtSc 353
# 4/20/2017
#
# Summary: Plot the equilibrium temperature of the Earth as a function of albedo
#          over the past 300 million years.

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

sigma = 5.67e-8  # Watts/(meter^2*Kelvin^4)
alpha = 0.3      # Albedo

megayears_ago = -np.arange(-300,1)

# Solar "Constant"
megayearly_percentage = np.arange(301)/300.0
Solar_brightening = (0.7 + 0.3*megayearly_percentage)
S_0 = 1368.0*Solar_brightening       # Watts/meter squared


temp_e_noalpha = (S_0/(4.0*sigma))**0.25
temp_e_alpha = ((S_0*(1-alpha))/(4.0*sigma))**0.25

plt.plot(megayears_ago, temp_e_noalpha, label='No Albedo')
plt.plot(megayears_ago, temp_e_alpha, label='Albedo 30%')
plt.legend(loc='upper left')
plt.xlabel('Millions of Years Ago')
plt.ylabel('Equilibrium Temperature (Kelvin)')
plt.gca().invert_xaxis()
plt.title('Variance of Equilibrium Temperature from\n Long Term Variance in Solar Constant')
plt.savefig('TakeHome_Temp.png', dpi=300)
plt.close()

