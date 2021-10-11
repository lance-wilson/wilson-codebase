#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   lab2_LWilson_planck.py
#
# Purpose:
#   Plot the emission spectrums for the Sun and the Earth.
#
# Syntax:
#   python lab2_LWilson_planck.py
#
#   Input: None.
#
#   Output: The emission curve for each body.
#
# Modification History:
#   2020/02/14 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

wavelengths = np.arange(0.2,50.,0.1)    # micrometers

earth_temp = 300.   # Kelvin
sun_temp = 3000.   # Kelvin


h = 6.626e-34      #Planck's  Constant
k = 1.381e-23      #Boltzmann's Constant
c = 2.988e8        #Speed of Light


term_a = ((2. * h * c**2)/wavelengths**5)*(1e6)**4 # Convert to W/(m^2 * um * Sr)
term_b_earth = h * c/(k*earth_temp*wavelengths*1e-6)
term_b_sun = h * c/(k*sun_temp*wavelengths*1e-6)

earth_emission = term_a/(np.exp(term_b_earth) - 1.)
sun_emission = term_a/(np.exp(term_b_sun) - 1.)


plt.plot(wavelengths, earth_emission)
plt.xlabel('Wavelength ($\mathregular{\mu}$m)')
plt.ylabel('Spectral Radiance (W m$^{-2}$ $\mathregular{\mu}$m$^{-1}$ Sr$^{-1}$')
plt.title('Emission Spectrum for Earth')
plt.xlim(0.1,50)
plt.ylim(0,)
plt.savefig('lab2_LWilson_planck_earth.png', dpi = 400)

plt.figure()
plt.plot(wavelengths, sun_emission)
plt.xlabel('Wavelength ($\mathregular{\mu}$m)')
plt.ylabel('Spectral Radiance (W m$^{-2}$ $\mathregular{\mu}$m$^{-1}$ Sr$^{-1}$')
plt.title('Emission Spectrum for Sun')
plt.xlim(-1,50)
plt.ylim(2,1050000)
#plt.semilogy()
plt.tight_layout()
plt.savefig('lab2_LWilson_planck_sun.png', dpi = 400)

