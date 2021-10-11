#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_lab5_unsupervised.py
#
# Purpose:
#   Perform unsupervised classification of a set of MODIS data by assigning
#   pixels to classes based on which mean they are closest to.
#
# Syntax:
#   python LWilson_lab5_unsupervised.py number_clusters band1 [bandn]
#   (Anaconda): runfile('{Path_to_file}/LWilson_lab5_unsupervised.py', args='number_clusters band1 [bandn]', wdir='{Path_to_file}')
#
# Note: if this doesn't work, run in Anaconda.
#
# Modification History:
#   2020/04/17 - Lance Wilson:  Created.

from get_hdf4_data import read_hdf_file
from PIL import Image
import itertools
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print('Syntax: python LWilson_lab5_unsupervised.py number_clusters band1 [bandn]')
    print('Syntax (Anaconda): runfile(\'{Path_to_file}/LWilson_lab5_unsupervised.py\', args=\'number_clusters band1 [bandn]\', wdir=\'{Path_to_file}\')')
    print('Note that bands 13 and 14 must have a specified sensitivity')
    print('E.g. 13lo or 13hi')
    sys.exit()

if len(sys.argv) <= 2:
    help_message()

filename = 'MOD021KM.A2009092.1740.061.2017296165538.hdf'
number_clusters = int(sys.argv[1])
# Will likely use these bands: 2, 3, 7, 22, 32
band_names = sys.argv[2:]

all_bands, all_band_names, all_scales, all_offsets, valid_range = read_hdf_file(filename)

image_shape = all_bands[0].shape

pixel_values = np.empty((len(band_names),) + image_shape)
class_means = np.empty((len(band_names), number_clusters))

for (i, band_name) in enumerate(band_names):
    try:
        # Find the index where the band is located.
        band_index = all_band_names.index(band_name)
    except ValueError:
        print('Band {:s} was not found in file'.format(band_name))
        help_message()

    # Get data for this band.
    band_counts = all_bands[band_index]

    # Apply reflectance/radiance scale and offset for this band.
    band = all_scales[band_index] * (band_counts - all_offsets[band_index])

    # Mask bad data.
    pixel_values[i] = np.ma.masked_where(band_counts > valid_range[1], band)
    
    # Plot the first band as a before image.
    if i == 0:
        # Convert data to a 0 to 255 range.
        max_value = all_scales[band_index] * (valid_range[1] - all_offsets[band_index])
        min_value = all_scales[band_index] * (valid_range[0] - all_offsets[band_index])
        band_range = max_value - min_value
        band_brightness = band * 255./band_range
        # Mask bad data.
        band_masked = np.ma.masked_where(band_counts > valid_range[1], band_brightness)
        img = Image.fromarray(band_masked.astype('uint8'))
        img.save('LWilson_beforeImage.png')

    band_min = np.min(band)
    band_max = np.max(band)

    # Evenly distribute starting class means along brightness values.
    class_means[i] = np.linspace(band_min, band_max, number_clusters)
    
iterations = 0
max_difference = 10

while(max_difference > 0.01 and iterations < 100):
    distance = np.empty((number_clusters,) + image_shape)
    cluster = np.empty(image_shape)
    # For each cluster
    for m in range(number_clusters):
        squared_diffs = np.empty((len(band_names),) + image_shape)
        # For each band
        for k in range(len(band_names)):
            squared_diffs[k] = (pixel_values[k,:,:] - class_means[k,m])**2
        # Use euclidean distance formula to find the distance of the pixel from
        #   all class means.
        distance[m,:,:] = np.sqrt(np.sum(squared_diffs, axis=0))
    
    # Find index of the minimum value.
    cluster = np.argmin(distance, axis=0)
    
    old_class_means = np.copy(class_means)
    mean_difference = np.zeros(class_means.shape)
    max_values = np.empty(class_means.shape)
    min_values = np.empty(class_means.shape)
    # Loop through each cluster and each channel.
    for i,j in itertools.product(range(number_clusters), range(len(band_names))):
        cluster_values = pixel_values[j][np.where(cluster == i)]
        # If there is nothing in the cluster, keep the old mean for this
        #   iteration.
        if cluster_values.shape[0] == 0:
            class_means[j,i] = old_class_means[j,i]
        else:
            class_means[j,i] = np.mean(cluster_values)
            mean_difference[j,i] = np.abs(class_means[j,i] - old_class_means[j,i])
            max_values[j,i] = np.max(cluster_values)
            min_values[j,i] = np.min(cluster_values)
    
    max_difference = np.max(mean_difference)
    iterations += 1
    print(iterations, max_difference)

np.set_printoptions(suppress=True)
print('Maximum values:')
print('Clusters->')
print('Bands--v')
print(max_values)

print('Minimum values:')
print('Clusters->')
print('Bands--v')
print(min_values)

rgbArray = np.ma.zeros(image_shape + (3,), 'uint8')

# Assign evenly distributed colors.
rgbArray[:,:,0] = (255/number_clusters) * cluster
rgbArray[:,:,1] = np.abs(128 - (255/number_clusters) * cluster)
rgbArray[:,:,2] = 255 - (255/number_clusters) * cluster

# Make a list of handles that have colors roughly matching those used in the image array.
handles = []
for i in range(number_clusters):
    red = i/number_clusters
    green = np.abs(0.5 - i/number_clusters)
    blue = 1 - i/number_clusters
    handles.append(mlines.Line2D([], [], color=(red, green, blue), markersize=15, label='Blue line'))

label_list = [str(i) for i in range(number_clusters)]

plt.imshow(rgbArray)
# Make legend manually; handles refers to the line marker.
plt.legend(handles=handles, labels=label_list, handlelength=0.5, loc=(1.04,0.5), ncol=2)
plt.title('Unsupervised Classification')
plt.savefig('LWilson_afterImage_{:d}.png'.format(number_clusters), dpi=800)
