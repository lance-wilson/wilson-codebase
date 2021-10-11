#!usr/bin/env python
#
# graph.py
#
# Purpose: Graphs the average daily temperature, river height at noon, snow depth, and rate of change of
#          river level for each day from February through April for 2009-2012 for the Red River through Fargo and
#          Grand Forks using 600 lines of graphing fun!
#
# Input:  "awked_river_data_fargo.txt", "awked_river_data_grandforks.txt", which contain the height of the river
#         level at each day over the sample periods at Noon, and "Avg_Temp_FAR.txt", "Avg_Temp_GFK.txt" which
#         contain the average daily temperatures over the sample periods
#
# Output: "tempANDriver_far.png" and "tempANDriver_gfk.png", which show the average daily temperature and noon
#         river level over the three month sample period for each year, and "tempANDriver_far2.png" and
#         "tempANDriver_gfk2.png", which show the snow depth and rate of change of river height over the sample
#         period for each year
#
# Execution: python graph.py
#
# Note: Must have MatPlotLib ~ 1.5.1 or greater to run this program
#
# Written: Lance Wilson, April 2016
# Observed by: Jon Rosencrans, Bailey Mueller, Max Mueller
#

import matplotlib.pyplot as plt
import numpy as np

# Create empty lists to store the data from text files.
year_list = []
month_list = []
day_list = []
day_list_2009 = []
day_list_2010 = []
day_list_2011 = []
day_list_2012 = []
river_height_far_list = []
river_height_gfk_list = []
river_height_far_list_2009 = []
river_height_gfk_list_2009 = []
river_height_far_list_2010 = []
river_height_gfk_list_2010 = []
river_height_far_list_2011 = []
river_height_gfk_list_2011 = []
river_height_far_list_2012 = []
river_height_gfk_list_2012 = []
temp_far_list = []
temp_gfk_list = []
temp_far_list_2009 = []
temp_gfk_list_2009 = []
temp_far_list_2010 = []
temp_gfk_list_2010 = []
temp_far_list_2011 = []
temp_gfk_list_2011 = []
temp_far_list_2012 = []
temp_gfk_list_2012 = []
river_rate_far_2009_list = []
river_rate_far_2010_list = []
river_rate_far_2011_list = []
river_rate_far_2012_list = []
river_rate_gfk_2009_list = []
river_rate_gfk_2010_list = []
river_rate_gfk_2011_list = []
river_rate_gfk_2012_list = []
snow_far_list_2009 = []
snow_far_list_2010 = []
snow_far_list_2011 = []
snow_far_list_2012 = []
snow_gfk_list_2009 = []
snow_gfk_list_2010 = []
snow_gfk_list_2011 = []
snow_gfk_list_2012 = []

# Open files
file1 = open('awked_river_data_fargo.txt', 'r')
while True:
    # Read in next line
    line = file1.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual lists
    year_list.append(float(line_list[0]))
    month_list.append(float(line_list[1]))
    day_list.append(float(line_list[2]))
    river_height_far_list.append(float(line_list[4]))

# Close file
file1.close()

