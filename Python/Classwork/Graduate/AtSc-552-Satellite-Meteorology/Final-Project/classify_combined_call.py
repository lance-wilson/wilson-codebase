#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   classify_combined_fn.py
#
# Purpose:
#   Get the radiance and reflectance mean and covariance matrix for the
#   training regions and classify pixels.
#
# Syntax:
#   python classify_combined_call.py file_to_classify1[,file_to_classifyN] training_set1[,traing_setN] band1,[bandn]
#   (Anaconda): runfile('{Path_to_file}/classify_combined.py', args='file_to_classify1[,file_to_classifyN] training_set1[,traing_setN] band1,[bandn]', wdir='{Path_to_file}')
#   Note that bands 13 and 14 must have a specified sensitivity (E.g. 13lo or 13hi)
#
# Example:
#   python classify_combined_call.py MOD021KM.A2009092.1740.061.2017296165538.hdf,MOD021KM.A2011101.1810.061.2017322200720.hdf,MOD021KM.A2015185.1805.061.2017321050011.hdf,MOD021KM.A2019104.1740.061.2019105021701.hdf 1,2,5,6,7 1,2,3,4,7,31,32
#
# Modification History:
#   2020/05/14 - Lance Wilson:  Created.

from classify_combined_fn import classify_combined_fn
#from get_hdf4_data import read_hdf_file
#from PIL import Image
#import glob
#import matplotlib.lines as mlines
#import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print('Syntax: python classify_combined_fn.py file_to_classify1[,file_to_classifyN] training_set1[,training_setN] band1,[bandn]')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/classify_combined.py\', args=\'file_to_classify1[,file_to_classifyN] training_set1[,traing_setN] band1,[bandn]\', wdir=\'{Path_to_file}\')')
    print('Example: python classify_combined_call.py MOD021KM.A2009092.1740.061.2017296165538.hdf,MOD021KM.A2011101.1810.061.2017322200720.hdf,MOD021KM.A2015185.1805.061.2017321050011.hdf,MOD021KM.A2019104.1740.061.2019105021701.hdf 1,2,5,6,7 1,2,3,4,7,31,32
    print('Note that bands 13 and 14 must have a specified sensitivity')
    print('E.g. 13lo or 13hi')
    sys.exit()

if len(sys.argv) <= 1:
    help_message()

# Bands 1,2,3,4,7,31,32,19,26,(9,10,or11)
trained_file = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'

files_to_classify = sys.argv[1].split(',')
training_sets = sys.argv[2].split(',')
band_names = sys.argv[3].split(',')

for file_to_classify in files_to_classify:
    for training_set in training_sets:
        print(file_to_classify, training_set)
        classify_combined_fn(trained_file, file_to_classify, training_set, band_names)
