#!/usr/bin/env python
#
# Name:
#   histogram.py
#
# Purpose:
#   To plot a histogram of the number and volume of liquid water drops.
#
# Syntax:
#   python histogram.py datafile.txt graph_name
#
#   Input: Name of file containing the diameter, number, and volume of water
#          droplets/washers; name of the image file; type of file.
#          Type 1 File:  Data in raw values.
#          Type 2 File:  Data per unit diameter, with the diameter given as
#                        the midpoint of the bin.
#
#   Output: Image file containing the histogram (graph_name). 
#
# Execution Example:
#   Linux example: python histogram.py Washers.txt WasherGraph.png 2
#
# Modification History:
#   2017/08/31 - Lance Wilson:  Created, from histogram.py, AtSc 270.   
#
# Copyright 2017 Lance Wilson

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print 'Syntax: python histogram.py datafile.txt graph_name file_type'
    print 'File should contain the diameter, number, and volume of water'
    print 'droplets in three columns separated by spaces.'

# Only run to program if there is the correct number of command line arguments.
if (len(sys.argv) != 4):
  help_message()
  exit()

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

graph_name = sys.argv[2]
file_type = float(sys.argv[3])

drop_data = []
# Read in data from the input file.
with open(sys.argv[1], 'r') as infile:
    for line in infile:
        drop_data.append(line)

diameter_list = []
number_list = []
volume_list = []
for value in drop_data:
    drop_list = value.split()
    diameter_list.append(float(drop_list[0]))
    number_list.append(float(drop_list[1]))
    volume_list.append(float(drop_list[2]))

diameters = np.array(diameter_list)
number = np.array(number_list)
volume = np.array(volume_list)

if (file_type == 1):
    diameters_center = diameters - 0.4
    # Plot histogram
    ##b1 = plt.bar(diameters_center, number, width=0.8)
    b1 = plt.bar(diameters_center, volume, width=0.8)

    ##plt.title('Frequency of Washers by Diameter')
    plt.title('Variation in Volume of Representative Drops by Diameter')
    plt.xlabel('Diameter (mm)')
    ##plt.ylabel('Frequency')
    plt.ylabel('Volume (mm^3)')

    # Save plot
    plt.savefig(graph_name, dpi=400)

if (file_type == 2):
    diameters_center = diameters - 4.45
    # Plot histogram
    ##b1 = plt.bar(diameters_center, number, width=8.9)
    b1 = plt.bar(diameters_center, volume, width=8.9)

    ##plt.title('Frequency of Washers per unit Diameter')
    plt.title('Variation in Volume of Representative Drops per unit Diameter')
    plt.xlabel('Diameter (mm)')
    ##plt.ylabel('Number/Diamter (mm^-1)')
    plt.ylabel('Volume/Diameter (mm^3/mm)')
    plt.xticks(range(5,51,9))

    # Save plot
    plt.savefig(graph_name, dpi=400)

if (file_type == 3):
    diameters_center = diameters - 4.95
    # Plot histogram
    b1 = plt.bar(diameters_center, number, width=9.9)
    ##b1 = plt.bar(diameters_center, volume, width=9.9)

    plt.title('Frequency of Washers per unit Diameter')
    ##plt.title('Variation in Volume of Representative Drops per unit Diameter')
    plt.xlabel('Diameter (mm)')
    plt.ylabel('Number/Diamter (mm^-1)')
    ##plt.ylabel('Volume/Diameter (mm^3/mm)')
    plt.xticks(range(0,51,10))

    # Save plot
    plt.savefig(graph_name, dpi=400)

# End of program
