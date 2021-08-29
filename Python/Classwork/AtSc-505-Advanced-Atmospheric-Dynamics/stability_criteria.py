#!/usr/bin/env python
#
# Name: stability_criteria.py
#
# Purpose:  Plot four wind profiles along with their first and second
#           derivatives to help determine if they meet Rayleigh's and
#           Fjortoft's Criteria for potential instability.
#

import matplotlib.pyplot as plt
import numpy as np

y = np.arange(-4., 4., 0.01)

profile_a = 4. - 2.*y**2
first_deriv_a = -4.*y
second_deriv_a = np.array([-4.] * len(y))

profile_b = np.cos(2.*y)
first_deriv_b = -2.*np.sin(2.*y)
second_deriv_b = -4.*np.cos(2.*y)

profile_c = 3.*y + 6.*y**2 + y**3
first_deriv_c = 3. + 12.*y + 3.*y**2
second_deriv_c = 12. + 6.*y

profile_d = np.exp(-2.*y**2)
first_deriv_d = -4.*y*np.exp(-2.*y**2)
second_deriv_d = -4.*np.exp(-2.*y**2) + 16.*(y**2)*np.exp(-2.*y**2)

fig = plt.figure()

# Part A
fig.add_subplot(221)
plt.plot(profile_a, y, label='u')
plt.plot(first_deriv_a, y, label='u\'')
plt.plot(second_deriv_a, y, label='u\'\'')
# Dashed line at 0.
plt.plot([0]*len(y), y, linestyle='dashed', color='black')
plt.xlabel('u')
plt.ylabel('y')
plt.ylim(-4,4)
plt.title(r'a) u = 4 - 2y$^{2}$')

# Part B
fig.add_subplot(222)
plt.plot(profile_b, y, label='u')
plt.plot(first_deriv_b, y, label='u\'')
plt.plot(second_deriv_b, y, label='u\'\'')
# Dashed line at 0.
plt.plot([0]*len(y), y, linestyle='dashed', color='black')
plt.xlabel('u')
plt.ylabel('y')
plt.ylim(-4,4)
plt.title(r'b) u = cos(2y)')

# Part C
fig.add_subplot(223)
plt.plot(profile_c, y, label='u')
plt.plot(first_deriv_c, y, label='u\'')
plt.plot(second_deriv_c, y, label='u\'\'')
# Dashed line at 0.
plt.plot([0]*len(y), y, linestyle='dashed', color='black')
plt.xlabel('u')
plt.ylabel('y')
plt.ylim(-4,4)
plt.title(r'c) u = 3y + 6y$^{2}$ + y$^{3}$')
#plt.legend(loc='best', ncol=3)

# Part D
fig.add_subplot(224)
plt.plot(profile_d, y, label='u')
plt.plot(first_deriv_d, y, label='u\'')
plt.plot(second_deriv_d, y, label='u\'\'')
# Dashed line at 0.
plt.plot([0]*len(y), y, linestyle='dashed', color='black')
plt.xlabel('u')
plt.ylabel('y')
plt.ylim(-4,4)
plt.title(r'd) u = e$^{-2y^{2}}$')

#fig.suptitle('Stability Criteria')
fig.legend(loc='lower center', ncol=3)

fig.tight_layout()

plt.savefig('stability_criteria.png', dpi=400)
