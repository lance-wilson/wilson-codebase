#!/usr/bin/env python3
#
# Name:
#   FDR.py
#
# Purpose:
#   To reproduce the Kalnay plots 2.3.3, 2.4.1, and 2.4.2, using the n^2
#	equation (Kalnay 2.3.22), solved for wave frequency in terms o fhorizontal
#	wave number) for the unfiltered, hydrostatic (alpha = 0), and anelastic
#	(beta = 0) cases in an isothermal atmosphere.
#
# Syntax:
#   Single file: python FDR.py
#
#   Input: None.
#
#   Output: Three plots that hopefully resemble the Kalnay plots.
#
# Modification History:
#   2019/01/21 - Lance Wilson:  Created.

import math
import matplotlib.pyplot as plt
import numpy as np

f = 1e-4   # Coriolis frequency (1/s).
f_squared = f**2

N = 1e-2
N_squared = 1e-4        # Brunt-Vasala Frequency (1/s^2).

c_sound = 343.   # Speed of Sound (m/s).
c_sound_sq = c_sound**2

g = 9.80665     # Standard Acceleration due to gravity (m/s^2).

chi = (c_sound_sq/4.) * ((g/c_sound_sq) + (N_squared/g))**2
anelastic_chi = g**2/(4.*c_sound_sq)

k = np.logspace(-7., -3., num=200)  # Wave Number (1/m).
k_squared = np.square(k)

# Lamb Wave term.
nu_lamb = np.sqrt(f_squared + c_sound_sq * k_squared)
# n^2 = infinity term.
nu_inf = np.array([f] * len(k))

N_reference = np.array([N] * len(k))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# No Filtering (alpha = 1, beta = 1)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
term_1 = f_squared + c_sound_sq*k_squared + N_squared + chi
term_2 = term_1**2 - 4. * (N_squared * (f_squared + c_sound_sq * k_squared) + chi * f_squared)
# n^2 = 0 terms.
nu_1 = np.sqrt(0.5*(term_1 + np.sqrt(term_2)))
nu_2 = np.sqrt(0.5*(term_1 - np.sqrt(term_2)))

plt.plot(k, nu_1, label='n^2 = 0, + sqrt', color='blue')
plt.plot(k, nu_2, label='n^2 = 0, - sqrt', color='blue')
plt.plot(k, nu_lamb, label='Lamb Wave', color='red')
plt.plot(k, nu_inf, label='n^2 = inf', color='green')
plt.plot(k, N_reference, linestyle='dashed', color='darkorange')

plt.xlim(0.5*1e-7, 5*1e-3)
plt.ylim(1e-5, 0.9)
plt.legend(loc='upper left')

plt.xscale('log')
plt.yscale('log', nonposy='clip')

plt.title(r'No Filtering ($\alpha$, $\beta$ = 1)')
plt.xlabel('Horizontal Wave Number (k) (1/m)')
plt.ylabel(r'Wave Frequency ($\nu$) (1/s)')

plt.savefig('Unfiltered.png', dpi=400)
plt.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Hydrostatic Approximation (alpha = 0, beta = 1)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
hydro_numerator = N_squared * (f_squared + c_sound_sq*k_squared) + chi * f_squared
hydro_denominator = N_squared + chi
nu_hydro = np.sqrt(hydro_numerator/hydro_denominator)

plt.plot(k, nu_hydro, label='n^2 = 0', color='blue')
plt.plot(k, nu_lamb, label='Lamb Wave', color='red')
plt.plot(k, nu_inf, label='n^2 = inf', color='green')
plt.plot(k, N_reference, linestyle='dashed', color='darkorange')

plt.xlim(0.5*1e-7, 5*1e-3)
plt.ylim(1e-5, 0.9)
plt.legend(loc='upper left')

plt.xscale('log')
plt.yscale('log', nonposy='clip')

plt.title(r'Hydrostatic ($\alpha$ = 0, $\beta$ = 1)')
plt.xlabel('Horizontal Wave Number (k) (1/m)')
plt.ylabel(r'Wave Frequency ($\nu$) (1/s)')

plt.savefig('Hydrostatic.png', dpi=400)
plt.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Anelastic Approximation (alpha = 1, beta = 0)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
anelastic_1 = N_squared * c_sound_sq * k_squared + anelastic_chi * f_squared
anelastic_2 = c_sound_sq * k_squared + anelastic_chi
nu_anelastic = np.sqrt(anelastic_1/anelastic_2)

plt.plot(k, nu_anelastic, label='n^2 = 0', color='blue')
plt.plot(k, nu_inf, label='n^2 = inf', color='green')
plt.plot(k, N_reference, linestyle='dashed', color='darkorange')

plt.xlim(0.5*1e-7, 5*1e-3)
plt.ylim(1e-5, 0.9)
plt.legend(loc='upper left')

plt.xscale('log')
plt.yscale('log', nonposy='clip')

plt.title(r'Anelastic ($\alpha$ = 1, $\beta$ = 0)')
plt.xlabel('Horizontal Wave Number (k) (1/m)')
plt.ylabel(r'Wave Frequency ($\nu$) (1/s)')

plt.savefig('Anelastic.png', dpi=400)
