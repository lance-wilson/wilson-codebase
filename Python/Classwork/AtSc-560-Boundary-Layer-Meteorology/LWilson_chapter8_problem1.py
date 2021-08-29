#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_chapter8_problem1.py
#
# Purpose:
#   Calculate the autocorrelations of a turbulence velocity dataset in Chapter
#   8, Problem 1, of "An Introduction to Boundary Layer Meteorology" by Roland
#   B. Stull using the exact and approximate methods.
#
# Syntax:
#   python3 LWilson_chapter8_problem1.py
#
# Modification History:
#   2020/04/30 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

measurements = np.array([5.5, 6.3, 7.4, 3.3, 3.8, 5.9, 6.1, 5.7, 6.3, 7.1, 4.8, 3.1, 2.1, 2.4, 3.0])
N = len(measurements)
auto_exact = np.empty(len(measurements))
auto_approx = np.empty(len(measurements))

# Exact Method: Equation 8.2.1a
for j in range(len(measurements)):
    a_k_bar = np.sum(measurements[:N-j])/(N-j)
    a_kj_bar = np.sum(measurements[j:N])/(N-j)
    k_diff = measurements[:N-j] - a_k_bar
    kj_diff = measurements[j:N] - a_kj_bar
    numerator = np.sum(k_diff * kj_diff[:N-j])
    denom1 = np.sqrt(np.sum(k_diff**2))
    denom2 = np.sqrt(np.sum(kj_diff**2))
    auto_exact[j] = numerator/(denom1 * denom2)

# Approximate Method: 8.2.1b
a_k_prime = measurements - np.mean(measurements)
variance_a = np.var(measurements)
for j in range(N):
    auto_approx[j] = np.mean(a_k_prime[:N-j] * a_k_prime[j:N])/variance_a

fig = plt.figure()
fig.add_subplot(211)
plt.plot(measurements)
plt.xlabel('Time (s)')
plt.ylabel('Turbulence Velocity')
plt.title('Time Series')

fig.add_subplot(212)
plt.plot(auto_exact, label='Exact')
plt.plot(auto_approx, label='Approx')
plt.legend()
plt.xlabel('Lag (s)')
plt.ylabel('Turbulence Velocity')
plt.title('Autocorrelations')

fig.tight_layout()
#plt.show()
plt.savefig('LWilson_ch8_1.png', dpi=400)

