#!/usr/bin/env python3
#
# Name:
#   categorize_traj_class.py
#
# Purpose:  Python object to work with back trajectories that have been
#           selected to belong to a specific region of the storm.
#
# Syntax: 
#   traj_data = Cat_traj(version_number, data_dir, parcel_label, category)
#
# Execution Example:
#   from categorize_traj_class import Cat_traj
#   traj_data = Cat_traj('v5', 'parcel_interpolation/', 'v5_meso_tornadogenesis', 'forward_flank')
#   traj_data.open_file('forward_flank')
#
# Modification History:
#   2021/12/16 - Lance Wilson:  Created.
#   2022/01/27 - Lance Wilson:  Moved file setup to separate method so that
#                               the existence of a file can be checked without
#                               creating an empty one.
#

from netCDF4 import Dataset
from os import path

import atexit
import numpy as np

class Cat_traj:
    def __init__(self, version_number, data_dir, parcel_label, category):
        # File names for this category of back trajectory data.
        if version_number in parcel_label:
            back_traj_file_name = '{:s}_{:s}.nc'.format(parcel_label, category)
        else:
            back_traj_file_name = '{:s}_{:s}_{:s}.nc'.format(version_number, parcel_label, category)

        if not data_dir.endswith('/'):
            data_dir = data_dir + '/'

        self.back_traj_file_path = data_dir + back_traj_file_name

        # Check whether this dataset already exists.
        if path.isfile(self.back_traj_file_path):
            self.existing_file = True
        else:
            self.existing_file = False

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Open the netCDF file.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def open_file(self, category):
        # If this dataset already exists, open it for reading and writing.
        if self.existing_file == True:
            self.read_existing_nc() 
        # Otherwise, create a new file.
        else:
            self.create_new_nc(category)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Create a new netCDF file to store the data.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_new_nc(self, category):
        # Open the output netCDF file.
        self.ds = Dataset(self.back_traj_file_path, mode='w')
        # From https://stackoverflow.com/a/41627098
        # Close netCDF files when the program exits.
        atexit.register(self.closeNCfile, self.ds)

        # Modify the category label to look nice in the definition of the
        #   output variable.
        category_string = ''
        for cat_string in category.split('_'):
            category_string += cat_string.title() + ' '

        # Create netCDF variable dimensions.
        parcel_dim = self.ds.createDimension('number_parcels', None)
        spatial_dim = self.ds.createDimension('spatial', 3)

        # Create variable containing the subset of x coordinate data used in the output.
        self.init_pos_var = self.ds.createVariable('init_pos', np.float32, ('number_parcels', 'spatial'))
        self.init_pos_var.units = 'm'
        self.init_pos_var.definition = 'Initialization Positions of Back Trajectories in the {:s}Region'.format(category_string)
        #init_pos_var[:,:] = []

        # Create default (empty) intialization position array that can be
        #   appended to when writing new data.
        self.initial_pos = np.zeros((0,3))

        return

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Open and read netCDF files containing initialization locations of back
    #   trajectories in the supplied category.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def read_existing_nc(self):
        self.ds = Dataset(self.back_traj_file_path, mode='r+')
        # From https://stackoverflow.com/a/41627098
        # Close netCDF files when the program exits.
        atexit.register(self.closeNCfile, self.ds)

        self.init_pos_var = self.ds.variables['init_pos']

        self.initial_pos = np.copy(self.ds.variables['init_pos'][:])

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Add a new set of initial positions
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def write_data(self, new_initial_pos):
        # Combine the existing set of positions with the new values to be added.
        output_initial_pos = np.concatenate((self.initial_pos, new_initial_pos))
        # Only write the unique sets of coordinates to the file.
        unique_initial_pos = np.unique(output_initial_pos, axis=0)
        self.init_pos_var[:,:] = unique_initial_pos

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Function to convert the intialization positions to an array index of a
    #   back trajectory dataset. The x, y, and z positions are arguments to
    #   the function so that it can be used with any of the back trajectory
    #   datasets (i.e. either the whole dataset or the one that retains only
    #   the usable trajectories).
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def meters_to_trajnum(self, xpos, ypos, zpos):
        traj_num = np.zeros(self.initial_pos[:,0].shape, dtype=np.int)

        for i, coord_meters in enumerate(self.initial_pos):
            x_indices = np.argwhere(xpos[0] == coord_meters[2])
            y_indices = np.argwhere(ypos[0] == coord_meters[1])
            z_indices = np.argwhere(zpos[0] == coord_meters[0])

            # Get indices that are to be plotted from the intersection of the x
            #   and y parts, and then the intersection of that and the z part.
            part1 = np.intersect1d(x_indices, y_indices)
            traj_num[i] = np.intersect1d(part1, z_indices)[0]

        return traj_num

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Called at exit time to close the netCDF files.
    #   From https://stackoverflow.com/a/41627098
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def closeNCfile(self, ds):
        ds.close()

