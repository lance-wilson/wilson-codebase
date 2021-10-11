# Reads in temperature data from each data file,and creates a histogram showing the
#     average temperatures for each day, with error bars plotted. The plot figure is
#     saved to a file.
# 
# Input: Files for temperature data for each day march 29 through 31, find in files
#     "0329.txt", "0330.txt", "0331.txt"
#
# Output: A plot with file name "histogram_avgtemps_LWilson.png"
#
# Syntax: python histogram_LWilson.py
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

# Put average temperatures in a list
avg_temp = [avg1, avg2, avg3]

# Plot histogram
b1 = plt.bar(day_center, avg_temp, width=0.8)

plt.title('Average Daily Temperatures 3/29-3/31')
plt.xlabel('Day')
plt.ylabel('Average Temperature (F)')
plt.xticks(range(29,32))

# Error is 1.8 degree instrument error plus 0.5 degree precision error.
total_error = 2.3

# Plot error bars
e1 = plt.errorbar(day, avg_temp, yerr=total_error, linestyle='None', ecolor='black', elinewidth=2.0, capsize=10, mew=2.0)

# Save plot
plt.savefig('histogram_avgtemps_LWilson.png', dpi=400)

# End of program
