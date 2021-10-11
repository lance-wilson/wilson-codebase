#!/usr/bin/env python
#
# Name:
#   IntegerCount_LanceWilson.py
#
# Purpose:
#   To sum all integers from one to an integer input by the user.
#
# Syntax:
#   python IntegerCount_LanceWilson.py integer
#
#   Input: An Integer.
#
#   Output: Sum of integers 1 to n.
#
# Execution Example:
#   Linux example: python IntegerCount.py integer
#
# Modification History:
#   2017/08/23 - Lance Wilson:  Created.
#
# Verification of Data:
#   Sum of numbers 1 to 3 is 6 (3 + 2 + 1 = 6).
#
# Copyright 2017 Lance Wilson

import sys

def help_message():
    print 'Syntax: python IntegerCount_LanceWilson.py integer'

# Only run to program if there is the correct number of command line arguments.
if (len(sys.argv) != 2):
  help_message()
  exit()

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

# The target integer we are summing to.
targetInt = int(sys.argv[1])

# Calculate the sum of integers.
#   n(n+1)/2 formula has been defined as the sum of the sequence of
#   integers from 1 to n.
IntSum = targetInt * (targetInt+1)/2

print 'Sum of numbers from 1 to ' + str(targetInt) + ': ' + str(IntSum)
