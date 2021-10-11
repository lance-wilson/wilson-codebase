#!/usr/bin/env python
#
# Name:
#   round_off.py
#
# Purpose:
#   To compare the value of the velocity of a water droplet and the 
#       rounding errors that result when only one significant
#       figure of precision is used. Case 1 uses single-precision floating
#       point values for all numerical constants, while Case 2 uses single-
#       precision for both constants and variables. The program takes each
#       radius and uses forward finite differences to calculate the velocity
#       of a water droplet of each radius at a time of 0.0002 seconds, using a
#       time step of 1e-7. The program then calculates the kinetic energy of
#       liquid water drops in standard atmospheric conditions, and then
#       calculates the relative error compared to the double-precision values.
#       The relative errors are then plotted on a single plot.
#       
#
# Syntax:
#   python round_off.py
#
#   Input: None
#
#   Output: File containing the diameters in micrometers, and the two kinetic
#           energies, one for standard atmospheric conditions and one with an
#           additional electric field.
#
# Execution Example:
#   Linux example: python round_off.py
#
# Modification History:
#   2017/09/10 - Lance Wilson:  Created from fall_velocity.py.
#
# Verification of Data:   
#
# Copyright 2017 Lance Wilson

import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Constants for the "true" values are double precision.
rho_w_true = 999.102     # Density of water (kg/m^3).
eta_true = 1.812e-5      # Dynamic Viscosity of Air (kg/(m*s)).
g_true = 9.810           # Acceleration due to gravity (m/s^2).
q_true = 1.60217646e-19  # Charge of proton (coulombs).

# Constants for the two cases are single precision.
rho_w = np.float32(999.102)     # Density of water (kg/m^3).
eta = np.float32(1.812e-5)      # Dynamic Viscosity of Air (kg/(m*s)).
g = np.float32(9.810)           # Acceleration due to gravity (m/s^2).
q = np.float32(1.60217646e-19)  # Charge of proton (coulombs).
###E = np.float32(3e6)             # Atmospheric electric field "breakdown" threshold (V/m).
pi = np.float32(math.pi)        # One significant figure of pi

# Radius of water droplet in units of meters.
radii_true = np.array([1.0e-6, 1.5e-6, 2.0e-6, 2.5e-6, 3.0e-6, 4.0e-6, 5.0e-6])
radii_case2 = np.float32(radii_true)

# "True" time interval.
time_step_true = 1e-7
# Time interval in seconds, Case 1 and 2.
time_step = np.float32(1e-7)
# "True" value of Kinetic Energy (Joules).
KE_true = np.empty(len(radii_true))
# Kinetic Energy for Case 1 (single-precision constant, double-precision 
#   variable) (Joules).
KE1 = np.empty(len(radii_true))
# Kinetic Energy, Case 2 (single-precision variable and constants) (Joules).
KE2 = np.float32(np.empty(len(radii_true)))
# Array of "true" values of final velocities.
v_final_true = np.empty(len(radii_true))
# List of the final velocities for Case 1, single-precision constant (m/s).
v_final1 = np.empty(len(radii_true))
# Final velocity for Case 2.
v_final2 = np.float32(np.empty(len(radii_true)))
# Relative Error for Case 1.
rel_error1 = np.empty(len(radii_true))
# Relative Error for Case 2.
rel_error2 = np.empty(len(radii_true))

# File output containing the relative errors for both cases. 
outfile = open('round_off.out', 'w')

