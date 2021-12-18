#!/usr/bin/env python3
#
# Name:
#   calc_vort_equation.py
#
# Purpose:  Calculate the terms of the vorticity equation for a subset domain
#           within the netCDF output from a run of Cloud Model 1.
#
# Syntax: python calc_vort_equation.py model_version
#
#   Input:
#
# Execution Example:
#   python calc_vort_equation.py v5
#
# Modification History:
#   2019/08/14 - Lance Wilson:  Created original program (vorticity_tendency.py).
#   2019/08/22 - Lance Wilson:  Completed terms of vorticity equation.
#   2019/09/04 - Lance Wilson:  Updated tilting terms to use new calculation method.
#   2019/09/06 - Lance Wilson:  Reconciled differences in solenoid terms.
#   2021/09/30 - Lance Wilson:  Created calc_vort_equation.py from
#                               vorticity_tendency.py to add file output and
#                               account for model versions.
#

from calc_parcel_bounds import calc_boundaries

from netCDF4 import Dataset
from netCDF4 import MFDataset

import glob
import numpy as np
import sys
import time

def calc_du_dx(u_wind, stagger_x_coord):
    # Calculate du/dx at unstaggered grid point i using staggered u values.
    u_diffs = u_wind[:,:,1:] - u_wind[:,:,:-1]
    x_diffs = stagger_x_coord[1:] - stagger_x_coord[:-1]
    return u_diffs/x_diffs[None,None,:]

def calc_dv_dy(v_wind, stagger_y_coord):
    # Calculate dv/dy at unstaggered grid point j using staggered v values.
    v_diffs = v_wind[:,1:,:] - v_wind[:,:-1,:]
    y_diffs = stagger_y_coord[1:] - stagger_y_coord[:-1]
    return v_diffs/y_diffs[None,:,None]

def calc_avg_du_dy(u_wind, grad_dy):
    # Calculate du/dy using centered differencing, with du/dy being valid at
    #   the staggered u points.
    u_y_diffs = np.gradient(u_wind, axis=1)
    du_dy = u_y_diffs/grad_dy[None,:,None]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    return (du_dy[:,:,1:] + du_dy[:,:,:-1])/2.

def calc_avg_du_dz(u_wind, grad_dz):
    # Calculate du/dz using centered differencing, with du/dz being valid at
    #   the staggered u points.
    u_z_diffs = np.gradient(u_wind, axis=0)
    du_dz = u_z_diffs/grad_dz[:,None,None]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    return (du_dz[:,:,1:] + du_dz[:,:,:-1])/2.

def calc_avg_dv_dx(v_wind, grad_dx):
    # Calculate dv/dx using centered differencing, with dv/dx being valid at
    #   the staggered v points.
    v_x_diffs = np.gradient(v_wind, axis=2)
    dv_dx = v_x_diffs/grad_dx[None,None,:]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    return (dv_dx[:,1:,:] + dv_dx[:,:-1,:])/2.

def calc_avg_dv_dz(v_wind, grad_dz):
    # Calculate dv/dz using centered differencing, with dv/dz being valid at
    #   the staggered v points.
    v_z_diffs = np.gradient(v_wind, axis=0)
    dv_dz = v_z_diffs/grad_dz[:,None,None]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    return (dv_dz[:,1:,:] + dv_dz[:,:-1,:])/2.

def calc_avg_dw_dx(w_wind, grad_dx):
    # Calculate dw/dx using centered differencing, with dw/dx being valid at
    #   the staggered w points (which are vertically stacked with the
    #   thermodynamic points).
    w_x_diffs = np.gradient(w_wind, axis=2)
    dw_dx = w_x_diffs/grad_dx[None,None,:]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    return (dw_dx[1:,:,:] + dw_dx[:-1,:,:])/2.

