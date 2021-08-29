#!/usr/bin/env python3
#
# Name:
#   LWilson_lab4_mean_func.py
#
# Purpose:
#   Function to calculate the mean values in a 2D array.
#
# Syntax:
#   from LWilson_lab4_mean_func import mean_func
#   mean_func(array)
#
# Modification History:
#   2020/03/28 - Lance Wilson:  Created.

import numpy as np

def mean_func(data):
    dimensions = data.shape

    # Check to prevent user from inputting an array that is not 2D.
    if len(dimensions) != 2:
        print('An array that was not two-dimensional was supplied.')
        print('This function is designed to work only with 2D arrays.')
        return

    data_sum = 0.
    number_values = 0.
    for (i, row) in enumerate(data):
        for (j, value) in enumerate(row):
            # Separate behavior for whether the array is masked.
            if np.ma.is_masked(data):
                if not data.mask[i,j]:
                    data_sum += value
                    number_values += 1
            else:
                data_sum += value
                number_values += 1
    mean = data_sum/number_values

    return mean
