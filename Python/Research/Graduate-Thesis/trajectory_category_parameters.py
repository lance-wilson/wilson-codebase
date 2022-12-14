#!/usr/bin/env python3
#
# Name:
#   trajectory_category_parameters.py
#
# Purpose:  Store the values used to define categories of trajectories based on
#           the region of the storm they come from.
#
# Syntax: from trajectory_category_parameters import termination_parameters, category_parameters
#         termination_parameters()
#         category_parameters()
#
# Execution Example:
#   from trajectory_category_parameters import termination_parameters, category_parameters
#   end_point_params = termination_parameters()
#   category_params = category_parameters()
#
# Modification History:
#   2022/04/14 - Lance Wilson:  Created.
#   2022/05/10 - Lance Wilson:  Modified to return entire dictionary so that
#                               categorize_forward_trajectories.py can
#                               determine all categories when run. 
#

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Parameters used for determining if the trajectory ends in the correct place.
#   xmin,xmax:          Limits of the termination region in the E-W direction.
#   ymin,ymax:          Limits of the termination region in the N-S direction.
#   zmin,zmax:          Vertical limits of the termination region.
#   zvort_threshold:    Minimum vertical vorticity (1) at model level (2).
#   w_threshold:        Minimum vertical velocity (1) at model level (2).
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def termination_parameters():
    parameters = {
            'mesocyclone':     {'xmin'            : None,
                                'xmax'            : None,
                                'ymin'            : None,
                                'ymax'            : None,
                                'zmin'            : 600.,
                                'zmax'            : 1000.,
                                'thresholds'      : {'zvort': [30, 0.001, '>'],
                                                     'w': [30, 0.0, '>'],},
                                },
             }
    #return parameters[variable]
    return parameters

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Parameters to be used to determine if the forward trajectory belongs to a
# certain category.
#   xmin,xmax:          Limits of the category region in the E-W direction.
#   ymin,ymax:          Limits of the category region in the N-S direction.
#   zmin,zmax:          Vertical limits of the termination region.
#                       Position limits above are given as a list in this
#                       format: [model coordinate (meters), percentile of data
#                       to start comparing to the limit, percentile of data to
#                       end comparison to compare to the limit]
#   thresholds:         Criteria that must be met to be part of a category,
#                       stored as a dictionary. The keys of the dictionary are
#                       the model fields to be compared against.
#                       Each threshold dictionary value is a list in this
#                       format: [model level (vertical grid point index), value
#                       of the field, comparison operator (e.g. '>')]
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def category_parameters():

    parameters = {
            'forward_flank':   {'xmin'              : None,
                                'xmax'              : None,
                                'ymin'              : None,
                                'ymax'              : None,
                                'zmin'              : None,
                                'zmax'              : [400., 0, 80],
                                'thresholds'        : {'thpert' : [5, -1.0, '<', 'all'],
                                                       'zvort'  : [5, 0.4, '<', 'all'],
                                                       'u'      : [30, 0.0, '<', 'all'],},
                                },
            'up_over':         {'xmin'              : None,
                                'xmax'              : None,
                                'ymin'              : None,
                                'ymax'              : None,
                                'zmin'              : [400., 60, 80],
                                'zmax'              : None,
                                'thresholds'        : {'thpert' : [5, 0.0, '<', 'any'],
                                                       'zvort'  : [5, 0.4, '<', 'all'],
                                                       'u'      : [30, 0.0, '<', 'all'],},
                                },
            'wraparound':      {'xmin'              : None,
                                'xmax'              : None,
                                'ymin'              : None,
                                'ymax'              : None,
                                'zmin'              : None,
                                'zmax'              : None,
                                'thresholds'        : {'thpert' : [5, 0.0, '<', 'all'],
                                                       'zvort'  : [5, 0.4, '<', 'all'],
                                                       'u'      : [30, 0.0, '>', 'any'],},
                                },
            'environment':     {'xmin'              : None,
                                'xmax'              : None,
                                'ymin'              : None,
                                'ymax'              : None,
                                'zmin'              : None,
                                'zmax'              : [500., 0, 80],
                                'thresholds'        : {'thpert' : [5, 0.0, '>', 'any'],},
                                },
        }

    #return parameters[variable]
    return parameters

