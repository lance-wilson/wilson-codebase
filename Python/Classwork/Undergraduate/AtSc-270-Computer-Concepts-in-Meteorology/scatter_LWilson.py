# Reads in data from a file containing values for day, latitude and longitude, MODIS
#     (a satellite) aerosol optical depth (aod), and NAAPS (a model) AOD data, and
#     creates a scatter plot of the data, and finds the best fit line, as well as a
#     one to one line. The plot is saved to a file.
# 
# Input: Input file called "naaps.txt", which contains data for the day, latitude,
#     longitude, modis aod data, and naaps aod data.
#
# Output: A scatter plot with file name "scatter_aod_LWilson.png"
#
# Syntax: python scatter_LWilson.py
#
# Written: Lance Wilson, March 2016

import matplotlib.pyplot as plt
import numpy as np

# Empty lists for file data.
day_list = []
latitude_list = []
longitude_list = []
modis_list = []
naaps_list = []

# Open "naaps.txt" file
file1 = open('naaps.txt', 'r')
while True:
    # Read in next line
    line = file1.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual lists
    day_list.append(float(line_list[0]))
    latitude_list.append(float(line_list[1]))
    longitude_list.append(float(line_list[2]))
    modis_list.append(float(line_list[3]))
    naaps_list.append(float(line_list[4]))
# Close file
file1.close()

# Convert lists to arrays
day = np.array(day_list)
latitide = np.array(latitude_list)
longitude = np.array(longitude_list)
modis_aod = np.array(modis_list)
naaps_aod = np.array(naaps_list)

# Find the maximum and minimum of modis aod data
modis_max = max(modis_aod)
modis_min = min(modis_aod)
print 'Max: ', modis_max, 'Min: ', modis_min

# Find best fit line
fcoeff = np.polyfit(modis_aod, naaps_aod, 1)
# Print coefficients and intercepts
print 'Expected Coefficient and intercept: 1, 0   Actual Coefficient and intercept: ', fcoeff

# Scatter polot
s1 = plt.scatter(modis_aod, naaps_aod, s = 25, c = 'crimson', label = 'data')
one_line = np.array([0,1])
# Plot a one to one line
plt.plot(one_line, one_line, 'k', label='one to one line')
# Plot best fit line
plt.plot(modis_aod, fcoeff[0]*modis_aod+fcoeff[1], 'r', label='Best Fit Line')

plt.title('Comparis of MODIS and NAAPS Aerosol Optical Depth measurements')
plt.xlabel('MODIS AOD')
plt.ylabel('NAAPS AOD')
plt.xlim([-0.1,1.1])
plt.ylim([-0.1,1.1])

# Create legend
leg = plt.legend(loc='upper left')
leg.legendHandles[2]._sizes = [1]

# Save file
plt.savefig('scatter_aod_LWilson.png', dpi=400)

# End of program
