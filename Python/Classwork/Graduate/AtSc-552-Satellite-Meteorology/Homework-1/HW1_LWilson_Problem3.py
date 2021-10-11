#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   HW1_LWilson_Problem3.py
#
# Purpose:
#   Plot the equivalent ground size of a pixel across a sensor's field of view
#   and the relative size of a pixel with respect to that at nadir over the
#   field of view of three remote sensors: Landsat MSS, AVHRR, and an aircraft
#   scanner.
#
# Syntax:
#   HW1_LWilson_Problem3.py
#
# Modification History:
#   2020/02/22 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

# Create a graph of equivalent ground size and relative pixel size across the
#   sensor's field of view.  ifov and fov must be in radians, altitude in
#   meters or kilometers, and part and sat_name as strings.  The abbreviation
#   for the units of altitude must be given.
def pixel_size_graphs(ifov, fov, altitude, part, sat_name, units='m'):
    if units == 'km':
        radius_earth = 6378.1 # kilometers
    else:
        radius_earth = 6.3781e6 # meters

    # Angle from nadir that the center of the ifov varies to get the total fov.
    max_center_ifov_deviation = fov - (ifov/2.)

    # Create an array of angles that the center of the ifov sweeps out.
    nadir_angles = np.arange(-1.*max_center_ifov_deviation, max_center_ifov_deviation+.000001, 0.000001)

    # In order to get the total distance from the satellite to the Earth, need
    #   the angle across from it in a triangle connecting the satellite, the
    #   point viewed on the Earth's surface, and the center of the Earth.  To
    #   get this angle, need the third angle (across from the distance from
    #   the center of the Earth to the satellite).  Subtracting this third
    #   angle from 180 degrees sometimes proudces angles greater than 180
    #   degrees, but this serves to make chi as close to zero as it can be,
    #   which is necessary to return the more realistic of the possible lengths
    #   for the total distance. 
    alpha = np.pi - np.arcsin(((altitude + radius_earth) * np.sin(nadir_angles))/radius_earth)

    # Use the two known angles to get the angle across from the unknown
    #   Earth-satellite distance.
    chi = np.pi - nadir_angles - alpha

    # From Equation 2.7b in Remote Sensing Digital Image Analysis 
    along_ground_sizes = ifov * (altitude + radius_earth - radius_earth*np.cos(chi))/np.cos(nadir_angles)

    # From Equation 2.7b in Remote Sensing Digital Image Analysis
    across_ground_sizes = along_ground_sizes/np.sin(np.pi/2. - nadir_angles - chi)

    # Calculate nadir ground size separately in case the correct angle is not
    #   in the nadir_angles array.
    nadir_size = ifov * altitude

    # Pixel sizes relative to that at nadir.
    across_relative_pixel_sizes = across_ground_sizes/nadir_size
    along_relative_pixel_sizes = along_ground_sizes/nadir_size

    # Plot the equivalent ground sizes in the across track direction.
    fig = plt.figure()
    fig.add_subplot(221)
    plt.plot(np.degrees(nadir_angles), across_ground_sizes)
    plt.title('Problem 1{:s}:  {:s}\nAcross Track Ground Sizes'.format(part.upper(), sat_name))
    plt.locator_params(axis='x', nbins=10)
    plt.locator_params(axis='y', nbins=10)
    plt.xlabel('Angle from Nadir (degrees)')
    plt.ylabel('Equivalent Ground\nSize of Pixel ({:s})'.format(units))

    # Plot the relative pixel sizes in the across track direction.
    fig.add_subplot(222)
    plt.plot(np.degrees(nadir_angles), across_relative_pixel_sizes)
    plt.title('Problem 1{:s}:  {:s}\nAcross Track Relative Pixel Sizes'.format(part.upper(), sat_name))
    plt.locator_params(axis='x', nbins=10)
    plt.locator_params(axis='y', nbins=10)
    plt.xlabel('Angle from Nadir (degrees)')
    plt.ylabel('Relative Size of Pixel')

    # Plot the equivalent ground sizes in the along track direction.
    fig.add_subplot(223)
    plt.plot(np.degrees(nadir_angles), along_ground_sizes)
    plt.title('Problem 1{:s}:  {:s}\nAlong Track Ground Sizes'.format(part.upper(), sat_name))
    plt.locator_params(axis='x', nbins=10)
    plt.locator_params(axis='y', nbins=10)
    plt.xlabel('Angle from Nadir (degrees)')
    plt.ylabel('Equivalent Ground\nSize of Pixel ({:s})'.format(units))

    # Plot the relative pixel sizes in the along track direction.
    fig.add_subplot(224)
    plt.plot(np.degrees(nadir_angles), along_relative_pixel_sizes)
    plt.title('Problem 1{:s}:  {:s}\nAlong Track Relative Pixel Sizes'.format(part.upper(), sat_name))
    plt.locator_params(axis='x', nbins=10)
    plt.locator_params(axis='y', nbins=10)
    plt.xlabel('Angle from Nadir (degrees)')
    plt.ylabel('Relative Size of Pixel')

    fig.tight_layout()

    plt.savefig('Homework1_chap1_1{:s}_quad.png'.format(part), dpi = 400)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# PART A:  LANDSAT MSS
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ifov = 0.086/1000.      # mrad converted to radians
fov = np.radians(11.56) # degrees to radians
altitude = 920000.      # meters
part = 'a'
sat_name = 'Landsat MSS'
pixel_size_graphs(ifov, fov, altitude, part, sat_name, units='m')

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# PART B:  NOAA AVHRR
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ifov = 1.3/1000.                    # mrad converted to radians
altitude = 833.                     # kilometers
fov = np.arctan((2500/2.)/altitude) # radians
part = 'b'
sat_name = 'NOAA AVHRR'
pixel_size_graphs(ifov, fov, altitude, part, sat_name, units='km')

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# PART C:  Aircraft Scanner
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ifov = 2.5/1000.        # mrad converted to radians
fov = np.radians(80)    # degrees to radians
altitude = 1000.        # meters
part = 'c'
sat_name = 'Aircraft Scanner'
pixel_size_graphs(ifov, fov, altitude, part, sat_name, units='m')

