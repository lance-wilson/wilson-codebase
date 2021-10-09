#!/usr/bin/env python
#
# Name:
#   plot_correlation.py
#
# Purpose:
#   The purpose of this function is to calculate the number of days in each
#   year in which there are named storms, hurricanes, and intense hurricanes,
#   to produce correlation plots with West African Rainfall in INTRAMWARE.
#
# Syntax:
#   Call function: from plot_correlation import plot_correlation
#
#   Input:  See argument list below.
#
#   Output: Scatter plot of the graph with a best-fit linear regression.
#
# Modification History:
#   Date         Editor         Version Modifications
#   2017/12/05 - Lance Wilson:  0.1     Created with INTRAMWARE.
#   2017/12/08 - Lance Wilson:  0.1.1   Added importation of data.
#   2017/12/11 - Lance Wilson:  0.2     Completed importation of data.
#   2017/12/15 - Lance Wilson:  1.0     Added averages, standard deviations,
#                                       and the regional rainfall index
#   2017/12/16 - Lance Wilson:  1.1     Added El Nino, AMO, and HURDAT data,
#                                       added data output.
#   2017/12/17 - Lance Wilson:  1.2     Added graphing of results and
#                                       correlations in data output, comments.
#   2017/12/19 - Lance Wilson:  1.2     Added comments, updated the percentile
#                                       list calculations.
#   2018/03/17 - Lance Wilson:  1.2     Added a special dot for 2017 season,
#                                       removed best-fit lines for quartiles,
#                                       migrated to separate file.
#
# Copyright 2017 Lance Wilson
#
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Function for plotting the various correlations, with the following arguments:
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Required:
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Arg 1, 2 (regional_index, comparison): the two variables to be compared.
#   Arg 3, 4 (period1, period2): the values in each year to be compared.
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Optional:
#   (The listed defaults are generally intended to illuminate incorrect usage.)
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Arg 5 (common_years): in version 1.2, the array of years that are common
#       to the variables being compared (to prevent the linear regression from
#       throwing an error due to unequal list sizes) (Future versions may move
#       this to the function). Default is a list of length 1: ['9999'].
#   Arg 6 (title_info): the title to be printed on the graph. Default 'Unknown'
#   Arg 7 (x_info): the info to be put on the x-axis label. Default 'Unknown'
#   Arg 8 (y_info): the info to be put on the y-axis label. Default 'Unknown'
#   Arg 9 (filename): the file name for the saved image. Default 'Unknown.png'
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Returns: the correlation coefficient of the two sets of data and whether
#            this value is greater than 0.9.
#   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   The correlation coefficient r and whether this value is greater than 0.9.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

import math
import matplotlib.pyplot as plt
import numpy as np
##import os
##import re
from scipy import stats
##import sys

