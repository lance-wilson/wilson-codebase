# Lance Wilson
# AtSc 353
# 2/2/2017
#
# Summary: Under ideal conditions, this program graphs equations of the change
#          in radius and mass as a water droplet grows by condensation.

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

pi = 3.1415926535
r_i = 0.75   #micrometers
G_l = 100.0  #micrometers squared/second
rho_l = 1000 #kilograms/meter cubed
S = 0.0005

t = np.arange(50001)

r = np.sqrt(2*G_l*S*t+r_i**2)

M = 4*pi*r*G_l*rho_l*S*t*1e-18+1.767e-15


plt.plot(t,r)
plt.xlabel('Time (seconds)')
plt.ylabel('Radius (micrometers)')
plt.title('Growth of Droplet by Radius, Supersaturation ' + str(S))
plt.savefig('S0005_radius.png', dpi=300)
plt.close()

plt.plot(t,M)
plt.xlabel('Time (seconds)')
plt.ylabel('Mass (kilograms)')
plt.title('Growth of Droplet by Mass, Supersaturation ' + str(S))
plt.savefig('S0005_mass.png', dpi=300)