# Loop for standard atmospheric conditions.
for x in range(0, len(radii_true)):
    # Initial Velocity, "true" value (m/s).
    v_initial_true = 0.0
    # Initial Velocity, case 1, double precision with single precision
    #   constants (m/s).
    v_initial1 = 0.0
    # Initial Velocity, case2, single precision constants and variables (m/s).
    v_initial2 = np.float32(0.0)

    t_initial_true = 0.0
    t_initial1 = 0.0
    t_initial2 = np.float32(0.0)

    # mass = density * volume (units: kg)
    mass_true = rho_w_true*(4.0/3.0)*math.pi*math.pow((radii_true[x]),3)
    mass1 = rho_w*(4.0/3.0)*pi*math.pow((radii_true[x]),3)
    mass2 = np.float32(rho_w*(4.0/3.0)*pi*math.pow((radii_case2[x]),3))

    # The equation to calculate dv is a calculation of the acceleration of the
    #   water droplet, with increments of velocity calculated at intervals
    #   of 1e-7 seconds. The equation is derived from Newton's First Law,
    #   where F/m = dv/dt.  The sum of forces in this case is gravitational
    #   force, drag force, and the force induced by the electric field,
    #   with gravity and the electric field forces pointed downward and
    #   the drag force resisting their motion.

    # For "true" case where all numbers are double precision.
    while (t_initial_true <= 0.0002):
        true_dv = (g_true - 6*math.pi*eta_true*radii_true[x]*v_initial_true/mass_true)*time_step_true

        # As the code iterates through the loop, the increment of velocity is
        #   accumulated onto the initial velocity, with each new velocity
        #   being used to calculate the increment at the next step.
        v_initial_true += true_dv
        t_initial_true += time_step_true

    # For Case 1, where constants are single precision.
    while (t_initial1 <= 0.0002):
        dv1 = (g - 6*pi*eta*radii_true[x]*v_initial1/mass1)*time_step

        # As the code iterates through the loop, the increment of velocity is
        #   accumulated onto the initial velocity, with each new velocity
        #   being used to calculate the increment at the next step.
        v_initial1 += dv1
        t_initial1 += time_step

    # For case 2, where both variables and constants are single-precision.
    while (t_initial2 <= 0.0002):
        dv2 = np.float32((g - 6*pi*eta*radii_case2[x]*v_initial2/mass2)*time_step)

        # As the code iterates through the loop, the increment of velocity is
        #   accumulated onto the initial velocity, with each new velocity
        #   being used to calculate the increment at the next step.
        v_initial2 = np.float32(v_initial2 + dv2)
        t_initial2 = np.float32(t_initial2 + time_step)

    v_final_true[x] = v_initial_true
    v_final1[x] = v_initial1
    v_final2[x] = v_initial2

    KE_true[x] = 0.5 * mass_true * math.pow(v_initial_true,2)
    KE1[x] = 0.5 * mass1 * math.pow(v_initial1,2)
    KE2[x] = np.float32(0.5 * mass2 * math.pow(v_initial2,2))

    rel_error1[x] = math.fabs((KE1[x] - KE_true[x]))/math.fabs(KE_true[x])
    rel_error2[x] = math.fabs((KE2[x] - KE_true[x]))/math.fabs(KE_true[x])

outfile.write('Radius (um)\t\tRelative Error Case 1\tRelative Error Case 2\n')
# Create a string to output a whole line to the file, containing the
#   radius, the relative error when just constants have single-precision, and
#   the relative error when both constants and variables have double-precision.
for x in range(len(rel_error1)):
    string_var = str(radii_true[x]) + '\t\t\t' + str(rel_error1[x]) + '\t\t' + str(rel_error2[x]) + '\n'
    outfile.write(string_var)

outfile.close()

# Final plot containing the comparison of the two kinetic energies as the
#   radius of the water droplets increases.
plt.plot((radii_true*1e6), rel_error1, label='Single Precision Constants')
plt.plot((radii_true*1e6), rel_error2, label='Single Precision Constants and Variables')
plt.yscale('log')
plt.title('Variation of Relative Error with Diameter of\nWater Drops Falling From Rest for 0.0002 seconds')
plt.xlabel('Diameter (um)')
plt.ylabel('Relative Error')
plt.legend(loc='best')
plt.savefig('round_off.png', dpi=400)
