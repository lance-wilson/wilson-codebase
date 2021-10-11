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
#   python classify_combined_fn.py band1 [bandn]
#   (Anaconda): runfile('{Path_to_file}/classify_combined_fn.py', args='band1 [bandn]', wdir='{Path_to_file}')
#   Note that bands 13 and 14 must have a specified sensitivity (E.g. 13lo or 13hi)
#
# Modification History:
#   2020/05/02 - Lance Wilson:  Created.

from get_hdf4_data import read_hdf_file
from PIL import Image
import glob
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print('Syntax: python classify_combined_fn.py band1 [bandn]')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/classify_combined.py\', args=\'band1 [bandn]\', wdir=\'{Path_to_file}\')')
    print('Note that bands 13 and 14 must have a specified sensitivity')
    print('E.g. 13lo or 13hi')
    sys.exit()

if len(sys.argv) <= 1:
    help_message()

# Bands 1,2,3,4,7,31,32,19,26,(9,10,or11)
trained_file = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'
files_to_classify = ['MOD021KM.A2009092.1740.061.2017296165538.hdf', 'MOD021KM.A2011101.1810.061.2017322200720.hdf', 'MOD021KM.A2015185.1805.061.2017321050011.hdf', 'MOD021KM.A2019104.1740.061.2019105021701.hdf']
#files_to_classify = ['MOD021KM.A2011101.1810.061.2017322200720.hdf', 'MOD021KM.A2015185.1805.061.2017321050011.hdf', 'MOD021KM.A2019104.1740.061.2019105021701.hdf']
#files_to_classify = ['MOD021KM.A2009092.1740.061.2017296165538.hdf']
#training_sets = ['1', '2', '3', '4', '5', '6', '7']
#training_sets = ['1', '2', '5', '6', '7']
#training_sets = ['1', '2']
#training_sets = ['1']
training_sets = ['8', '9']
band_names = sys.argv[1:]
prefix = './'
#prefix = 'Extra_Output/'

def classify_combined_fn(trained_file, file_to_classify, training_set, band_names):

    data_label = file_to_classify.split('.')[1]
    
    # Colors:  cloud, floodwater, land, semiarid, snow, water.
    color_table = np.array([[127,127,127], [0,0,120], [0,255,0], [255,240,179], [250,250,250], [0,0,220]])
    
    # Get a list of files containing signatures.
    signature_files = glob.glob('Signature_Files/signatures_class{:s}_*.txt'.format(training_set))
    
    trained_bands, trained_band_names, trained_scales, trained_offsets, valid_range = read_hdf_file(trained_file)
    
    data_bands, data_band_names, data_scales, data_offsets, data_valid_range = read_hdf_file(file_to_classify)
    
    image_shape = data_bands[0].shape
    number_clusters = len(signature_files)
    
    band_masked = {}
    data = np.ma.empty(image_shape + (len(band_names),))
    
    # Loop for getting data to minimize redundant calculations.
    for i, band_name in enumerate(band_names):
        try:
            # Find the index where the band is located.
            trained_band_index = trained_band_names.index(band_name)
            data_band_index = data_band_names.index(band_name)
        except ValueError:
            print('Band {:s} was not found in file'.format(band_name))
            help_message()
        
        # Get data for this band.
        trained_band_counts = trained_bands[trained_band_index]
        data_band_counts = data_bands[data_band_index]
    
        # Apply reflectance/radiance scale and offset for this band.
        trained_band = trained_scales[trained_band_index] * (trained_band_counts - trained_offsets[trained_band_index])
        data_band = data_scales[data_band_index] * (data_band_counts - data_offsets[data_band_index])
        
        # Mask bad data.
        band_masked[band_name] = np.ma.masked_where(trained_band_counts > valid_range[1], trained_band)
        
        # Multiplying by 100 to match to scale of the means calculated later.
        data[:,:,i] = np.ma.masked_where(data_band_counts > data_valid_range[1], data_band) * 100.
    
    signature_values = {}
    probabilities = np.empty((number_clusters,) + image_shape)
    info_classes = []
    
    # Loop through each informational class.
    for m, filename in enumerate(signature_files):
        signature_indices = np.loadtxt(filename).astype(np.int)
        info_class = filename.split('.')[0].split('_')[-1]
        info_classes.append(info_class)
        signature_values[info_class] = {}
        # Data will be organized so that each row is one channel (makes
        #   calculating the mean and covariance matrix easier).
        signature_values[info_class]['data'] = np.ma.empty((len(band_names), len(signature_indices)))
        
        # Get reflectance/radiance values for each point in the image for this
        #   informational class.
        for i, pair in enumerate(signature_indices):
            band_subset = np.ma.empty(len(band_names))
            for j, band_name in enumerate(band_names):
                band_subset[j] = band_masked[band_name][pair[0], pair[1]]
            # Multiplying by 100 to avoid overflow errors in probability later.
            signature_values[info_class]['data'][:,i] = band_subset.T * 100.
            
        signature_values[info_class]['mean'] = np.ma.empty(len(band_names))
        # Get Mean values for each channel.
        for i in range(len(band_names)):
            signature_values[info_class]['mean'][i] = np.mean(signature_values[info_class]['data'][i])
       
        # Get the covariance matrix.
        signature_values[info_class]['cov_matrix'] = np.cov(signature_values[info_class]['data'])
    
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        exponent = -1. * len(band_names)/2.
        cov_det = np.linalg.det(signature_values[info_class]['cov_matrix'])
        cov_inverse = np.linalg.inv(signature_values[info_class]['cov_matrix'])
        perturb = data - signature_values[info_class]['mean']
        
        # Don't need to do transpose of perturb because shape (n,) will be
        #   interpreted as (1 x n).
        inner_part1 = np.tensordot(perturb, cov_inverse, axes=1)
        inner_part = -0.5 * np.sum(inner_part1 * perturb, axis=-1)
    
        # Formula for maximum likelihood method.
        probabilities[m] = (2.*np.pi)**exponent * cov_det**-0.5 * np.exp(inner_part)
    
    # Index of the maximum probability at each pixel in the image.
    cluster = np.argmax(probabilities, axis=0)
    
    rgbArray = np.ma.zeros(image_shape + (3,), 'uint8')
    
    # Make a list of handles that have colors roughly matching those used in the image array.
    handles = []
    for i in range(number_clusters):
        rgbArray[np.where(cluster == i)] = color_table[i]
    
        handles.append(mlines.Line2D([], [], color=color_table[i]/255., marker='.',  markersize=15))
    
    plot_title = 'Bands: '
    for band_name in band_names:
        plot_title = plot_title + band_name + ' '
    
    # One plot to get a legend and list the channels used.
    plt.imshow(rgbArray)
    # Make legend manually; handles refers to the line marker.
    plt.legend(handles=handles, labels=info_classes, handlelength=0.5, loc=(1.04,0.5), ncol=1)
    plt.title(plot_title)
    plt.savefig(prefix + 'data{:s}_set{:s}_{:d}bands_legend.png'.format(data_label, training_set, len(band_names)), dpi=800)
    
    # Image with exactly one value per pixel.
    img = Image.fromarray(rgbArray)
    img.save(prefix + 'data{:s}_set{:s}_{:d}bands_no_legend.png'.format(data_label, training_set, len(band_names)))
    

for file_to_classify in files_to_classify:
    for training_set in training_sets:
        print(file_to_classify, training_set)
        classify_combined_fn(trained_file, file_to_classify, training_set, band_names)
