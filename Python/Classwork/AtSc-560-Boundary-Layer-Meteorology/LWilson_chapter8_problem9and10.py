#                                                               Lance Wilson
# Name:
#   LWilson_chapter8_problem9and10.py
#
# Purpose:
#   Chapter 8, Problem 9:
#   ----------------------------
#   Compute the Fast Fourier Transform for temperature and vertical velocity
#   data in Chapter 8, Problem 9 of "An Introduction to Boundary Layer
#   Meteorology" by Roland B. Stull.
#
#   Chapter 8, Problem 10:
#   ----------------------------
#   Compute the inverse Fast Fourier Transform for modified transformed
#   temperature data in Chapter 8, Problem 10 of "An Introduction to Boundary
#   Layer Meteorology" by Roland B. Stull.
#
# Syntax:
#   python3 LWilson_chapter8_problem9and10.py
#
# Modification History:
#   2020/05/05 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Chapter 8, Problem 9
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
time = np.arange(0, 210, 10)
# Temperature (degrees C)
temperature = np.array([25., 23., 21., 21., 30., 20., 24., 23., 23., 24, 23., 20., 19., 20., 25., 21., 25., 23., 21., 20., 19.])
# Vertical Velocity (m/s)
w = np.array([2., 2., -1., 1., 4., -3., 3., 1., 2., 3., -1., -4., -1., 1., 3., 0., 1., 0., -2., -1., -2.])

temp_fft = np.fft.fft(temperature)
# Save FFT of temperature for the next problem.
w_fft = np.fft.fft(w)

fig = plt.figure()
fig.add_subplot(211)
plt.plot(time, temperature)
plt.xlabel('Time (s)')
plt.ylabel('Temperature ($\degree$C)')
plt.title('Original Temperature Data')

fig.add_subplot(212)
plt.plot(time[1:], temp_fft[1:])
plt.xlabel('Time (s)')
plt.ylabel('Temperature ($\degree$C)')
plt.title('Fast Fourier Transform')

fig.tight_layout()
#plt.show()
plt.savefig('LWilson_ch8_9_T.png', dpi=400)

fig = plt.figure()
fig.add_subplot(211)
plt.plot(time, w)
plt.xlabel('Time (s)')
plt.ylabel('Vertical Velocity (m/s)')
plt.title('Original Velocity Data')

fig.add_subplot(212)
plt.plot(time[1:], w_fft[1:])
plt.xlabel('Time (s)')
plt.ylabel('Vertical Velocity (m/s)')
plt.title('Fast Fourier Transform')

fig.tight_layout()
#plt.show()
plt.savefig('LWilson_ch8_9_w.png', dpi=400)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Chapter 8, Problem 10
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
N = len(temp_fft)
temp_fft[int((N-1)/2)-5:int((N-1)/2)+6] = 0.

new_temp = np.fft.ifft(temp_fft)

fig = plt.figure()
fig.add_subplot(211)
plt.plot(time, temperature)
plt.xlabel('Time (s)')
plt.ylabel('Temperature ($\degree$C)')
plt.title('Original Temperature Data')

fig.add_subplot(212)
plt.plot(time, new_temp)
plt.xlabel('Time (s)')
plt.ylabel('Temperature ($\degree$C)')
plt.title('Inverted Modified Fast Fourier Transform')

fig.tight_layout()
#plt.show()
plt.savefig('LWilson_ch8_10.png', dpi=400)

