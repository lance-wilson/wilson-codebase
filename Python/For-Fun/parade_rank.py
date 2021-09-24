#!/usr/bin/env python
#
# Author:  Lance Wilson
#
# Name: parade_rank.py
#
# Syntax: parade_rank.py file_name
#
# Example: parade_rank.py Fall_2019.txt
#
# Purpose:  Create a ranking of different homes in the Parade of Homes based on the price (in 1000's of dollars) and the size (in square feet).
#

import numpy as np
import sys

if len(sys.argv) < 2:
    print('Must include a file name.')
    exit()

file_name = sys.argv[1]

homes = np.genfromtxt(file_name)

dtype = [('house', float), ('score', float)]
values = [(homes[i,0], homes[i,1] * homes[i,2]) for i in range(len(homes))]

# Create a structured array
scored_homes = np.array(values, dtype=dtype)

##ranked_homes = np.transpose(np.sort(scored_homes, order='score'))
ranked_homes = np.sort(scored_homes, order='score')[::-1]

print('Home\tScore')
for home in ranked_homes:
    print('{:d}\t{:d}'.format(int(home[0]), int(home[1])))
