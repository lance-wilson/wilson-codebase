# Reads in latitude, longitude, surface temperatures, and upper level temperatures,
#     and creates a contour plot of the data.  Surface temperatures are in a filled
#     contour, while upper level temperatures are superimposed over that plot. The
#     plot figure is saved to a file.
# 
# Input: Files for latitidue, longitude, surface temperature, and upper level temperature,
#        called "lat.txt", "lon.txt", "sfc.txt", and "aloft.txt"
#
# Output: A plot with file name "contour_temp_LWilson.png"
#
# Syntax: python contour_LWilson.py
#
# Written: Lance Wilson, March 2016

import matplotlib.pyplot as plt


# Read in latitiude data
fid1 = open('lat.txt', 'r') # Open the lat.txt file
lats = fid1.read()  # Read in the data into a string
fid1.close()    # Close the lat.txt file
lats_list = lats.split()    # Split the lats string on spaces
latf_list = []      # Create an empty list
# Loop through lats_list, convert from string to float, and
# append to latf_list.
for num in lats_list:
    latf_list.append(float(num))

# Read in longitude data.
fid2 = open('lon.txt', 'r') # Open the lat.txt file
lons = fid2.read()  # Read in the data into a string
fid2.close()    # Close the lat.txt file
lons_list = lons.split()    # Split the lats string on spaces
lonf_list = []      # Create an empty list
# Loop through lats_list, convert from string to float, and
# append to latf_list.
for num in lons_list:
    lonf_list.append(float(num))

# Read in surface temperature data
sfc_temps = []
# Open file in read mode and save as an object
with open('sfc.txt', 'r') as openfileobject:
    # Loop through all the lines in the file object
    for line in openfileobject:
        # Split the line on spaces and save to sfc_temps list
        sfc_temps.append(line.split())

# Read in upper level temperature data
aloft_temps = []
# Open file and save as object
with open('aloft.txt', 'r') as openfileobject:
    for line in openfileobject:
        aloft_temps.append(line.split())


# Create new figure.
fig1 = plt.figure()
# Plot a contour of surface temperatures
c1 = plt.contourf(lons_list, lats_list, sfc_temps)
plt.title('Contour of Surface and Upper Level Temperatures')
plt.xlabel(r'Longitude [$\degree$ East]')
plt.ylabel(r'Latitude [$\degree$ North]')

# Add colorbar
cbar = plt.colorbar(c1)
# Label colorbar
cbar.set_label('Surface Temperature [$\degree$C]')

# Add acontour plot of upper-level temperatures
c2 = plt.contour(lons_list, lats_list, aloft_temps, colors='black')
# Label contour plot
c21 = plt.clabel(c2, inline = 0, fmt = '%5.1f')

# Modify plot axis limits
plt.xlim([min(lonf_list), max(lonf_list)])
plt.ylim([min(latf_list), max(latf_list)])

# Save figure to file
fig1.savefig('contour_temps_LWilson.png', dpi=400)

# End of program
