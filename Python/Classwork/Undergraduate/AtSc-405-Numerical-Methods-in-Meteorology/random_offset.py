#!/usr/bin/env python
#
# Name:
#   random_offset.py
#
# Purpose:
#   The purpose of this program is to take in a data file containing the true
#       air speed, heading, beta angle, east and north ground velocity, and
#       east and north wind, and calculate the optimum heading offset angle by
#       measuring the standard deviation of the east and north wind components
#       for each of 1000 randomly selected offset angles and calculating which
#       angle minimizes the sum of those standard deviations.
#
# Syntax:
#   python random_offset.py winds_file
#
#   Input: Data concerning winds from an input file. Example: winds_offset.dat.
#
#   Output: The optimum value of the heading angle offset.
#
# Execution Example:
#   Linux example: python random_offset.py winds_offset.dat
#
# Modification History:
#   2017/10/01 - Lance Wilson:  Created.
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

def mean_avg(in_array):
    total = 0.0
    for value in in_array:
        total += value
    return float(total)/float(len(in_array))

def standard_deviation(in_array):
    # Formula for standard deviation: sqrt(sum((value - mean_value)^2)/(N+1))
    mean_value = mean_avg(in_array)
    numerator = 0.0
    for value in in_array:
        numerator += math.pow((value - mean_value), 2)
    return math.sqrt(numerator/(len(in_array)+1.0))

def minimum(in_array):
    min_value = in_array[0]
    min_index = 0
    for index in range(0,len(in_array)):
        if in_array[index] < min_value:
            min_value = in_array[index]
            min_index = index
    # Return a tuple of the minimum standard deviation calculated and the index
    #   of the array where that minimum occurs.
    return (min_value, min_index)

def help_message():
    print 'Syntax: python random_offset.py winds_file'
    print 'Example: python random_offset.py winds_offset.dat'

# Only run to program if there is the correct number of command line arguments.
if (len(sys.argv) != 2):
  help_message()
  exit()

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

with open(sys.argv[1], 'r') as infile:
    # Take in the header from the file.
    header_names = infile.readline().split()
    header_units = infile.readline().split()

    # Data gets loaded into a 2D array.
    data = np.loadtxt(infile)
    # Convert the columns in the data to individual arrays.
    true_air_speed = data[:,0]
    heading = data[:,1]
    beta = data[:,2]
    ground_x = data[:,3]
    ground_y = data[:,4]
##    wind_x = data[:,5]
##    wind_y = data[:,6]

# Random heading angle offsets are in degrees.
random_offsets = np.random.uniform(low=-1.0, high=1.0, size=1000)
standard_dev_sums = np.empty(len(random_offsets))

# Convert the heading and beta angles to radians.
random_offsets_radians = np.radians(random_offsets)
heading_radians = np.radians(heading)
beta_radians = np.radians(beta)

# Equations:
#      U = -1.0 * true_air_speed * sin((heading + offset) + beta) + ground_x
#      V = -1.0 * true_air_speed * cos((heading + offset) + beta) + ground_y
for x in range(0,len(random_offsets_radians)):
    east_wind = -1.0 * true_air_speed * np.sin((heading_radians + random_offsets_radians[x]) + beta_radians) + ground_x
    north_wind = -1.0 * true_air_speed * np.cos((heading_radians + random_offsets_radians[x]) + beta_radians) + ground_y
    standard_dev_sums[x] = standard_deviation(east_wind) + standard_deviation(north_wind)

# Optimized deviation is a tuple of both the minimum standard deviation and the
#   index where that value occurs.
optimized_deviation = minimum(standard_dev_sums)
optimized_offset = random_offsets[optimized_deviation[1]]

print 'The minimum sum of the standard deviations of the east/west and north/south winds is %0.5f m/s.' % optimized_deviation[0]
print 'The corresponding optimum heading angle offset is %2.4f degrees.' % optimized_offset