def calc_avg_dw_dy(w_wind, grad_dy):
    # Calculate dw/dy using centered differencing, with dw/dy being valid at
    #   the staggered w points (which are vertically stacked with the
    #   thermodynamic points).
    w_y_diffs = np.gradient(w_wind, axis=1)
    dw_dy = w_y_diffs/grad_dy[None,:,None]

    # To keep arrays the same size for component calculation, averaging
    #   data to unstaggered thermodynamic points.
    return (dw_dy[1:,:,:] + dw_dy[:-1,:,:])/2.

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate solenoid (baroclinic generation) term for all three components
#   xvort_component: (1/rho^2) * (drho/dy * dp/dz - drho/dz * dp/dy)
#   yvort_component: (1/rho^2) * (drho/dz * dp/dx - drho/dx * dp/dz)
#   zvort_component: (1/rho^2) * (drho/dx * dp/dy - drho/dy * dp/dx)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_solenoid_terms(pressure, rho, grad_dx, grad_dy, grad_dz):
    # Note: np.gradient takes centered differences of the field at each point,
    #       except at the edges where it uses forward or backward differences.
    # Note: indices of np.gradient result refer to the axes on which the
    #       gradient is taken (i.e. 0 corresponds to gradient in k/z direction,
    #       1 to j/y direction, and 2 to i/x direction).

    # Calculate dp/dx.
    grad_p_x = np.gradient(pressure, axis=2)
    dp_dx = grad_p_x/grad_dx[None,None,:]

    # Calculate d(rho)/dx.
    grad_rho_x = np.gradient(rho, axis=2)
    drho_dx = grad_rho_x/grad_dx[None,None,:]

    # Calculate dp/dy.
    grad_p_y = np.gradient(pressure, axis=1)
    dp_dy = grad_p_y/grad_dy[None,:,None]

    # Calculate d(rho)/dy.
    grad_rho_y = np.gradient(rho, axis=1)
    drho_dy = grad_rho_y/grad_dy[None,:,None]

    # Calculate dp/dz.
    grad_p_z = np.gradient(pressure, axis=0)
    dp_dz = grad_p_z/grad_dz[:,None,None]

    # Calculate d(rho)/dz.
    grad_rho_z = np.gradient(rho, axis=0)
    drho_dz = grad_rho_z/grad_dz[:,None,None]

    x_solenoid_term = (1/rho**2) * (drho_dy * dp_dz - drho_dz * dp_dy)
    y_solenoid_term = (1/rho**2) * (drho_dz * dp_dx - drho_dx * dp_dz)
    z_solenoid_term = (1/rho**2) * (drho_dx * dp_dy - drho_dy * dp_dx)

    return (x_solenoid_term, y_solenoid_term, z_solenoid_term)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate Advection terms
#   -1.*u * d(vort)/dx - v * d(vort)/dy - w * d(vort)/dz
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def calc_advection(vort, avg_u, avg_v, avg_w):
    grad_vort_x = np.gradient(vort, axis=2)
    grad_vort_y = np.gradient(vort, axis=1)
    grad_vort_z = np.gradient(vort, axis=0)

    # Calculate d(vort)/dx.
    dvort_dx = grad_vort_x/grad_dx[None,None,:]
    # Calculate d(vort)/dy.
    dvort_dy = grad_vort_y/grad_dy[None,:,None]
    # Calculate d(vort)/dz.
    dvort_dz = grad_vort_z/grad_dz[:,None,None]

    return -1.*avg_u * dvort_dx - avg_v * dvort_dy - avg_w * dvort_dz

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Beginning of Main Program
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
if len(sys.argv) > 1:
    # Model run that is being used.
    version_number = sys.argv[1]
else:
    print('Parcel label or version number was not specified.')
    print('Syntax: python3 calc_vort_equation.py model_version')
    print('Example: python3 calc_vort_equation.py v5')
    print('Currently supported version numbers: v3, 10s, v4, v5')
    sys.exit()

model_dir = '75m_100p_{:s}/'.format(version_number)

# Number of model grid points to add to each side of the boundary edge calculation.
bound_buffer = 5

gravity = 9.80665 #m/s^2

# Get list of all CM1 output files for this run.
model_file_list = glob.glob(model_dir + 'JS_75m_run*_[0-9]*.nc')

# Open the netCDF dataset using netCDF4 module.
dataset = MFDataset(model_file_list)

