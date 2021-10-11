#!/usr/bin/env python3
#
# Name:
#   LWilson_lab4_mean_func.py
#
# Purpose:
#   Function to calculate the standard variance values in a 2D array.
#
# Syntax:
#   from LWilson_lab4_variance import variance_func
#   variance_func(array)
#
# Modification History:
#   2020/03/28 - Lance Wilson:  Created.

import numpy as np

def variance_func(data, mean_value):
    dimensions = data.shape

    # Check to prevent user from inputting an array that is not 2D.
    if len(dimensions) != 2:
        print('An array that was not two-dimensional was supplied.')
        print('This function is designed to work only with 2D arrays.')
        return

    sum_squares = 0.
    number_values = 0.
    for (i, row) in enumerate(data):
        for (j, value) in enumerate(row):
            # Separate behavior for whether the array is masked.
            if np.ma.is_masked(data):
                if not data.mask[i,j]:
                    sum_squares += (value - mean_value)**2
                    number_values += 1
            else:
                sum_squares += (value - mean_value)**2
                number_values += 1
    if number_values <= 1:
        print('Not enough valid values to calculate variance.')
        return
    variance = sum_squares/(number_values-1)

    return variance