# Open files
file2 = open('awked_river_data_grandforks.txt', 'r')
while True:
    # Read in next line
    line = file2.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the river height data to a list (since its formatted the same as file1, don't need to read in date)
    river_height_gfk_list.append(float(line_list[4]))

# Close file
file2.close()

# Open files
file3 = open('Avg_Temp_FAR.txt', 'r')
while True:
    # Read in next line
    line = file3.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the temperature data to individual list
    temp_far_list.append(float(line_list[1]))
# Close file
file3.close()

# Open files
file4 = open('Avg_Temp_GFK.txt', 'r')
while True:
    # Read in next line
    line = file4.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual lists
    temp_gfk_list.append(float(line_list[1]))
# Close file
file4.close()

# Open file
file5 = open('2009_river_rate_FAR.txt', 'r')
while True:
    # Read in next line
    line = file5.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_far_2009_list.append(float(line_list[1]))
# Close file
file5.close()

# Open file
file6 = open('2010_river_rate_FAR.txt', 'r')
while True:
    # Read in next line
    line = file6.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_far_2010_list.append(float(line_list[1]))
# Close file
file6.close()

# Open file
file7 = open('2011_river_rate_FAR.txt', 'r')
while True:
    # Read in next line
    line = file7.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_far_2011_list.append(float(line_list[1]))
# Close file
file7.close()

# Open file
file8 = open('2012_river_rate_FAR.txt', 'r')
while True:
    # Read in next line
    line = file8.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_far_2012_list.append(float(line_list[1]))
# Close file
file8.close()

# Open file
file9 = open('2009_river_rate_GF.txt', 'r')
while True:
    # Read in next line
    line = file9.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_gfk_2009_list.append(float(line_list[1]))
# Close file
file9.close()

# Open file
file10 = open('2010_river_rate_GF.txt', 'r')
while True:
    # Read in next line
    line = file10.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_gfk_2010_list.append(float(line_list[1]))
# Close file
file10.close()

# Open file
file11 = open('2011_river_rate_GF.txt', 'r')
while True:
    # Read in next line
    line = file11.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_gfk_2011_list.append(float(line_list[1]))
# Close file
file11.close()

# Open file
file12 = open('2012_river_rate_GF.txt', 'r')
while True:
    # Read in next line
    line = file12.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    river_rate_gfk_2012_list.append(float(line_list[1]))
# Close file
file12.close()

# Open file
file13 = open('final_snowdepth_fargo_2009.txt', 'r')
while True:
    # Read in next line
    line = file13.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_far_list_2009.append(float(line_list[1]))
# Close file
file13.close()

# Open file
file14 = open('final_snowdepth_fargo_2010.txt', 'r')
while True:
    # Read in next line
    line = file14.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_far_list_2010.append(float(line_list[1]))
# Close file
file14.close()

# Open file
file15 = open('final_snowdepth_fargo_2011.txt', 'r')
while True:
    # Read in next line
    line = file15.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_far_list_2011.append(float(line_list[1]))
# Close file
file15.close()

# Open file
file16 = open('final_snowdepth_fargo_2012.txt', 'r')
while True:
    # Read in next line
    line = file16.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_far_list_2012.append(float(line_list[1]))
# Close file
file16.close()

# Open file
file17 = open('final_snowdepth_grandforks_2009.txt', 'r')
while True:
    # Read in next line
    line = file17.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_gfk_list_2009.append(float(line_list[1]))
# Close file
file17.close()

# Open file
file18 = open('final_snowdepth_grandforks_2010.txt', 'r')
while True:
    # Read in next line
    line = file18.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_gfk_list_2010.append(float(line_list[1]))
# Close file
file18.close()

# Open file
file19 = open('final_snowdepth_grandforks_2011.txt', 'r')
while True:
    # Read in next line
    line = file19.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_gfk_list_2011.append(float(line_list[1]))
# Close file
file19.close()

# Open file
file20 = open('final_snowdepth_grandforks_2012.txt', 'r')
while True:
    # Read in next line
    line = file20.readline()
    # Break if there was no line to read
    if not line: break
    # Create a list of data in the line
    line_list = line.split()
    # Add the data to individual list
    snow_gfk_list_2012.append(float(line_list[1]))
# Close file
file20.close()


# For days 0-89, year is 2009
for x in range(0,89):
    # Append the given range of each list into a year specific list for:
    # Day
    day_list_2009.append(day_list[x])
    # Fargo temperature
    temp_far_list_2009.append(temp_far_list[x])
    # Grand Forks temperature
    temp_gfk_list_2009.append(temp_gfk_list[x])
    # Fargo River Height
    river_height_far_list_2009.append(river_height_far_list[x])
    # Grand Forks River Height
    river_height_gfk_list_2009.append(river_height_gfk_list[x])
# For days 89-178, year is 2010
for x in range(89,178):
    day_list_2010.append(day_list[x])
    temp_far_list_2010.append(temp_far_list[x])
    temp_gfk_list_2010.append(temp_gfk_list[x])
    river_height_far_list_2010.append(river_height_far_list[x])
    river_height_gfk_list_2010.append(river_height_gfk_list[x])
# For days 178-267, year is 2011
for x in range(178,267):
    day_list_2011.append(day_list[x])
    temp_far_list_2011.append(temp_far_list[x])
    temp_gfk_list_2011.append(temp_gfk_list[x])
    river_height_far_list_2011.append(river_height_far_list[x])
    river_height_gfk_list_2011.append(river_height_gfk_list[x])
# For days 267-357, year is 2012
for x in range(267,357):
    day_list_2012.append(day_list[x])
    temp_far_list_2012.append(temp_far_list[x])
    temp_gfk_list_2012.append(temp_gfk_list[x])
    river_height_far_list_2012.append(river_height_far_list[x])
    river_height_gfk_list_2012.append(river_height_gfk_list[x])

# Convert lists to arrays
year = np.array(year_list)
month = np.array(month_list)
day_2009 = np.array(day_list_2009)
day_2010 = np.array(day_list_2010)
day_2011 = np.array(day_list_2011)
day_2012 = np.array(day_list_2012)
river_height_far_2009 = np.array(river_height_far_list_2009)
river_height_gfk_2009 = np.array(river_height_gfk_list_2009)
river_height_far_2010 = np.array(river_height_far_list_2010)
river_height_gfk_2010 = np.array(river_height_gfk_list_2010)
river_height_far_2011 = np.array(river_height_far_list_2011)
river_height_gfk_2011 = np.array(river_height_gfk_list_2011)
river_height_far_2012 = np.array(river_height_far_list_2012)
river_height_gfk_2012 = np.array(river_height_gfk_list_2012)
temp_far_2009 = np.array(temp_far_list_2009)
temp_gfk_2009 = np.array(temp_gfk_list_2009)
temp_far_2010 = np.array(temp_far_list_2010)
temp_gfk_2010 = np.array(temp_gfk_list_2010)
temp_far_2011 = np.array(temp_far_list_2011)
temp_gfk_2011 = np.array(temp_gfk_list_2011)
temp_far_2012 = np.array(temp_far_list_2012)
temp_gfk_2012 = np.array(temp_gfk_list_2012)
river_rate_far_2009 = np.array(river_rate_far_2009_list)
river_rate_far_2010 = np.array(river_rate_far_2010_list)
river_rate_far_2011 = np.array(river_rate_far_2011_list)
river_rate_far_2012 = np.array(river_rate_far_2012_list)
river_rate_gfk_2009 = np.array(river_rate_gfk_2009_list)
river_rate_gfk_2010 = np.array(river_rate_gfk_2010_list)
river_rate_gfk_2011 = np.array(river_rate_gfk_2011_list)
river_rate_gfk_2012 = np.array(river_rate_gfk_2012_list)
snow_far_2009 = np.array(snow_far_list_2009)
snow_far_2010 = np.array(snow_far_list_2010)
snow_far_2011 = np.array(snow_far_list_2011)
snow_far_2012 = np.array(snow_far_list_2012)
snow_gfk_2009 = np.array(snow_gfk_list_2009)
snow_gfk_2010 = np.array(snow_gfk_list_2010)
snow_gfk_2011 = np.array(snow_gfk_list_2011)
snow_gfk_2012 = np.array(snow_gfk_list_2012)


# Modify March and April days so that each array has values measure in days from February first
for y in range(28,59):
    day_2009[y] = day_2009[y] + 28
for y in range(59,89):
    day_2009[y] = day_2009[y] + 59
for y in range(28,59):
    day_2010[y] = day_2010[y] + 28
for y in range(59,89):
    day_2010[y] = day_2010[y] + 59
for y in range(28,59):
    day_2011[y] = day_2011[y] + 28
for y in range(59,89):
    day_2011[y] = day_2011[y] + 59
for y in range(29,60):
    day_2012[y] = day_2012[y] + 29
for y in range(60,90):
    day_2012[y] = day_2012[y] + 60


# Variables for vertical line for February/March division
x = [29] * 3
y = [-20, 30, 70]
# Variables for vertical line for March/April division
x2 = [60] * 3
y2 = [-20, 30, 70]
# Variables for Freezing line
x3 = [0, 45, 90]
y3 = [32, 32, 32]
# Variables for 0 ft/day level
x4 = [0, 45, 90]
y4 = [0, 0, 0]

# Fargo
# Define first figure and divide into two subplots with a shared x-axis
fig9, axarr = plt.subplots(2, sharex=True)
# Plot each year's temperatures over time
axarr[0].plot(day_2009, temp_far_2009, label = '2009', color='firebrick')
axarr[0].plot(day_2010, temp_far_2010, label = '2010', color='b')
axarr[0].plot(day_2011, temp_far_2011, label = '2011', color='turquoise')
axarr[0].plot(day_2012, temp_far_2012, label = '2012', color='magenta')
# Plot Month vertical lines
axarr[0].plot(x, y, 'g')
axarr[0].plot(x2, y2, 'g')
# Plot Freezing line
axarr[0].plot(x3, y3, label='Freezing Temp', linestyle='--', color='c')
# Title and y-axis label
axarr[0].set_title('Temperature Fargo')
axarr[0].set_ylabel('Temperature (F)')
# Small legend with two columns
axarr[0].legend(loc='best',fontsize='small', ncol=2)
# Plot each year's river height over time
axarr[1].plot(day_2009, river_height_far_2009, label = '2009', color='firebrick')
axarr[1].plot(day_2010, river_height_far_2010, label = '2010', color='b')
axarr[1].plot(day_2011, river_height_far_2011, label = '2011', color='turquoise')
axarr[1].plot(day_2012, river_height_far_2012, label = '2012', color='magenta')
# Plot month vertical lines
axarr[1].plot(x, y, 'g')
axarr[1].plot(x2, y2, 'g')
# Title and y-axis label
axarr[1].set_title('River Height Fargo')
axarr[1].set_ylabel('River Level (ft)')
# y-axis from 10 to 45 feet
axarr[1].set_ylim([10,45])
# Small legend with two columns
axarr[1].legend(loc='upper left', ncol = 2, fontsize = 'small')
# x-axis label for entire plot
plt.xlabel('Days since February 1')
# Save file
plt.savefig('tempANDriver_far.png', dpi=400)

fig10, axarr = plt.subplots(2, sharex=True)
# Plot each year's snow depth over time
axarr[0].plot(day_2009, snow_far_2009, label = '2009', color='firebrick')
axarr[0].plot(day_2010, snow_far_2010, label = '2010', color='b')
axarr[0].plot(day_2011, snow_far_2011, label = '2011', color='turquoise')
axarr[0].plot(day_2012, snow_far_2012, label = '2012', color='magenta')
# Plot Month vertical lines
axarr[0].plot(x, y, 'g')
axarr[0].plot(x2, y2, 'g')
# Title and y-axis label
axarr[0].set_title('Snow Depth Fargo')
axarr[0].set_ylabel('Snow Depth (in)')
# y-axis from 0 o 22 inches
axarr[0].set_ylim([0,22])
# Small legend with two columns
axarr[0].legend(loc='best',fontsize='small', ncol=2)
# Plot each year's rate of change of river level over time
axarr[1].plot(day_2009, river_rate_far_2009, label = '2009', color='firebrick')
axarr[1].plot(day_2010, river_rate_far_2010, label = '2010', color='b')
axarr[1].plot(day_2011, river_rate_far_2011, label = '2011', color='turquoise')
axarr[1].plot(day_2012, river_rate_far_2012, label = '2012', color='magenta')
# Plot Month vertical lines
axarr[1].plot(x, y, 'g')
axarr[1].plot(x2, y2, 'g')
# Plot 0 line
axarr[1].plot(x4, y4, color='k')
# Title and y-axis label
axarr[1].set_title('Rate of Change of River Level Fargo')
axarr[1].set_ylabel('River Level Change (ft/day)')
# y-axis from -1.5 to 5 feet/day
axarr[1].set_ylim([-1.5,5])
# Small legend with two columns
axarr[1].legend(loc='best',fontsize='small', ncol=2)
# x-axis label for entire plot
plt.xlabel('Days since February 1')
# Save file
plt.savefig('tempANDriver_far2.png', dpi=400)


# Grand Forks
# Define second figure and divide into two subplots with a shared x-axis
fig11, axarr = plt.subplots(2, sharex=True)
# Plot each year's temperatures over time
axarr[0].plot(day_2009, temp_gfk_2009, label = '2009', color='firebrick')
axarr[0].plot(day_2010, temp_gfk_2010, label = '2010', color='b')
axarr[0].plot(day_2011, temp_gfk_2011, label = '2011', color='turquoise')
axarr[0].plot(day_2012, temp_gfk_2012, label = '2012', color='magenta')
# Plot month verical lines
axarr[0].plot(x, y, 'g')
axarr[0].plot(x2, y2, 'g')
# Plot freezling line
axarr[0].plot(x3, y3, label='Freezing Temp', linestyle='--', color='c')
# Title and y-axis label
axarr[0].set_title('Temperature Grand Forks')
axarr[0].set_ylabel('Temperature (F)')
# Small legend with two columns
axarr[0].legend(loc='best',fontsize='small', ncol=2)
# Plot each year's temperatures over time
axarr[1].plot(day_2009, river_height_gfk_2009, label = '2009', color='firebrick')
axarr[1].plot(day_2010, river_height_gfk_2010, label = '2010', color='b')
axarr[1].plot(day_2011, river_height_gfk_2011, label = '2011', color='turquoise')
axarr[1].plot(day_2012, river_height_gfk_2012, label = '2012', color='magenta')
# Plot month verical lines
axarr[1].plot(x, y, 'g')
axarr[1].plot(x2, y2, 'g')
# Title and y-axis label
axarr[1].set_title('River Height Grand Forks')
axarr[1].set_ylabel('River Level (ft)')
# y-axis range from 15 to 55 feet
axarr[1].set_ylim([15,55])
# Small legend with two columns
axarr[1].legend(loc='upper left', ncol = 2, fontsize = 'small')
# x-axis label for entire plot
plt.xlabel('Days since February 1')
# Save file
plt.savefig('tempANDriver_gfk.png', dpi=400)

fig12, axarr = plt.subplots(2, sharex=True)
# Plot each year's snow depth over time
axarr[0].plot(day_2009, snow_gfk_2009, label = '2009', color='firebrick')
axarr[0].plot(day_2010, snow_gfk_2010, label = '2010', color='b')
axarr[0].plot(day_2011, snow_gfk_2011, label = '2011', color='turquoise')
axarr[0].plot(day_2012, snow_gfk_2012, label = '2012', color='magenta')
# Plot Month vertical lines
axarr[0].plot(x, y, 'g')
axarr[0].plot(x2, y2, 'g')
# Title and y-axis label
axarr[0].set_title('Snow Depth Grand Forks')
axarr[0].set_ylabel('Snow Depth (in)')
# y-axis from 0 to 15 inches
axarr[0].set_ylim([0,15])
# Small legend with two columns
axarr[0].legend(loc='best',fontsize='small', ncol=2)
# Plot each year's rate of change of river level over time
axarr[1].plot(day_2009, river_rate_gfk_2009, label = '2009', color='firebrick')
axarr[1].plot(day_2010, river_rate_gfk_2010, label = '2010', color='b')
axarr[1].plot(day_2011, river_rate_gfk_2011, label = '2011', color='turquoise')
axarr[1].plot(day_2012, river_rate_gfk_2012, label = '2012', color='magenta')
# Plot Month vertical lines
axarr[1].plot(x, y, 'g')
axarr[1].plot(x2, y2, 'g')
# Plot 0 line
axarr[1].plot(x4, y4, color='k')
# Title and y-axis label
axarr[1].set_title('Rate of Change of River Level Grand Forks')
axarr[1].set_ylabel('River Level Change (ft/day)')
# y-axis from -1.5 to 8 feet/day
axarr[1].set_ylim([-1.5,8])
# Small legend with two columns
axarr[1].legend(loc='best',fontsize='small', ncol=2)
# x-axis label for entire plot
plt.xlabel('Days since February 1')
# Save file
plt.savefig('tempANDriver_gfk2.png', dpi=400)
# End of marathon
