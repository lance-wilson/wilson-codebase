#!/usr/bin/env python3
#
# Name:
#   calc_vort_budget.py
#
# Purpose:  Calculate vorticity tendency based on momentum budget variables in
#           CM1, and output to a netCDF file.
#
# Syntax: python3 calc_vort_budget.py model_version
#
#   Input:
#
# Execution Example:
#   python3 calc_vort_budget.py v5
#
# Temporary Execution Example (Run local script on server):
#   ssh vortex python < calc_vort_budget.py - v5
#
# Modification History:
#   2021/09/28 - Lance Wilson:  Created, splitting off code from
#                               calc_back_traj_vort_tendency.py to calculate
#                               vorticity budgets and output to netCDF file.
#

from calc_parcel_bounds import calc_boundaries

from netCDF4 import Dataset
from netCDF4 import MFDataset
import glob
import numpy as np
import sys
import time

if len(sys.argv) > 1:
    # Model run that is being used.
    version_number = sys.argv[1]
else:
    print('Parcel label or version number was not specified.')
    print('Syntax: python3 calc_vort_budget.py model_version')
    print('Example: python3 calc_vort_budget.py v5')
    print('Currently supported version numbers: v4, v5')
    sys.exit()

if version_number == 'v3' or version_number =='10s':
    print('Version number is not valid.')
    print('Currently supported version numbers: v4, v5')
    sys.exit()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Calculate Horizontal Vorticity in the East-West Direction
#   xvort = dw/dy - dv/dz
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_xvort_component(vb_var, wb_var, y_coord, z_coord):
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # d(v_budget)/dz, averaged to thermodynamic points.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Buoyancy budget is only in w, so xvort component will just be the dw/dy part.
    #   If looking at buoyancy budget, vb_var will be an empty array.
    if vb_var.size != 0:
        v_z_diffs = np.gradient(vb_var, axis=0)
        z_diffs = np.gradient(z_coord)
        # dvb_var_dz is valid at the staggered v/y points.
        dvb_var_dz = v_z_diffs/z_diffs[:,None,None]

        # To keep arrays the same size for component calculation, averaging
        #   data to unstaggered thermodynamic points.
        avg_dvb_var_dz = (dvb_var_dz[:,1:,:] + dvb_var_dz[:,:-1,:])/2.
    else:
        avg_dvb_var_dz = 0.

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # d(w_budget)/dy, averaged to thermodynamic points.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    w_y_diffs = np.gradient(wb_var, axis=1)
    y_diffs = np.gradient(y_coord)
    # dwb_var_dy is valid at the staggered w/z points.
    dwb_var_dy = w_y_diffs/y_diffs[None,:,None]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    avg_dwb_var_dy = (dwb_var_dy[1:,:,:] + dwb_var_dy[:-1,:,:])/2.

    return avg_dwb_var_dy - avg_dvb_var_dz

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Calculate Horizontal Vorticity in the North-South Direction
#   yvort = -(dw/dx - du/dz)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_yvort_component(ub_var, wb_var, x_coord, z_coord):
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # d(u_budget)/dz, averaged to thermodynamic points.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Buoyancy budget is only in w, so yvort component will just be the dw/dx part.
    #   If looking at buoyancy budget, ub_var will be an empty array.
    if ub_var.size != 0:
        u_z_diffs = np.gradient(ub_var, axis=0)
        z_diffs = np.gradient(z_coord)
        # dub_var_dz is valid at the staggered u/x points.
        dub_var_dz = u_z_diffs/z_diffs[:,None,None]

        # To keep arrays the same size for component calculation, averaging
        #   data to unstaggered thermodynamic points.
        avg_dub_var_dz = (dub_var_dz[:,:,1:] + dub_var_dz[:,:,:-1])/2.
    else:
        avg_dub_var_dz = 0.

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # d(w_budget)/dx, averaged to thermodynamic points.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    w_x_diffs = np.gradient(wb_var, axis=2)
    x_diffs = np.gradient(x_coord)
    # dwb_var_dx is valid at the staggered w/z points.
    dwb_var_dx = w_x_diffs/x_diffs[None,None,:]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    avg_dwb_var_dx = (dwb_var_dx[1:,:,:] + dwb_var_dx[:-1,:,:])/2.

    return avg_dub_var_dz - avg_dwb_var_dx

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#   Calculate Vertical Vorticity
#   zvort = dv/dx - du/dy
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_zvort_component(ub_var, vb_var, x_coord, y_coord):
    # No u or v buoyancy budget, so there should be no vertical vorticity component.
    if ub_var.size == 0 or vb_var.size == 0:
        return 0.

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # d(u_budget)/dy, averaged to thermodynamic points.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    u_y_diffs = np.gradient(ub_var, axis=1)
    y_diffs = np.gradient(y_coord)
    # dub_var_dy is valid at the staggered u/x points.
    dub_var_dy = u_y_diffs/y_diffs[None,:,None]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    avg_dub_var_dy = (dub_var_dy[:,:,1:] + dub_var_dy[:,:,:-1])/2.

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # d(v_budget)/dx, averaged to thermodynamic points.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    v_x_diffs = np.gradient(vb_var, axis=2)
    x_diffs = np.gradient(x_coord)
    # dvb_var_dx is valid at the staggered v/y points.
    dvb_var_dx = v_x_diffs/x_diffs[None,None,:]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    avg_dvb_var_dx = (dvb_var_dx[:,1:,:] + dvb_var_dx[:,:-1,:])/2.

    return avg_dvb_var_dx - avg_dub_var_dy

