# Reads in temperature data from each data file,and creates a histogram showing the
#     maximum, minimum, and average temperatures for each day, with error bars
#     plotted. The plot figure is saved to a file.
# 
# Input: Files for temperature data for each day march 29 through 31, find in files
#     "0329.txt", "0330.txt", "0331.txt"
#
# Output: A plot with file name "histogram_maxavgmin_LWilson.png"
#
# Syntax: python histogramEC_LWilson.py
#
# Written: Lance Wilson, March 2016

import matplotlib.pyplot as plt
import numpy as np


# Read in data from 3/29
fid1 = open('0329.txt', 'r') # Open the 0329.txt file
march29_str = fid1.read()  # Read in the data into a string
fid1.close()    # Close the 0329.txt file
march29_list = march29_str.split()    # Split the march29 string on spaces
march29f_list = []      # Create an empty list
# Loop through march29_list, convert from string to float, and
# append to march29f_list.
for num in march29_list:
    march29f_list.append(float(num))

fid2 = open('0330.txt', 'r') # Open the 0330.txt file
march30_str = fid2.read()  # Read in the data into a string
fid2.close()    # Close the 0330.txt file
march30_list = march30_str.split()    # Split the march30 string on spaces
march30f_list = []      # Create an empty list
# Loop through march30_list, convert from string to float, and
# append to march30f_list.
for num in march30_list:
    march30f_list.append(float(num))

fid3 = open('0331.txt', 'r') # Open the 0331.txt file
march31_str = fid3.read()  # Read in the data into a string
fid3.close()    # Close the 0331.txt file
march31_list = march31_str.split()    # Split the march31 string on spaces
march31f_list = []      # Create an empty list
# Loop through march31_list, convert from string to float, and
# append to march31f_list.
for num in march31_list:
    march31f_list.append(float(num))


# Convert lists to arrays
march29 = np.array(march29f_list)
march30 = np.array(march30f_list)
march31 = np.array(march31f_list)

# List of days
day = [29, 30, 31]
# List of days, subtracted to center histogram bars
day_center = [29-0.4, 30-0.4, 31-0.4]

# Calculate daily averages
avg1 = march29.mean()
avg2 = march30.mean()
avg3 = march31.mean()

# Find the maximum and minimum of march29 data
march29_max = max(march29)
march29_min = min(march29)
#print 'Max: ', march29_max, 'Min: ', march29_min

# Find the maximum and minimum of march30 data
march30_max = max(march30)
march30_min = min(march30)
#print 'Max: ', march30_max, 'Min: ', march30_min

# Find the maximum and minimum of march31 data
march31_max = max(march31)
march31_min = min(march31)
#print 'Max: ', march31_max, 'Min: ', march31_min

# List of maximum and minimum temperatures.
max_temp = [march29_max, march30_max, march31_max]
min_temp = [march29_min, march30_min, march31_min]

# Put average temperatures in a list
avg_temp = [avg1, avg2, avg3]

# Average temperature minus minimum temperature.
avg_minus_min = [(avg1 - march29_min), (avg2 - march30_min), (avg3 - march31_min)]
# Maximum minus average temperature.
max_minus_avg = [(march29_max - avg1), (march30_max - avg2), (march31_max - avg3)]

# Plot histogram
b1 = plt.bar(day_center, min_temp, width=0.8, label='Minimum Temp')

plt.title('Average, Minimum, and Maximum Daily Temperatures 3/29-3/31')
plt.xlabel('Day')
plt.ylabel('Average Temperature (F)')
plt.xticks(range(29,32))

# Error is 1.8 degree instrument error plus 0.5 degree precision error.
total_error = 2.3

# Plot error bars
e1 = plt.errorbar(day, min_temp, yerr=total_error, linestyle='None', ecolor='black', elinewidth=2.0, capsize=10, mew=2.0)

# Plot average minus min bar
b2 = plt.bar(day_center, avg_minus_min, width = 0.8, label='Average Temperature', color='green', bottom=min_temp, yerr=total_error, ecolor='black')
# Plot maximum minus average bar
b3 = plt.bar(day_center, max_minus_avg, width=0.8, label='Maximum Temperature', color='red', bottom=avg_temp, yerr=total_error, ecolor='black')

leg = plt.legend(loc='best')

# Save plot
plt.savefig('histogram_maxavgmin_LWilson.png', dpi=400)

# End of program
