#!/usr/bin/env python3
#
# Name:
#   back_traj_interp_class.py
#
# Purpose:  Create a Python object to work with vorticity budget data
#           interpolated to back trajectory positions.
#
# Syntax: 
#   traj_data = Back_traj_ds(model_version_number, path_to_data, parcel_label)
#
# Execution Example:
#   from back_traj_interp_class import Back_traj_ds
#   traj_data = Back_traj_ds('v5', 'parcel_interpolation/', 'v5_meso_tornadogenesis')
#
# Modification History:
#   2021/11/19 - Lance Wilson:  Created.
#

from netCDF4 import Dataset
from netCDF4 import MFDataset
from os import path

import atexit
import numpy as np
import sys

class Back_traj_ds:
    def __init__(self, version_number, interp_dir, parcel_label):

        self.read_data(version_number, interp_dir, parcel_label)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Open and read netCDF files containing vorticity budget data interpolated
    #   to back trajectory locations.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def read_data(self, version_number, interp_dir, parcel_label):
        # File names for the vorticity budget data interpolated to trajectory locations.
        if version_number in parcel_label:
            back_traj_vort_name_full = '{:s}_fully_valid_back_trajectory.nc'.format(parcel_label)
            back_traj_vort_name_partial = '{:s}_partially_valid_back_trajectory.nc'.format(parcel_label)
        else:
            back_traj_vort_name_full = '{:s}_{:s}_fully_valid_back_trajectory.nc'.format(version_number, parcel_label)
            back_traj_vort_name_partial = '{:s}_{:s}_partially_valid_back_trajectory.nc'.format(version_number, parcel_label)


        # Attempt to open the file containing fully valid trajectory data.
        if path.isfile(interp_dir + back_traj_vort_name_full):
            self.ds_full = Dataset(interp_dir + back_traj_vort_name_full)
            self.full_flag = True
            # From https://stackoverflow.com/a/41627098
            # Close netCDF files when the program exits.
            atexit.register(self.closeNCfile, self.ds_full)
        else:
            self.full_flag = False

        # Attempt to open the file containing trajectory data valid back to a certain time.    
        if path.isfile(interp_dir + back_traj_vort_name_partial):
            self.ds_partial = Dataset(interp_dir + back_traj_vort_name_partial)
            self.partial_flag = True
            # From https://stackoverflow.com/a/41627098
            # Close netCDF files when the program exits.
            atexit.register(self.closeNCfile, self.ds_partial)
        else:
            self.partial_flag = False

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If neither dataset exists.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if self.full_flag == False and self.partial_flag == False:
            print('No back trajectories were found for this dataset.')    
            sys.exit()

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If both the fully valid and partially valid datasets were opened successfully.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if self.full_flag == True and self.partial_flag == True:
            # Get the number of parcels in the fully valid dataset.
            fully_valid_parcel_num = self.ds_full.dimensions['number_parcels'].size
            # Get the number of time steps in the full set of parcel data.
            self.parcel_time_step_num = self.ds_full.dimensions['time'].size

            # Get the number of parcels in the partially valid dataset.
            partially_valid_parcel_num = self.ds_partial.dimensions['number_parcels'].size
            # Get the number of time steps in the partially valid set of
            #   parcel of data.
            partial_parcel_time_step_num = self.ds_partial.dimensions['time'].size

            # Difference in the number of time steps between the fully valid and
            #   partially valid datasets.
            time_length_diff = self.parcel_time_step_num - partial_parcel_time_step_num
            # To keep the array sizes of the fully valid and partially valid
            #   datasets the same (to allow them to be concatenated), a buffer
            #   of nan's is to be added to the end of the partial dataset (this
            #   will not affect plotting, as matplotlib will not plot the nan's).
            self.nan_buffer = np.array([np.nan] * time_length_diff * partially_valid_parcel_num).reshape(time_length_diff, partially_valid_parcel_num)

            # Total number of parcels for the full set of data.
            self.total_parcel_num = fully_valid_parcel_num + partially_valid_parcel_num

            # Position data for the fully valid back trajectories.
            xpos_full = np.copy(self.ds_full.variables['xpos'])
            ypos_full = np.copy(self.ds_full.variables['ypos'])
            zpos_full = np.copy(self.ds_full.variables['zpos'])

            # Position data for the partially valid trajectories with the
            #   buffer of nan's added to the end of the array.
            xpos_partial = np.concatenate((np.copy(self.ds_partial.variables['xpos']), self.nan_buffer))
            ypos_partial = np.concatenate((np.copy(self.ds_partial.variables['ypos']), self.nan_buffer))
            zpos_partial = np.concatenate((np.copy(self.ds_partial.variables['zpos']), self.nan_buffer))

            # Combine the full and partial sets of trajectory positions into
            #   one array.
            self.xpos = np.concatenate((xpos_full, xpos_partial), axis=1)
            self.ypos = np.concatenate((ypos_full, ypos_partial), axis=1)
            self.zpos = np.concatenate((zpos_full, zpos_partial), axis=1)

            # Model file at the earliest time of the trajectory dataset (zero
            #   indexed, add one to get the correct CM1 model file).
            # Using value from fully valid data, since it should be the same in
            #   both datasets.
            self.file_num_offset = self.ds_full.variables['file_num_offset'][0]

            # Array of model simulation times (in seconds) for the trajectory dataset.
            self.simulation_times = np.copy(self.ds_full.variables['time'])

            # List of vorticity budget variables, which are all variables in
            #   the file except those containing position data (which end in
            #   'pos') and those that have only one dimension (which should
            #   just be file_num_offset).
            self.budget_var_keys = [var_name for var_name in self.ds_full.variables.keys() if not var_name.endswith('pos') if len(self.ds_full.variables[var_name].dimensions) > 1]

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If only the fully valid dataset exists.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if self.full_flag == True and self.partial_flag == False:
            # Position data for the back trajectories.
            self.xpos = np.copy(self.ds_full.variables['xpos'])
            self.ypos = np.copy(self.ds_full.variables['ypos'])
            self.zpos = np.copy(self.ds_full.variables['zpos'])

            # Total number of parcels for this set of data.
            self.total_parcel_num = self.ds_full.dimensions['number_parcels'].size

            # Model file at the earliest time of the trajectory dataset (zero
            #   indexed, add one to get the correct CM1 model file).
            self.file_num_offset = self.ds_full.variables['file_num_offset'][0]

            # Get the number of time steps in the full set of parcel data.
            self.parcel_time_step_num = self.ds_full.dimensions['time'].size

            # Array of model simulation times (in seconds) for the trajectory dataset.
            self.simulation_times = np.copy(self.ds_full.variables['time'])

            # List of vorticity budget variables, which are all variables in
            #   the file except those containing position data (which end in
            #   'pos') and those that have only one dimension (which should
            #   just be file_num_offset).
            self.budget_var_keys = [var_name for var_name in self.ds_full.variables.keys() if not var_name.endswith('pos') if len(self.ds_full.variables[var_name].dimensions) > 1]

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # If only the partially valid dataset exists.
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        if self.full_flag == False and self.partial_flag == True:
            # Position data for the back trajectories.
            self.xpos = np.copy(self.ds_partial.variables['xpos'])
            self.ypos = np.copy(self.ds_partial.variables['ypos'])
            self.zpos = np.copy(self.ds_partial.variables['zpos'])

            # Total number of parcels for this set of data.
            self.total_parcel_num = self.ds_partial.dimensions['number_parcels'].size

            # Model file at the earliest time of the trajectory dataset (zero
            #   indexed, add one to get the correct CM1 model file).
            self.file_num_offset = self.ds_partial.variables['file_num_offset'][0]

            # Get the number of time steps in the full set of parcel data.
            self.parcel_time_step_num = self.ds_partial.dimensions['time'].size

            # Array of model simulation times (in seconds) for the trajectory dataset.
            self.simulation_times = np.copy(self.ds_partial.variables['time'])

            # List of vorticity budget variables, which are all variables in
            #   the file except those containing position data (which end in
            #   'pos') and those that have only one dimension (which should
            #   just be file_num_offset).
            self.budget_var_keys = [var_name for var_name in self.ds_partial.variables.keys() if not var_name.endswith('pos') if len(self.ds_partial.variables[var_name].dimensions) > 1]

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
        if self.full_flag == True and self.partial_flag == True:
            budget_var_full = np.copy(self.ds_full.variables[budget_var_name])
            budget_var_partial = np.concatenate((np.copy(self.ds_partial.variables[budget_var_name]), self.nan_buffer))
            budget_var = np.concatenate((budget_var_full, budget_var_partial), axis=1)
            return budget_var

        if self.full_flag == True and self.partial_flag == False:
            return np.copy(self.ds_full.variables[budget_var_name])

        if self.full_flag == False and self.partial_flag == True:
            return np.copy(self.ds_partial.variables[budget_var_name])

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

    # Remove the horizontal (h) or vertical (v) part of the budget variable
    #   label so that the horizontal and vertical components of turbulence and
    #   diffusion get plotted together.
    def remove_dirFromVar(self, var_name):
        var_name_split = var_name.split('_')
        new_name = var_name_split[0] + '_' + var_name_split[-1][1:]
        return new_name

    # Add the horizontal or vertical (v) back into the budget variable label to
    #   access data.
    def add_dir2var(self, base_name, mode):
        base_name_split = base_name.split('_')
        new_name = base_name_split[0] + '_' + mode + base_name_split[-1]
        return new_name