model_dir = '75m_100p_{:s}/'.format(version_number)

# Momentum Budget Variables (Model Terms)
#   'b_buoy' is only calculated in the w direction; the others have are
#   calculated in all three dimensions.
budget_variables = ['b_buoy', 'b_hadv', 'b_vadv', 'b_hedif', 'b_vedif', 'b_hturb', 'b_vturb', 'b_pgrad']

# Number of model grid points to add to each side of the boundary edge calculation.
bound_buffer = 5

# Get list of all CM1 output files for this run.
model_file_list = glob.glob(model_dir + 'JS_75m_run*_000*.nc')
# Open the netCDF dataset using netCDF4 module.
ds = MFDataset(model_file_list)

# Total number of time steps to include in the output file.
model_time_steps = len(model_file_list)

# Get staggered coordinates for the wind data, converted from kilometers to meters.
stagger_x_coord = np.copy(ds.variables['xf'])*1000.
stagger_y_coord = np.copy(ds.variables['yf'])*1000.
stagger_z_coord = np.copy(ds.variables['zf'])*1000.
# Get unstaggered coordinates for thermodynamic variables, converted from kilometers to meters.
x_coord = np.copy(ds.variables['xh'])*1000.
y_coord = np.copy(ds.variables['yh'])*1000.
z_coord = np.copy(ds.variables['z'])*1000.

# Calculate the indices used as boundaries of the subset domain written to
#   the vorticity budget output netCDF file.
#   Minimum boundary values: x1, y1, z1.
#   Maximum boundary values: x2, y2, z2.
x1, y1, z1, x2, y2, z2 = calc_boundaries(version_number, bound_buffer)

# Open the output netCDF file.
ds_out = Dataset(model_dir + 'back_traj_analysis/{:s}_model_vort_budget.nc'.format(version_number), mode='w')

# Create netCDF variable dimensions.
x_dim = ds_out.createDimension('ni', x2-x1)
y_dim = ds_out.createDimension('nj', y2-y1)
z_dim = ds_out.createDimension('nk', z2-z1)
time_dim = ds_out.createDimension('time', None)

# Create variable containing the subset of x coordinate data used in the output.
xcoord_var = ds_out.createVariable('xh', np.float32, ('ni'))
xcoord_var.units = 'm'
xcoord_var.definition = getattr(ds.variables['xh'], 'def')
xcoord_var[:] = x_coord[x1:x2]

# Create variable containing the subset of y coordinate data used in the output.
ycoord_var = ds_out.createVariable('yh', np.float32, ('nj'))
ycoord_var.units = 'm'
ycoord_var.definition = getattr(ds.variables['yh'], 'def')
ycoord_var[:] = y_coord[y1:y2]

# Create variable containing the subset of z coordinate data used in the output.
zcoord_var = ds_out.createVariable('z', np.float32, ('nk'))
zcoord_var.units = 'm'
zcoord_var.definition = getattr(ds.variables['z'], 'def')
zcoord_var[:] = z_coord[z1:z2]

