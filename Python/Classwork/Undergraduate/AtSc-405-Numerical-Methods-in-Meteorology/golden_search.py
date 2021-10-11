#!/usr/bin/env python
#
# Name:
#   golden_search.py
#
# Purpose:
#   The purpose of this program is to take in a data file containing the true
#       air speed, heading, beta angle, east and north ground velocity, and
#       east and north wind, and calculate the optimum heading offset angle by
#       measuring the standard deviation of the east and north wind components
#       for offset angles selected using the golden search method and
#       calculating which angle minimizes the sum of those standard deviations.
#
# Syntax:
#   python golden_search.py winds_file
#
#   Input: Data concerning winds from an input file. Example: winds2a.dat.
#
#   Output: The optimum value of the heading angle offset.
#
# Execution Example:
#   Linux example: python golden_search.py winds2a.dat
#
# Modification History:
#   2017/10/08 - Lance Wilson:  Created.
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

# Equations:
#      U = -1.0 * true_air_speed * sin((heading + offset) + beta) + ground_x
#      V = -1.0 * true_air_speed * cos((heading + offset) + beta) + ground_y
def wind_dev(heading_offset):
    east_wind = -1.0 * true_air_speed * np.sin((heading_radians + heading_offset) + beta_radians) + ground_x
    north_wind = -1.0 * true_air_speed * np.cos((heading_radians + heading_offset) + beta_radians) + ground_y
    standard_dev_sum = standard_deviation(east_wind) + standard_deviation(north_wind)
    return standard_dev_sum

def help_message():
    print 'Syntax: python golden_search.py winds_file'
    print 'Example: python golden_search.py winds2a.dat'

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

# Convert the heading and beta angles to radians.
heading_radians = np.radians(heading)
beta_radians = np.radians(beta)

# Set the boundaries of the initial search.
lower_bound = math.radians(-1.5)
upper_bound = math.radians(1.5)
d_interior = (upper_bound - lower_bound) * (math.sqrt(5.0) - 1.0)/2.0
# Set the "golden" intermediary points.
x1 = lower_bound + d_interior
x2 = upper_bound - d_interior
iterations = 0

while ((upper_bound - lower_bound) > 0.0001):
##while ((math.degrees(upper_bound) - math.degrees(lower_bound)) > 0.0001):
    standard_dev_sum1 = wind_dev(x1)
    standard_dev_sum2 = wind_dev(x2)

    if (standard_dev_sum1 < standard_dev_sum2):
        lower_bound = x2
        x2 = x1
        d_interior = (upper_bound - lower_bound) * (math.sqrt(5.0) - 1.0)/2.0
        x1 = lower_bound + d_interior
        standard_dev_sum2 = standard_dev_sum1
        standard_dev_sum1 = wind_dev(x1)
    else:
        upper_bound = x1
        x1 = x2
        d_interior = (upper_bound - lower_bound) * (math.sqrt(5.0) - 1.0)/2.0
        x2 = upper_bound - d_interior
        standard_dev_sum1 = standard_dev_sum2
        standard_dev_sum2 = wind_dev(x2)
    iterations += 1

optimized_offset_high = math.degrees(upper_bound)
optimized_offset_low = math.degrees(lower_bound)
optimized_offset_avg = math.degrees(mean_avg(np.array([upper_bound, lower_bound])))

print 'The optimum heading angle offset upper bound is %2.8f degrees.' % optimized_offset_high
print 'The optimum heading angle offset lower bound is %2.8f degrees.' % optimized_offset_low
print 'The optimum heading angle offset average is %2.8f degrees.' % optimized_offset_avg
print 'The number of iterations was %d.' % iterations