def plot_correlation(regional_index, comparison, period1, period2,
            common_years=['9999'], title_info='Unknown', x_info='Unknown',
            y_info='Unknown', filename='Unknown.png'):
    # For graphing purposes, remove the values containing missing value codes.
    for year in sorted(common_years):
        if (period2 in comparison[year].keys() and
               (regional_index[year][period1] == 99.9 or
                comparison[year][period2] == 99.9)):
            common_years.remove(year)

    # The following construct ([value for year in common]) loops through each
    #   list in common_years and uses that value to produce a new list.
    rainfall_index = [float(regional_index[year][period1])
                                            for year in common_years]
    comparison_index = [float(comparison[year][period2])
                                            for year in common_years]

    if '2017' in common_years:
        rainfall_2017 = regional_index['2017'][period1]
        comparison_2017 = comparison['2017'][period2]

    #^^^ Calculate Stats for full data ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    m, b, r_value, p_value, std_err = stats.linregress(
                                        rainfall_index, comparison_index)
    # Create a smoother set of x_values for plotting the best-fit line.
    x_values = np.arange(min(rainfall_index)-1., max(rainfall_index)+1., 0.01)
    y_values = m * x_values + b

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    #^^^ Calculate Stats for lower quartile ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Create a set of lists to look at the correlations of the lowest
    #   quartile of the comparison value.
    lower_compare = np.percentile(comparison_index, 25)
    lower_quart_rainfall = []
    lower_quart_compare = []

    compare_index = 0
    try:
        # To make sure that all of the highest values are found, only look for
        #   values that are less than the 25 percentile mark (if one fourth of
        #   the values are, this will finish).
        while len(lower_quart_compare) < (len(comparison_index)/4):
            if (comparison_index[compare_index] < lower_compare):
                lower_quart_rainfall.append(rainfall_index[compare_index])
                lower_quart_compare.append(comparison_index[compare_index])
            compare_index += 1
    except IndexError:
        # If some of the values are equal to the 25 percentile mark, this will
        #   fill up the remainder of the lower fourth lists.
        compare_index = 0
        while len(lower_quart_compare) < (len(comparison_index)/4):
            if (comparison_index[compare_index] <= lower_compare):
                lower_quart_rainfall.append(rainfall_index[compare_index])
                lower_quart_compare.append(comparison_index[compare_index])
            compare_index += 1

    ##m_low, b_low, r_value_low, p_value_low, std_err_low = stats.linregress(
    ##                                lower_quart_rainfall, lower_quart_compare)
    ##x_values_low = np.arange(min(lower_quart_rainfall)-1.,
    ##                         max(lower_quart_rainfall)+1., 0.01)
    ##y_values_low = m_low * x_values_low + b_low

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    #^^^ Calculate Stats for upper quartile ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Create a set of lists to look at the correlations of the upper
    #   quartile of the comparison value.
    ##upper_rainfall = np.percentile(rainfall_index, 75)
    upper_compare = np.percentile(comparison_index, 75)
    upper_quart_rainfall = []
    upper_quart_compare = []

    compare_index = 0
    try:
        # To make sure that all of the highest values are found, only look for
        #   values that are less than the 25 percentile mark (if one fourth of
        #   the values are, this will finish).
        while len(upper_quart_compare) < (len(comparison_index)/4):
            if (comparison_index[compare_index] > upper_compare):
                upper_quart_rainfall.append(rainfall_index[compare_index])
                upper_quart_compare.append(comparison_index[compare_index])
            compare_index += 1
    except IndexError:
        # If some of the values are equal to the 25 percentile mark, this will
        #   fill up the remainder of the lower fourth lists.
        compare_index = 0
        while len(upper_quart_compare) < (len(comparison_index)/4):
            if (comparison_index[compare_index] >= upper_compare):
                upper_quart_rainfall.append(rainfall_index[compare_index])
                upper_quart_compare.append(comparison_index[compare_index])
            compare_index += 1

    ##m_upper, b_upper, r_value_upper, p_value_upper, std_err_upper = (
    ##            stats.linregress(upper_quart_rainfall, upper_quart_compare))
    ##x_values_upper = np.arange(min(upper_quart_rainfall)-1.,
    ##                           max(upper_quart_rainfall)+1., 0.01)
    ##y_values_upper = m_upper * x_values_upper + b_upper

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    #^^^ Make Graphs ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    plt.scatter(rainfall_index, comparison_index, label='25-75 percentile')
    plt.scatter(upper_quart_rainfall, upper_quart_compare, color='red',
                label='75-100 percentile')
    plt.scatter(lower_quart_rainfall, lower_quart_compare, color='green',
                label='0-25 percentile')
    if '2017' in common_years:
        plt.scatter(rainfall_2017, comparison_2017, color='black', label='2017')
        filename = filename.replace('.', '_2017.', 1)
    ##plt.plot(x_values, y_values, label=('Total $r^{2}$ = %.2f' %
    ##                                    math.pow(r_value,2)))
    ##plt.plot(x_values_low, y_values_low, label=('Lower $r^{2}$ = %.2f' %
    ##                                            math.pow(r_value_low,2)))
    ##plt.plot(x_values_upper, y_values_upper, label=('Upper $r^{2}$ = %.2f' %
    ##                                                math.pow(r_value_upper,2)))
    plt.plot(x_values, y_values, label=('Total r = %.2f' % r_value))
    ##plt.plot(x_values_low, y_values_low, label=('Lower r = %.2f' % r_value_low))
    ##plt.plot(x_values_upper, y_values_upper, label=('Upper r = %.2f' %
    ##                                                r_value_upper))
    plt.title('Relationship of\n' + title_info)
    plt.xlabel(x_info)
    plt.ylabel(y_info)
    min_x = min(rainfall_index) - 0.25 * (max(rainfall_index) -
                                          min(rainfall_index))
    max_x = max(rainfall_index) + 0.25 * (max(rainfall_index) -
                                          min(rainfall_index))
    min_y = min(comparison_index) - 0.25 * (max(comparison_index) -
                                            min(comparison_index))
    max_y = max(comparison_index) + 0.25 * (max(comparison_index) -
                                            min(comparison_index))
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    ##if (r_value > 0):
    plt.legend(loc='upper left', scatterpoints=1)
    ##plt.legend(loc='upper left', scatterpoints=1, fontsize='medium')
    ##else:
    ##    plt.legend(loc='lower left', scatterpoints=1)
    plt.tight_layout()
    plt.savefig(filename, dpi=400)
    plt.close()

    correlation = 'U'
    if (r_value >= 0.90):
        correlation = 'Y'
    else:
        correlation = 'N'

    return r_value, correlation
