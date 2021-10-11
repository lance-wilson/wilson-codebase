#!/usr/bin/env python
#
# Name: chord_error.py
#
# Purpose:  Determine the range of degrees in which the chord approximation has
#           less than 10% error compared to the curved dx surface.
#

import numpy as np

# Radius of the Earth.
r = 6.371e6
# Approximate Grand Forks latitude, converted to radians.
# Note: since cos(phi) is a common term, latitude should not affect the results.
phi = np.radians(48)
# Array of angles to check.
angles = np.radians(np.arange(0,180,0.1))
max_angle = 0.0

for angle in angles:
    # Curved surface solution.
    ##arc = r * np.cos(phi) * angle
    arc = angle
    # Chord approximation.
    ##chord = 2. * r * np.cos(phi) * np.sin(0.5 * angle)
    chord = 2. * np.sin(0.5 * angle)

    # Will print out the maximum angle with less than 10% error.
    if arc - chord < 0.1 * arc:
        max_angle = angle

print('Maximum angle of less than 10% error: {:.1f} degrees'.format(np.degrees(max_angle)))


