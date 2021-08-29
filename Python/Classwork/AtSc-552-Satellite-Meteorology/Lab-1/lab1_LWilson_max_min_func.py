#!/usr/bin/env python3
#
# Name:
#   lab1_LWilson_max_min_func.py
#
# Purpose:
#   Function to calculate the maximum and minimum values in a 2D array.
#
# Syntax:
#   python lab1_LWilson_max_min_func.py
#
# Modification History:
#   2020/01/30 - Lance Wilson:  Created.

import numpy as np

def max_min_func(data):
    dimensions = data.shape

    # Check to prevent user from inputting an array that is not 2D.
    if len(dimensions) != 2:
        print('An array that was not two-dimensional was supplied.')
        print('This function is designed to work only with 2D arrays.')
        return

    # Starting minimum and maximum values that are hopefully outside the range
    #   of realistic data.
    min_value = 99999999.
    max_value = -1.

    for line in data:
        for value in line:
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value

    return (max_value, min_value)

