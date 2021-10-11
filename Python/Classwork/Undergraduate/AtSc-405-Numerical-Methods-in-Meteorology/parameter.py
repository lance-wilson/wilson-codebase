#!/usr/bin/env python
#
# Name:
#   parameter.py
#
# Purpose:
#   The purpose of this program is determine the number concentration of cloud condensation nuclei (CCN) for a maximum supersaturation at an updraft speed of 1 m/s.
#
# Syntax:
#   python parameter.py
#
#   Input: Requires a directory of data labelled with the name of the month containing data of supersaturations and CCN number concentration.
#
#   Output: Two image files (parameterplota.png and parameterplotb.png) that show the power fitted function of the data for September 19 and October 19, 2017, of the CCN and superaturation data.
#
# Execution Example:
#   Linux example: python parameter.py
#
# Modification History:
#   2017/11/15 - Lance Wilson:  Created.
#   2017/11/18 - Lance Wilson:  Added graphs and linear regression fit, header.
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

def help_message():
    print 'Syntax/Example: python parameter.py'

# Check whether the user asked for the help message.
for param in sys.argv:
    if (param.startswith('-h') or param.startswith('--help')):
        help_message()
        exit()

def parameterize(month):
    filelist = sorted(os.listdir(('./' + month)))

    if not filelist:
        print 'No files were found for' + month
        exit()

    supersat = np.array([])
    ccn_conc = np.array([])
    # Supersaturation at an updraft speed of 1 m/s.
    #   Based on linear fit of data provided in class.
    target_supersat = 0.306

    for datafile in filelist:
        thisfile = open((month + '/' + datafile), 'r')

        # Read header lines.
        filename = thisfile.readline()
        filedate = thisfile.readline()
        filetime = thisfile.readline()
        thisfile.readline()
        variables = thisfile.readline()
        thisfile.readline()

        this_supersat, this_ccn_conc = np.loadtxt(thisfile, delimiter=',', usecols=(1,-3), unpack=True)

        supersat = np.append(supersat,this_supersat)
        ccn_conc = np.append(ccn_conc,this_ccn_conc)

    change_indices = np.where(supersat[:-1]!=supersat[1:])[0]
    supersat_avg = supersat[change_indices]

    # Average the 30 seconds of CCN data before each change in supersaturation.
    CCN_avg = np.array([np.mean(ccn_conc[i-29:i+1]) for i in change_indices])

    # Sort the data by the supersaturation.
    CCN02 = CCN_avg[np.where(supersat_avg==0.2)]
    ss02  = supersat_avg[np.where(supersat_avg==0.2)]
    CCN03 = CCN_avg[np.where(supersat_avg==0.3)]
    ss03  = supersat_avg[np.where(supersat_avg==0.3)]
    CCN06 = CCN_avg[np.where(supersat_avg==0.6)]
    ss06  = supersat_avg[np.where(supersat_avg==0.6)]
    CCN09 = CCN_avg[np.where(supersat_avg==0.9)]
    ss09  = supersat_avg[np.where(supersat_avg==0.9)]

    # Averages of the data at each supersaturation.
    supersat_avgs = np.array([0.2, 0.3, 0.6, 0.9])
    ccn_avgs = np.array([np.mean(CCN02), np.mean(CCN03), np.mean(CCN06), np.mean(CCN09)])

    # A linear regression fit of logarithmic data will give the coefficients
    #   for a power law fit. 
    log_supersat = np.log(supersat_avgs)
    log_ccn_avgs = np.log(ccn_avgs)

    # First order polynomial fit (y = kx + a) of the logarithm data.
    k, log_a = np.polyfit(log_supersat, log_ccn_avgs, 1)

    a = math.exp(log_a)

    print '\n' + month
    print 'a\tk'
    print '%4.2f\t%1.3f' % (a, k)

    final_ccn_conc = a*math.pow(target_supersat,k)
    print 'Concentration at %1.2f%% supersaturation: %4.2f cm^-3' % (target_supersat, final_ccn_conc)

    all_ss = np.concatenate((ss02,ss03,ss06,ss09))
    all_ccn = np.concatenate((CCN02,CCN03,CCN06,CCN09))

    # Create a smoother function of CCN = a*SS^k for the graph.
    fitted_ss = np.arange(0.05,0.95,0.01)
    fitted_ccn = a*np.power(fitted_ss,k)

    plt.clf()
    plt.scatter(supersat_avgs, ccn_avgs,color='red',s=100,label='Mean values')
    plt.scatter(all_ss,all_ccn,label='All data points')
    plt.plot(fitted_ss, fitted_ccn,label='Power fit: CCN = a*$SS^k$')

    plt.legend(loc='upper left')
    plt.ylim(ymin=0)
    plt.title('Power law relation between supersaturation\nand CCN for ' + month + ' $19^{th}$, 2017')
    plt.xlabel('Supersaturation (%)')
    plt.ylabel('CCN Concentration ($cm^{-3}$)')
    if (month == 'September'):
        plt.savefig('parameterplota.png', dpi=400)
    if (month == 'October'):
        plt.savefig('parameterplotb.png', dpi=400)

parameterize('September')
parameterize('October')