# Total number of time steps to include in the output file.
model_time_steps = len(model_file_list)

if version_number == 'v3':
    print('Using default values for domain boundaries (back trajectory data not available)')
    # Boundary indicies for slicing the Dataset.
    k1 = 0
    k2 = 144#144
    j1 = 31#400#0#360
    j2 = 475#501#920#461
    i1 = 238#340#0#410
    i2 = 623#441#921#511
else:
    # Calculate the indices used as boundaries of the subset domain written to
    #   the vorticity budget output netCDF file using back trajectory data.
    #   Minimum boundary values: i1, j1, k1.
    #   Maximum boundary values: i2, j2, k2.
    i1, j1, k1, i2, j2, k2 = calc_boundaries(version_number, bound_buffer)

# Get staggered coordinates for the wind data, converted to meters.
stagger_x_coord = np.copy(dataset.variables['xf'][i1:i2+1])*1000.
stagger_y_coord = np.copy(dataset.variables['yf'][j1:j2+1])*1000.
stagger_z_coord = np.copy(dataset.variables['zf'][k1:k2+1])*1000.
# Get unstaggered coordinates for thermodynamic variables, converted to meters.
x_coord = np.copy(dataset.variables['xh'][i1:i2])*1000.
y_coord = np.copy(dataset.variables['yh'][j1:j2])*1000.
z_coord = np.copy(dataset.variables['z'][k1:k2])*1000.

# Gradients of spatial coordinates.
grad_dx = np.gradient(x_coord)
grad_dy = np.gradient(y_coord)
grad_dz = np.gradient(z_coord)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Setup output netCDF file and create variables.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Open the output netCDF file.
ds_out = Dataset(model_dir + 'back_traj_analysis/{:s}_direct_vort_equation.nc'.format(version_number), mode='w')

# Create netCDF variable dimensions.
x_dim = ds_out.createDimension('ni', i2-i1)
y_dim = ds_out.createDimension('nj', j2-j1)
z_dim = ds_out.createDimension('nk', k2-k1)
time_dim = ds_out.createDimension('time', None)

# Create variable containing the subset of x coordinate data used in the output.
xcoord_var = ds_out.createVariable('xh', np.float32, ('ni'))
xcoord_var.units = 'm'
xcoord_var.definition = getattr(dataset.variables['xh'], 'def')
xcoord_var[:] = x_coord

# Create variable containing the subset of y coordinate data used in the output.
ycoord_var = ds_out.createVariable('yh', np.float32, ('nj'))
ycoord_var.units = 'm'
ycoord_var.definition = getattr(dataset.variables['yh'], 'def')
ycoord_var[:] = y_coord

# Create variable containing the subset of z coordinate data used in the output.
zcoord_var = ds_out.createVariable('z', np.float32, ('nk'))
zcoord_var.units = 'm'
zcoord_var.definition = getattr(dataset.variables['z'], 'def')
zcoord_var[:] = z_coord

# Create variable in the output file for time.
time_var = ds_out.createVariable('time', np.float32, ('time'))
time_var.units = dataset.variables['time'].units
time_var.definition = getattr(dataset.variables['time'], 'def')
time_var[:] = dataset.variables['time'][:]

# Create variable for the divergence/stretching term in the east-west direction.
x_stretch_term_var = ds_out.createVariable('x_stretch_term', np.float32, ('time','nk','nj','ni'))
x_stretch_term_var.units = 's^-2'
x_stretch_term_var.definition = 'Stretching Term of East-West Horizontal Vorticity Equation'

# Create variable for the divergence/stretching term in the north-south direction.
y_stretch_term_var = ds_out.createVariable('y_stretch_term', np.float32, ('time','nk','nj','ni'))
y_stretch_term_var.units = 's^-2'
y_stretch_term_var.definition = 'Stretching Term of North-South Horizontal Vorticity Equation'

# Create variable for the divergence/stretching term in the vertical direction.
z_stretch_term_var = ds_out.createVariable('z_stretch_term', np.float32, ('time','nk','nj','ni'))
z_stretch_term_var.units = 's^-2'
z_stretch_term_var.definition = 'Stretching Term of Vertical Vorticity Equation'

