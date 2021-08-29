#!/usr/bin/env python
#
# Author:  Lance Wilson
#
# Name: Brunt_Vaisala_HW2.py
#
# Purpose:  Calculate the vertical profile of Brunt Vaisala frequencies using a sounding from Aberdeen, South Dakota.
#

import numpy as np
import matplotlib.pyplot as plt

def theta_convert(temp, pressure):
    theta = (temp+273.15)*(1000./pressure)**(R/c_p)
    return theta

R = 287. # J kg^-1 K^-1
c_p = 1004. # J kg^-1 K^-1
g = 9.81 # m s^-2

sounding = 'ABR_2019_09_10_12Z_data.txt'

# Pressure (hPa), height (m), temperature (degrees C)
pressure, heights, temperature = np.genfromtxt(sounding, skip_header=5, usecols=(0,1,2), unpack=True)

# Potential temperature (Kelvin).
potential_temp = theta_convert(temperature, pressure)

# Rounding up to the first 100 m height interval.
initial_height = np.ceil(heights[0]/100.)*100.
# Get the non-inclusive second limit for the range function.
non_inclusive_top = np.ceil(heights[-1]/100.)*100.

# Calculate the size of the interpolated grid field.
array_length = int((non_inclusive_top - initial_height)/100)
# Allocate space for the interpolated height and potential temperature fields.
heights_interp = np.zeros((array_length))
theta_interp = np.zeros((array_length))
dtheta_dz = np.zeros((array_length))

# Starting index for the interpolation arrays.
i = 0

for height in np.arange(initial_height, non_inclusive_top, 100):
    # If there is a height in the original sounding that matches one of the
    #   interpolation points, no interpolation is necessary.
    if np.where(heights == height)[0]:
        heights_interp[i] = height
        index_of_height = np.where(heights == height)[0][0]
        theta_interp[i] = potential_temp[index_of_height]
        i += 1
        continue

    # Find all indices where the heights array has values less than this height.
    #   First index: just get indices from this row (in this case the only row).
    #   Second index: get the last of these indices (highest value less than height).
    lower_index = np.where(heights < height)[0][-1]
    # Find all indices where the heights array has values greater than this height.
    #   First index: just get indices from this row (in this case the only row).
    #   Second index: get the first of these indices (lowest value greater than
    #                 height).
    upper_index = np.where(heights > height)[0][0]

    # Surrounding elevations nearest the current height. 
    z_lower = heights[lower_index]
    z_upper = heights[upper_index]

    # Surrounding potential temperatures nearest the current height.
    theta_lower = potential_temp[lower_index]
    theta_upper = potential_temp[upper_index]

    # Weight fraction for calculating a linearly interpolated average.
    weight_fraction = (height - z_lower)/(z_upper - z_lower)

    # Calculate the interpolated average at this height.
    temp_interp = theta_upper * weight_fraction + theta_lower * (1. - weight_fraction)

    heights_interp[i] = height
    theta_interp[i] = temp_interp
    i += 1

# Get dtheta_dz using centered difference, except on boundaries, where forward
#   and backward difference are used.
##dtheta_dz[0] = (theta_interp[1] - theta_interp[0])/(heights_interp[1] - ##heights_interp[0])
##for j in range(1, array_length-1):
##    d_theta = theta_interp[j+1] - theta_interp[j-1]
##    dz = heights_interp[j+1] - heights_interp[j-1]
##    dtheta_dz[j] = d_theta/dz
##dtheta_dz[-1] = (theta_interp[-1] - theta_interp[-2])/(heights_interp[-1] - ##heights_interp[-2])

# Get dtheta_dz using centered difference, except on boundaries, where forward
#   and backward difference are used.
dtheta_dz = np.gradient(theta_interp)/np.gradient(heights_interp)

# Calculate the Brunt-Vaisala Frequency (N^2).
n_squared = (g/theta_interp)*dtheta_dz

# Output profile to file.
with open('brunt-vaisala_profile.txt', 'w') as outfile:
    outfile.write('Height (m)\tBrunt-Vaisala Frequency (1/s^2)\n')
    for k in range(array_length):
        outfile.write('{:.1f}\t\t{:.8f}\n'.format(heights_interp[k], n_squared[k]))

# Plot the vertical profile of N^2.
plt.plot(n_squared, heights_interp)
plt.title('Vertical profile of Brunt-Vaisala frequencies for\nAberdeen, South Dakota, at 12 UTC 10 Sept. 2019')
plt.xlabel(r's$^{-2}$')
plt.ylabel('m')
plt.ylim(0,max(heights_interp))
plt.savefig('brunt-vaisala_profile.png', dpi=500)
##plt.show()

