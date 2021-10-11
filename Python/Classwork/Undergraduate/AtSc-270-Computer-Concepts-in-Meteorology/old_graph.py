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



#bar_width = 0.4
#time_center = time - (bar_width/2.0)

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


fig1 = plt.figure()
plt.plot(day_2009, river_height_far_2009, label = 'River Height')
plt.plot(day_2009, temp_far_2009, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Fargo, 2009')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_far_2009.png', dpi=400)

fig2 = plt.figure(2)
plt.plot(day_2009, river_height_gfk_2009, label = 'River Height')
plt.plot(day_2009, temp_gfk_2009, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Grand Forks, 2009')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_gfk_2009.png', dpi=400)


fig3 = plt.figure(3)
plt.plot(day_2010, river_height_far_2010, label = 'River Height')
plt.plot(day_2010, temp_far_2010, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Fargo, 2010')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_far_2010.png', dpi=400)

fig4 = plt.figure(4)
plt.plot(day_2010, river_height_gfk_2010, label = 'River Height')
plt.plot(day_2010, temp_gfk_2010, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Grand Forks, 2010')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_gfk_2010.png', dpi=400)

fig5 = plt.figure(5)
plt.plot(day_2011, river_height_far_2011, label = 'River Height')
plt.plot(day_2011, temp_far_2011, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Fargo, 2011')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_far_2011.png', dpi=400)

fig6 = plt.figure(6)
plt.plot(day_2011, river_height_gfk_2011, label = 'River Height')
plt.plot(day_2011, temp_gfk_2011, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Grand Forks, 2011')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_gfk_2011.png', dpi=400)

fig7 = plt.figure(7)
plt.plot(day_2012, river_height_far_2012, label = 'River Height')
plt.plot(day_2012, temp_far_2012, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Fargo, 2012')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_far_2012.png', dpi=400)

fig8 = plt.figure(8)
plt.plot(day_2012, river_height_gfk_2012, label = 'River Height')
plt.plot(day_2012, temp_gfk_2012, label = 'Temperature', color='firebrick')
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
plt.title('River heights and temperature over time at Grand Forks, 2012')
plt.xlabel('Days from February 1')
plt.ylabel('Height (ft), Temperature (F)')
plt.legend(loc='upper left')
plt.savefig('tempVSriver_gfk_2012.png', dpi=400)


fig9 = plt.figure(9)
plt.bar(day_2009, snow_far_2009, label = 'Snow Depth', color='cyan')
plt.plot(day_2009, temp_far_2009, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Fargo 2009')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-15,55])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_far_2009.png')


fig10 = plt.figure(10)
plt.bar(day_2010, snow_far_2010, label = 'Snow Depth', color='cyan')
plt.plot(day_2010, temp_far_2010, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Fargo 2010')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-10,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_far_2010.png')

fig11 = plt.figure(11)
plt.bar(day_2011, snow_far_2011, label = 'Snow Depth', color='cyan')
plt.plot(day_2011, temp_far_2011, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Fargo 2011')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-12,60])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_far_2011.png')

fig12 = plt.figure(12)
plt.bar(day_2012, snow_far_2012, label = 'Snow Depth', color='cyan')
plt.plot(day_2012, temp_far_2012, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Fargo 2012')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-5,70])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_far_2012.png')

fig13 = plt.figure(13)
plt.bar(day_2009, snow_gfk_2009, label = 'Snow Depth', color='cyan')
plt.plot(day_2009, temp_gfk_2009, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Grand Forks 2009')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-15,55])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_gfk_2009.png')

fig14 = plt.figure(14)
plt.bar(day_2010, snow_gfk_2010, label = 'Snow Depth', color='cyan')
plt.plot(day_2010, temp_gfk_2010, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Grand Forks 2010')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-10,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_gfk_2010.png')

fig15 = plt.figure(15)
plt.bar(day_2011, snow_gfk_2011, label = 'Snow Depth', color='cyan')
plt.plot(day_2011, temp_gfk_2011, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Grand Forks 2011')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-15,60])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_gfk_2011.png')

fig16 = plt.figure(16)
plt.bar(day_2012, snow_gfk_2012, label = 'Snow Depth', color='cyan')
plt.plot(day_2012, temp_gfk_2012, label = 'Temperature', color='firebrick')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Snow Depth Grand Forks 2012')
plt.xlabel('Days from February 1')
plt.ylabel('Snow Depth (in), Temperature (F)')
# y-axis
plt.ylim([-5,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSsnow_gfk_2012.png')


fig17 = plt.figure(17)
# Plot each year's rate of change of river level over time
plt.plot(day_2009, river_rate_far_2009, label = 'River Rate', color='firebrick')
plt.plot(day_2009, temp_far_2009, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Fargo 2009')
plt.ylabel('River LevelChange (ft/day)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-15,55])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_far_2009.png')

fig18 = plt.figure(18)
# Plot each year's rate of change of river level over time
plt.plot(day_2010, river_rate_far_2010, label = 'River Rate', color='firebrick')
plt.plot(day_2010, temp_far_2010, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Fargo 2010')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-10,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_far_2010.png')

fig19 = plt.figure(19)
# Plot each year's rate of change of river level over time
plt.plot(day_2011, river_rate_far_2011, label = 'River Rate', color='firebrick')
plt.plot(day_2011, temp_far_2011, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Fargo 2011')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-10,60])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_far_2011.png')

fig20 = plt.figure(20)
# Plot each year's rate of change of river level over time
plt.plot(day_2012, river_rate_far_2012, label = 'River Rate', color='firebrick')
plt.plot(day_2012, temp_far_2012, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Fargo 2012')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-5,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_far_2012.png')

fig21 = plt.figure(21)
# Plot each year's rate of change of river level over time
plt.plot(day_2009, river_rate_gfk_2009, label = 'River Rate', color='firebrick')
plt.plot(day_2009, temp_gfk_2009, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Grand Forks 2009')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-15,55])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_gfk_2009.png')

fig22 = plt.figure(22)
# Plot each year's rate of change of river level over time
plt.plot(day_2010, river_rate_gfk_2010, label = 'River Rate', color='firebrick')
plt.plot(day_2010, temp_gfk_2010, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Grand Forks 2010')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-10,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_gfk_2010.png')

fig23 = plt.figure(23)
# Plot each year's rate of change of river level over time
plt.plot(day_2011, river_rate_gfk_2011, label = 'River Rate', color='firebrick')
plt.plot(day_2011, temp_gfk_2011, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Grand Forks 2011')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-10,60])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_gfk_2011.png')

fig24 = plt.figure(24)
# Plot each year's rate of change of river level over time
plt.plot(day_2012, river_rate_gfk_2012, label = 'River Rate', color='firebrick')
plt.plot(day_2012, temp_gfk_2012, label = 'Temperature', color='b')
# Plot Month vertical lines
plt.plot(x, y, 'g')
plt.plot(x2, y2, 'g')
plt.plot(x3, y3, label='Freezing Temperature', linestyle='--', color='c')
# Plot 0 line
plt.plot(x4, y4, color='k')
# Title and y-axis label
plt.title('Rate of Change of River Level Grand Forks 2012')
plt.ylabel('River Level Change (ft/day), Temperature (F)')
# y-axis from -1.5 to 5 feet/day
plt.ylim([-5,65])
# Small legend with two columns
plt.legend(loc='best')
plt.savefig('tempVSrate_gfk_2012.png')

