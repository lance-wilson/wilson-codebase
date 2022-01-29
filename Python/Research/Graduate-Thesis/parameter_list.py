#!/usr/bin/env python3
#
# Name:
#   parameter_list.py
#
# Purpose:  Store the values of the plotting parameter dictionary separately so
#           that it doesn't have to take space at the beginning of the plotting
#           files. Also includes dictionaries of colorbar labels and matplotlib
#           legend labels for vorticity budget variables, and a dictionary for
#           substituting the dimension of the data.
#
# Syntax: from parameter_list import parameters
#         parameters = parameters(variable)
#
# Execution Example:
#   from parameter_list import parameters
#   params = parameters('dbz')
#
# Modification History:
#   2021/07/28 - Lance Wilson:  Created.
#

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Parameters used for plotting trajectory data (both back and forward).
#   val_interval:       Distance between tick labels on the colorbar.
#   datamin:            Minimum value variable on the colorbar.
#   datamax:            Maximum value variable on the colorbar.
#   offset:             Vertical height of the layer (in CM1 grid points).
#   contour_interval:   Number of contours to plot.
#   colormap:           Matplotlib colormap to use.
#   bar_label:          Label for the color bar.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def parameters(variable):
    parameters = {  'dbz': {'val_interval'      : 5,
                        'datamin'           : -35,
                        'datamax'           : 65,
                        'offset'            : 0,
                        'contour_interval'  : 100,
                        'colormap'          : 'gist_ncar',
                        'bar_label'         : 'Reflectivity (dbz)'},
              'xvort': {'val_interval'      : 0.1,
                        'datamin'           : -0.35,
                        'datamax'           : 0.55,
                        'offset'            : 10,
                        'contour_interval'  : 10,
                        'colormap'          : 'PuOr',
                        'bar_label'         : 'Horizontal Vorticity (1/s)'},
             'thpert': {'val_interval'      : 2,
                        'datamin'           : -5.0,
                        'datamax'           : 5.0,
                        'offset'            : 5,
                        'contour_interval'  : 11,
                        'colormap'          : 'PuOr',
                        'bar_label' : 'Potential Temperature Perturbation (K)'},
                  'u': {'val_interval'      : 12,
                        'datamin'           : -30.0,
                        'datamax'           : 30.0,
                        'offset'            : 25,
                        'contour_interval'  : 11,
                        'colormap'          : 'PuOr',
                        'bar_label'         : 'E-W Horizontal Velocity (m/s)'},
                  'v': {'val_interval'      : 12,
                        'datamin'           : -30.0,
                        'datamax'           : 30.0,
                        'offset'            : 25,
                        'contour_interval'  : 11,
                        'colormap'          : 'PuOr',
                        'bar_label'         : 'N-S Horizontal Velocity (m/s)'},
                  'w': {'val_interval'      : 2,
                        'datamin'           : -5.0,
                        'datamax'           : 5.0,
                        'offset'            : 25,
                        'contour_interval'  : 11,
                        'colormap'          : 'PuOr',
                        'bar_label'         : 'Vertical Velocity (m/s)'}
             }
    return parameters[variable]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Labels to be used for the vorticity budget variable colorbar (when plotting
#   trajectory paths spatially).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def budget_barlabels(variable):

    bar_labels = {
            'x_stretch_term'   : r'E-W Stretching (s$\mathregular{^{-2}}$)',
            'y_stretch_term'   : r'N-S Stretching (s$\mathregular{^{-2}}$)',
            'z_stretch_term'   : r'Vertical Stretching (s$\mathregular{^{-2}}$)',
            'x_tilt_term'      : r'E-W Tilting (s$\mathregular{^{-2}}$)',
            'y_tilt_term'      : r'N-S Tilting (s$\mathregular{^{-2}}$)',
            'z_tilt_term'      : r'Vertical Tilting (s$\mathregular{^{-2}}$)',
            'x_solenoid_term'  : r'E-W Solenoid (s$\mathregular{^{-2}}$)',
            'y_solenoid_term'  : r'N-S Solenoid (s$\mathregular{^{-2}}$)',
            'z_solenoid_term'  : r'Vertical Solenoid (s$\mathregular{^{-2}}$)',
            'x_advection_term' : r'E-W Advection (s$\mathregular{^{-2}}$)',
            'y_advection_term' : r'N-S Advection (s$\mathregular{^{-2}}$)',
            'z_advection_term' : r'Vertical Advection (s$\mathregular{^{-2}}$)',
            'xvortb_buoy'      : r'E-W Vort. Buoyancy (s$\mathregular{^{-2}}$)',
            'yvortb_buoy'      : r'N-S Vort. Buoyancy (s$\mathregular{^{-2}}$)',
            'xvortb_hadv'      : r'Horiz. Advection of E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_hadv'      : r'Horiz. Advection of N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_hadv'      : r'Horiz. Advection of Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_vadv'      : r'Vert. Advection of E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_vadv'      : r'Vert. Advection of N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_vadv'      : r'Vert. Advection of Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_hedif'     : r'Horiz. Diffusion of E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_hedif'     : r'Horiz. Diffusion of N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_hedif'     : r'Horiz. Diffusion of Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_vedif'     : r'Vert. Diffusion of E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_vedif'     : r'Vert. Diffusion of N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_vedif'     : r'Vert. Diffusion of Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_hturb'     : r'Horiz. Turbulence, E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_hturb'     : r'Horiz. Turbulence, N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_hturb'     : r'Horiz. Turbulence, Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_vturb'     : r'Vert. Turbulence, E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_vturb'     : r'Vert. Turbulence, N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_vturb'     : r'Vert. Turbulence, Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_pgrad'     : r'Pressure Gradient, E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_pgrad'     : r'Pressure Gradient, N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_pgrad'     : r'Pressure Gradient, Vertical Vort. (s$\mathregular{^{-2}}$)',
            # Combined terms
            'xvortb_turb'      : r'Total Turbulence, E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_turb'      : r'Total Turbulence, N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_turb'      : r'Total Turbulence, Vertical Vort. (s$\mathregular{^{-2}}$)',
            'xvortb_edif'      : r'Total Diffusion of E-W Vort. (s$\mathregular{^{-2}}$)',
            'yvortb_edif'      : r'Total Diffusion of N-S Vort. (s$\mathregular{^{-2}}$)',
            'zvortb_edif'      : r'Total Diffusion of Vertical Vort. (s$\mathregular{^{-2}}$)',
            # Height
            'zpos'             : r'Height Above Ground (m)',
        }
    return bar_labels[variable]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Labels to be used for the vorticity budget variable legend labels (when
#   plotting trajectory components vs. time).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def budget_legendlabels(variable):

    legend_labels = {
                '_stretch_term'   : 'Stretching',
                '_tilt_term'      : 'Tilting',
                '_solenoid_term'  : 'Solenoid',
                '_advection_term' : 'Advection',
                'vortb_buoy'      : 'Buoyancy',
                'vortb_hadv'      : 'Horiz. Advection',
                'vortb_vadv'      : 'Vert. Advection',
                'vortb_hedif'     : 'Hor. Diffusion',
                'vortb_vedif'     : 'Vert. Diffusion',
                'vortb_hturb'     : 'Horiz. Turbulence',
                'vortb_vturb'     : 'Vert. Turbulence',
                'vortb_pgrad'     : 'Pressure Gradient',
                # Combined terms
                'vortb_turb'      : 'Total Turbulence',
                'vortb_edif'      : 'Total Diffusion',
            }
    return legend_labels[variable[1:]]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Colormap to be used for coloring trajectory paths.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def budget_colormap(budget_var_name):
    if budget_var_name == 'zpos':
        colormap_name = 'gist_rainbow'
    else:
        colormap_name = 'RdBu_r'
    return colormap_name

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Substitute coordinate identifier with full description.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def title_dir_sub(variable):
    title_dir_sub = {
                'x' : 'East-West Component of',
                'y' : 'North-South Component of',
                'z' : 'Vertical Component of',
                }
    return title_dir_sub[variable]

