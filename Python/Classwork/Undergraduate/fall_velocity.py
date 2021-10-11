#!/usr/bin/env python
#
# Name:
#   fall_velocity.py
#
# Purpose:
#   To calculate the kinetic energy of liquid water drops in standard
#       atmospheric conditions and in the presence of an electric field,
#       and plot the variation of kinetic energy with droplet radius.
#       The program takes each radius and uses forward finite differences to
#       calculate the velocity of a water droplet of each radius at a time of
#       0.0002 seconds, using a time step of 1e-7.  Both the standard velocity
#       and the velocity in the presence of an electric field are calculated
#       at the same time.  The final velocities and kinetic energies are then
#       outputed to a file. The Kinetic Energies are then added to lists so
#       they can be graphed.
#
# Syntax:
#   python fall_velocity.py
#
#   Input: None
#
#   Output: File containing the diameters in micrometers, and the two kinetic
#           energies, one for standard atmospheric conditions and one with an
#           additional electric field.
#
# Execution Example:
#   Linux example: python fall_velocity.py
#
# Modification History:
#   2017/08/28 - Lance Wilson:  Created.
#   2017/08/29 - Lance Wilson:  Added loop over radius and time.
#   2017/08/30 - Lance Wilson:  Added the second case, and graphing.
#   2017/09/01 - Lance Wilson:  Added comments.
#   2017/09/06 - Lance Wilson:  Added comments.
#
# Verification of Data:   
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np

# Constants
rho_w = 999.102     # Density of water (kg/m^3).
eta = 1.812e-5      # Dynamic Viscosity of Air (kg/(m*s)).
g = 9.810           # Acceleration due to gravity (m/s^2).
q = 1.60217646e-19  # Charge of proton (coulombs).
E = 3e6             # Atmospheric electric field "breakdown" threshold (V/m).

# Radius of water droplet in units of meters.
radii = np.array([1.0e-6, 1.5e-6, 2.0e-6, 2.5e-6, 3.0e-6, 4.0e-6, 5.0e-6])

# Time interval in seconds.
time_step = 1e-7
# Kinetic Energy for Case 1 (standard atmospheric conditions, no Electric
#   Field) (Joules).
KE1 = []
# Kinetic Energy, Case 2 (Additional Electric Field) (Joules).
KE2 = []
# List of the final velocities for Case 1 (m/s).
v_final1 = []
# Final velocity for Case 2.
v_final2 = []

# File output containing the Diameter of each drop and the kinetic energies
#   in Joules in both standard atmospheric conditions and with an added
#   electric field in the direction of the gravitational force. 
outfile = open('fall_velocity.out', 'w')

# Loop for standard atmospheric conditions.
for radius in radii:
    # Initial Velocity (m/s)
    v_initial1 = 0.0
    v_initial2 = 0.0
    t_initial = 0.0
    # mass = density * volume (units: kg)
    m = rho_w*(4.0/3.0)*math.pi*math.pow((radius),3)

    outfile.write('For radius ' + str(radius*1e6) + ' um:\n')
    outfile.write('Time step    Velocity (standard)    Velocity (Electric Field)\n')

    while (t_initial <= 0.0002):
        # The following equation is a calculation of the acceleration of the
        #   water droplet, with increments of velocity calculated at intervals
        #   of 1e-7 seconds. The equation is derived from Newton's First Law,
        #   where F/m = dv/dt.  The sum of forces in this case is gravitational
        #   force, drag force, and the force induced by the electric field,
        #   with gravity and the electric field forces pointed downward and
        #   the drag force resisting their motion.
        # For first case where Electric field is omitted.
        dv1 = (g - 6*math.pi*eta*radius*v_initial1/m)*time_step
        # For second case when an electric field exists.
        dv2 = (g + q*E/m - 6*math.pi*eta*radius*v_initial2/m)*time_step

        # Create a string to output a whole line to the file, containing the
        #   time, the velocity in standard conditions (in meters/second), and
        #   the velocity with the addition of an electric field (m/s).
        string_var = str(t_initial) + '    ' + str(v_initial1) + '    ' + str(v_initial2) + '\n'
        outfile.write(string_var)

        # As the code iterates through the loop, the increment of velocity is
        #   accumulated onto the initial velocity, with each knew velocity
        #   being used to calculate the increment at the next step.
        v_initial1 += dv1
        v_initial2 += dv2

        t_initial += time_step

    v_final1.append(v_initial1)
    v_final2.append(v_initial2)
    KE1.append(0.5 * m * math.pow(v_initial1,2))
    KE2.append(0.5 * m * math.pow(v_initial2,2))

outfile.close()

# Final plot containing the comparison of the two kinetic energies as the
#   radius of the water droplets increases.
plt.plot((radii*1e6), KE1, label='Standard ATM Conditions')
plt.plot((radii*1e6), KE2, label='Additional Electric Field')
plt.yscale('log')
plt.title('Variation of Kinetic Energy with Diameter of\nWater Drops Falling From Rest for 0.0002 seconds')
plt.xlabel('Diameter (um)')
plt.ylabel('Kinetic Energy (J)')
plt.legend(loc='best')
plt.savefig('fall_velocity.png', dpi=400)
