#!/usr/bin/env python3
#
# Name:
#   forward_traj_interp_class.py
#
# Purpose:  Create a Python object to work with vorticity budget data
#           interpolated to forward trajectory positions.
#
# File input/output: files containing vorticity budget data interpolated to
#                    forward trajectory locations, named
#             "cm1out_pdata_vort_interp_{model_version_number}_{parcel_label}.nc"
#
# Syntax: 
#   traj_data = Forward_traj_ds(model_version_number, path_to_data, parcel_label)
#
# Execution Example:
#   from forward_traj_interp_class import Forward_traj_ds
#   traj_data = Forward_traj_ds('v5', 'parcel_interpolation/', '1000parcel_tornadogenesis')
#
# Modification History:
#   2022/03/30 - Lance Wilson:  Created from back_traj_interp_class and
#                               categorize_traj_class.
#

from netCDF4 import Dataset
from netCDF4 import MFDataset
from os import path

import atexit
import numpy as np
import sys

class Forward_traj_ds:
    def __init__(self, version_number, interp_dir, parcel_label):
        # File names for this category of interpolated trajectory data.
        if version_number in parcel_label:
            file_name = 'cm1out_pdata_vort_interp_{:s}.nc'.format(parcel_label)
        else:
            file_name = 'cm1out_pdata_vort_interp_{:s}_{:s}.nc'.format(version_number, parcel_label)

        # Add the directory slash for concatenating with the filename if it is not
        #   already there.
        if not interp_dir.endswith('/'):
            interp_dir = interp_dir + '/'

        self.file_path = interp_dir + file_name

        # Check whether this dataset already exists.
        if path.isfile(self.file_path):
            self.existing_file = True
        else:
            self.existing_file = False

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Create a new netCDF file to store the data.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_new_nc(self, version_number, parcel_label, traj_num, xpos, ypos, zpos, parcel_out_times, file_num_offset):
        self.ds = Dataset(self.file_path, mode='w')
        # From https://stackoverflow.com/a/41627098
        # Close netCDF files when the program exits.
        atexit.register(self.closeNCfile, self.ds)

        # Create netCDF variable dimensions.
        parcel_dim = self.ds.createDimension('number_parcels', traj_num)
        time_dim = self.ds.createDimension('time', None)
        offset_dim = self.ds.createDimension('offset', 1)

        # Create variable containing the subset of x coordinate data used in the output.
        xpos_var = self.ds.createVariable('xpos', np.float32, ('time', 'number_parcels'))
        xpos_var.units = 'm'
        xpos_var.definition = 'X-Direction Parcel Positions'
        xpos_var[:,:] = xpos

        # Create variable containing the subset of y coordinate data used in the output.
        ypos_var = self.ds.createVariable('ypos', np.float32, ('time', 'number_parcels'))
        ypos_var.units = 'm'
        ypos_var.definition = 'Y-Direction Parcel Positions'
        ypos_var[:,:] = ypos

        # Create variable containing the subset of z coordinate data used in the output.
        zpos_var = self.ds.createVariable('zpos', np.float32, ('time', 'number_parcels'))
        zpos_var.units = 'm'
        zpos_var.definition = 'Z-Direction Parcel Positions'
        zpos_var[:,:] = zpos

        # Create variable to store file_num_offset.
        offset_var = self.ds.createVariable('file_num_offset', np.int, ('offset'))
        offset_var.definition = 'Number of model file at the earliest forward trajectory time'
        offset_var[:] = file_num_offset

        # Create variable to store time.
        time_var = self.ds.createVariable('time', np.float32, ('time'))
        time_var.units = 'seconds'
        time_var.definition = 'Time Since Beginning of Simulation'
        time_var[:] = parcel_out_times

        return

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Create variables to store interpolated vorticity budget data.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_vort_var(self, ds_in, var_name, vort_var_out):
        # Create netCDF variable to store the interpolated values for this variable.
        vort_var = self.ds.createVariable(var_name, np.float32, ('time', 'number_parcels'))
        vort_var.units = ds_in.variables[var_name].units
        vort_var.definition = ds_in.variables[var_name].definition
        vort_var[:,:] = vort_var_out

        return

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Open and read netCDF files containing vorticity budget data interpolated
    #   to back trajectory locations.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def read_data(self):
        if self.existing_file == True:
            self.ds = Dataset(self.file_path)
            # From https://stackoverflow.com/a/41627098
            # Close netCDF files when the program exits.
            atexit.register(self.closeNCfile, self.ds)

            # Total number of parcels for this set of data.
            self.total_parcel_num = self.ds.dimensions['number_parcels'].size

            # Model file at the earliest time of the trajectory dataset (should not
            #   need to add one to get the correct CM1 model file).
            self.file_num_offset = self.ds.variables['file_num_offset'][0]

            # Get the number of time steps in the full set of parcel data.
            self.parcel_time_step_num = self.ds.dimensions['time'].size

            # Array of model simulation times (in seconds) for the trajectory dataset.
            self.simulation_times = np.copy(self.ds.variables['time'])

            # List of vorticity budget variables, which are all variables in
            #   the file except those containing position data (which end in
            #   'pos') and those that have only one dimension (which should
            #   just be file_num_offset).
            self.budget_var_keys = [var_name for var_name in self.ds.variables.keys() if not var_name.endswith('pos') if len(self.ds.variables[var_name].dimensions) > 1]

            # Position data for the back trajectories.
            self.xpos = self.getBudgetData('xpos')
            self.ypos = self.getBudgetData('ypos')
            self.zpos = self.getBudgetData('zpos')
        else:
            print('Forward trajectory interpolated vorticity budget file does not exist.')
            sys.exit()

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Called at exit time to close the netCDF files.
    #   From https://stackoverflow.com/a/41627098
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def closeNCfile(self, ds):
        ds.close()

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Get Data for this vorticity budget variable.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def getBudgetData(self, budget_var_name):
        return np.copy(self.ds.variables[budget_var_name])

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Retrieve and combine horizontal and vertical components of vorticity
    #   budget variable data (if both components exist).
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def getCombinedBudgetData(self, combined_var_name):
        horiz_name = self.add_dir2var(combined_var_name, 'h')
        vert_name = self.add_dir2var(combined_var_name, 'v')

        if horiz_name in self.budget_var_keys and vert_name in self.budget_var_keys:
            budget_var = self.getBudgetData(horiz_name) + self.getBudgetData(vert_name)
        else:
            # For now, if there are not both horizontal and vertical
            #   components, or if a regular variable name was entered, return
            #   data for just that variable.
            budget_var = self.getBudgetData(combined_var_name)
        return budget_var

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Remove the horizontal (h) or vertical (v) part of the budget variable label
    #   so that the horizontal and vertical components of turbulence and diffusion
    #   get plotted together.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def remove_dirFromVar(self, var_name):
        var_name_split = var_name.split('_')
        new_name = var_name_split[0] + '_' + var_name_split[-1][1:]
        return new_name

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Add the horizontal or vertical (v) back into the budget variable label to
    #   access data.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def add_dir2var(self, base_name, mode):
        base_name_split = base_name.split('_')
        new_name = base_name_split[0] + '_' + mode + base_name_split[-1]
        return new_name