# Create variable for the north-south horizontal tilting term.
x_tilt_term_var = ds_out.createVariable('x_tilt_term', np.float32, ('time','nk','nj','ni'))
x_tilt_term_var.units = 's^-2'
x_tilt_term_var.definition = 'Tilting Term of East-West Horizontal Vorticity Equation'

# Create variable for the east-west horizontal tilting term.
y_tilt_term_var = ds_out.createVariable('y_tilt_term', np.float32, ('time','nk','nj','ni'))
y_tilt_term_var.units = 's^-2'
y_tilt_term_var.definition = 'Tilting Term of North-South Horizontal Vorticity Equation'

# Create variable for the vertical tilting term.
z_tilt_term_var = ds_out.createVariable('z_tilt_term', np.float32, ('time','nk','nj','ni'))
z_tilt_term_var.units = 's^-2'
z_tilt_term_var.definition = 'Tilting Term of Vertical Vorticity Equation'

# Create variable for the x-direction solenoid term.
x_solenoid_term_var = ds_out.createVariable('x_solenoid_term', np.float32, ('time','nk','nj','ni'))
x_solenoid_term_var.units = 's^-2'
x_solenoid_term_var.definition = 'Solenoid (Baroclinic Generation) Term of East-West Horizontal Vorticity Equation'

# Create variable for the y-direction solenoid term.
y_solenoid_term_var = ds_out.createVariable('y_solenoid_term', np.float32, ('time','nk','nj','ni'))
y_solenoid_term_var.units = 's^-2'
y_solenoid_term_var.definition = 'Solenoid (Baroclinic Generation) Term of North-South Horizontal Vorticity Equation'

# Create variable for the z-direction solenoid term.
z_solenoid_term_var = ds_out.createVariable('z_solenoid_term', np.float32, ('time','nk','nj','ni'))
z_solenoid_term_var.units = 's^-2'
z_solenoid_term_var.definition = 'Solenoid (Baroclinic Generation) Term of Vertical Vorticity Equation'

# Create variable for the vertical advection term.
x_advection_var = ds_out.createVariable('x_advection_term', np.float32, ('time','nk','nj','ni'))
x_advection_var.units = 's^-2'
x_advection_var.definition = 'Advection  Term of East-West Horizontal Vorticity Equation'

# Create variable for the vertical advection term.
y_advection_var = ds_out.createVariable('y_advection_term', np.float32, ('time','nk','nj','ni'))
y_advection_var.units = 's^-2'
y_advection_var.definition = 'Advection  Term of North-South Horizontal Vorticity Equation'