# Create variable in the output file for time.
time_var = ds_out.createVariable('time', np.float32, ('time'))
time_var.units = ds.variables['time'].units
time_var.definition = getattr(ds.variables['time'], 'def')

# Calculate vorticity components for each term of the model momentum budgets separately.
for var_name in budget_variables:
    # Timer for the variable loop.
    start = time.time()

    # Create variable for the East-West component of vorticity for this term.
    xvort_var = ds_out.createVariable('xvort{:s}'.format(var_name), np.float32, ('time','nk','nj','ni'))
    xvort_var.units = 's^-2'

    # Create variable for the North-South component of vorticity for this term.
    yvort_var = ds_out.createVariable('yvort{:s}'.format(var_name), np.float32, ('time','nk','nj','ni'))
    yvort_var.units = 's^-2'

    # If this is not the buoyancy component, can create normal descriptions for
    #   the x and y components and the variable for the vertical component.
    if var_name != 'b_buoy':
        xvort_var.definition = 'xvort' + getattr(ds.variables['u' + var_name], 'def')[1:]
        yvort_var.definition = 'yvort' + getattr(ds.variables['v' + var_name], 'def')[1:]

        # Create variable for the vertical component of vorticity for this term.
        zvort_var = ds_out.createVariable('zvort{:s}'.format(var_name), np.float32, ('time','nk','nj','ni'))
        zvort_var.units = 's^-2'
        zvort_var.definition = 'zvort' + getattr(ds.variables['w' + var_name], 'def')[1:]
    # If this is the buoyancy variable, use the description of buoyancy from w
    #   momentum as the definition for the x and y components.
    else:
        xvort_var.definition = 'xvort' + getattr(ds.variables['w' + var_name], 'def')[1:]
        yvort_var.definition = 'yvort' + getattr(ds.variables['w' + var_name], 'def')[1:]

    for cur_file_num in range(model_time_steps):
        # Timer for the time loop.
        start2 = time.time()
        # There is no buoyancy variable for u and v momentum, so creating an
        #   empty array that can be passed and used as a check in component
        #   calculation functions.
        if var_name == 'b_buoy':
            ub_var = np.zeros((0))
            vb_var = np.zeros((0))

            # Time variable output is done with the buoyancy variable so
            #   that it is done only once for each time step.
            time_var[cur_file_num] = ds.variables['time'][cur_file_num]
        # Get this momentum budget term's x and y component if this is not the buoyancy term.
        else:
            ub_var = np.copy(ds.variables['u' + var_name][cur_file_num, z1:z2, y1:y2, x1:x2+1])
            vb_var = np.copy(ds.variables['v' + var_name][cur_file_num, z1:z2, y1:y2+1, x1:x2])
        # Get this momentum budget term's vertical component.
        wb_var = np.copy(ds.variables['w' + var_name][cur_file_num, z1:z2+1, y1:y2, x1:x2])

        # Calculate the East-West component of vorticity for this term.
        xvort_comp = calc_xvort_component(vb_var, wb_var, y_coord[y1:y2], z_coord[z1:z2])
        # Calculate the North-South component of vorticity for this term.
        yvort_comp = calc_yvort_component(ub_var, wb_var, x_coord[x1:x2], z_coord[z1:z2])

        # Output x and y components of vorticity to the netCDF file.
        xvort_var[cur_file_num,:,:,:] = xvort_comp
        yvort_var[cur_file_num,:,:,:] = yvort_comp

        # Calculate and output the vertical component of vorticity for this
        #   term only if this is not the buoyancy term.
        if var_name != 'b_buoy':
            zvort_comp = calc_zvort_component(ub_var, vb_var, x_coord[x1:x2], y_coord[y1:y2])
            zvort_var[cur_file_num,:,:,:] = zvort_comp

        stop2 = time.time()
        print("Variable {:>7s}, time step {:01d} took {:.2f} seconds".format(var_name, cur_file_num, stop2-start2))

    # Timer
    stop = time.time()
    print("Variable {:s} took {:.2f} seconds".format(var_name, stop-start))

# Close the netCDF files.
ds_out.close()
if not sys.flags.interactive:
    ds.close()