# Create variable for the vertical advection term.
z_advection_var = ds_out.createVariable('z_advection_term', np.float32, ('time','nk','nj','ni'))
z_advection_var.units = 's^-2'
z_advection_var.definition = 'Advection  Term of Vertical Vorticity Equation'

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate terms of each component of the vorticity equation at each time step.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
for time_index in range(model_time_steps):
    # Timer
    start = time.time()

    # Storing data in numpy arrays runs faster than accessing data directly from dataset.
    # Note: extra index for staggered wind grid points are included here.
    u_wind = np.copy(dataset.variables['u'][time_index,k1:k2,j1:j2,i1:i2+1])
    v_wind = np.copy(dataset.variables['v'][time_index,k1:k2,j1:j2+1,i1:i2])
    w_wind = np.copy(dataset.variables['w'][time_index,k1:k2+1,j1:j2,i1:i2])

    # East-West Vorticity
    x_vort = np.copy(dataset.variables['xvort'][time_index,k1:k2,j1:j2,i1:i2])
    # North-South Vorticity
    y_vort = np.copy(dataset.variables['yvort'][time_index,k1:k2,j1:j2,i1:i2])
    # Vertical Vorticity
    z_vort = np.copy(dataset.variables['zvort'][time_index,k1:k2,j1:j2,i1:i2])

    # Get density and pressure.
    rho_perturb = np.copy(dataset.variables['rhopert'][time_index,k1:k2,j1:j2,i1:i2])
    pressure_perturb = np.copy(dataset.variables['prspert'][time_index,k1:k2,j1:j2,i1:i2])
    base_pressure = np.copy(dataset.variables['prs0'][time_index,k1:k2,j1:j2,i1:i2])

    base_rho = (-1./gravity) * np.gradient(base_pressure, axis=0)/grad_dz[:,None,None]

    rho = base_rho + rho_perturb
    pressure = base_pressure + pressure_perturb

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Solenoid Terms
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    x_solenoid_term, y_solenoid_term, z_solenoid_term = calc_solenoid_terms(pressure, rho, grad_dx, grad_dy, grad_dz)

    x_solenoid_term_var[time_index,:,:,:] = x_solenoid_term
    y_solenoid_term_var[time_index,:,:,:] = y_solenoid_term
    z_solenoid_term_var[time_index,:,:,:] = z_solenoid_term

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Advection Terms
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Average the nearest staggered wind values to get a value at the
    #   unstaggered grid point.
    avg_u = (u_wind[:,:,:-1] + u_wind[:,:,1:])/2.
    avg_v = (v_wind[:,:-1,:] + v_wind[:,1:,:])/2.
    avg_w = (w_wind[:-1,:,:] + w_wind[1:,:,:])/2.

    x_advection_var[time_index,:,:,:] = calc_advection(x_vort, avg_u, avg_v, avg_w)
    y_advection_var[time_index,:,:,:] = calc_advection(y_vort, avg_u, avg_v, avg_w)
    z_advection_var[time_index,:,:,:] = calc_advection(z_vort, avg_u, avg_v, avg_w)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Divergence/Stretching Terms
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Derivatives for the Divergence/Stretching Terms
    du_dx = calc_du_dx(u_wind, stagger_x_coord)
    dv_dy = calc_dv_dy(v_wind, stagger_y_coord)
    
    # North-South Horizontal Divergence/Stretching Term
    #   xvort * du/dx
    x_stretch_term_var[time_index,:,:,:] = x_vort * du_dx

    # North-South Horizontal Divergence/Stretching Term
    #   yvort * dv/dy
    y_stretch_term_var[time_index,:,:,:] = y_vort * dv_dy

    # Vertical Divergence/Stretching Term
    #   -1 * zvort * (du/dx + dv/dy) or zvort * dw/dz
    #   Using -(du/dx + dv/dy) = dw/dz, since dw/dz may be small in parts of
    #   the domain
    z_stretch_term_var[time_index,:,:,:] = -1. * z_vort * (du_dx + dv_dy)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Tilting Terms
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Tilting Term for East-West Horizontal Vorticity
    #   yvort*du/dy + zvort*du/dz
    x_tilt_term = y_vort * calc_avg_du_dy(u_wind, grad_dy) + z_vort * calc_avg_du_dz(u_wind, grad_dz)
    x_tilt_term_var[time_index,:,:,:] = x_tilt_term

    # Tilting Term for North-South Horizontal Vorticity
    #   xvort*dv/dx + zvort*dv/dz
    y_tilt_term = x_vort * calc_avg_dv_dx(v_wind, grad_dx) + z_vort * calc_avg_dv_dz(v_wind, grad_dz)
    y_tilt_term_var[time_index,:,:,:] = y_tilt_term

    # Tilting Term for Vertical Vorticity
    #   xvort*dw/dx + yvort*dw/dy
    z_tilt_term = x_vort * calc_avg_dw_dx(w_wind, grad_dx) + y_vort * calc_avg_dw_dy(w_wind, grad_dy)
    z_tilt_term_var[time_index,:,:,:] = z_tilt_term

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Total Vorticity Tendency
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #lagrangian_vort = div_term - tilt_term1 + tilt_term2 + solenoid_term
    #eulerian_vort = advection + lagrangian_vort

    stop = time.time()
    print('Model time step {:d} completed in {:.1f} seconds'.format(time_index, stop-start))

# Close netCDF files.
ds_out.close()
dataset.close()

