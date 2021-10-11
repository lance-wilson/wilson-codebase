#!/usr/bin/env python
#
# Name:
#   newton.py
#
# Purpose:
#   The purpose of this program is to calculate the maximum value of the
#       function f(x) = -x^4-2x^3-6x^2-4x using Newton's method. Newton's
#       method requires just one initial guess, but does not guarantee
#       convergence of the solution. If the method converges for a given
#       function at a given point, then iterating the method multiple times
#       will result in convergence on the correct answer.
#
# Syntax:
#   python newton.py
#
#   Input: None.
#
#   Output: Maximum of the function -x^4-2x^3-6x^2-4x.
#
# Execution Example:
#   Linux example: python newton.py
#
# Modification History:
#   2017/10/15 - Lance Wilson:  Created.
#
# Verification of Data:
#   Test case of f(x)   = 2*sin(x)-(x^3)/69
#                f'(x)  = 2*cos(x)-(x^2)/23
#                f''(x) = -2*sin(x)-2x/23
#   Initial Guesses: xi = 2.0
#   First iteration: xi+1 = 1.495
#   Second iteration: xi+1 = 1.521
#   Third iteration: x1+1 = 1.521
#
# Copyright 2017 Lance Wilson

import math
import numpy as np
import sys

def help_message():
    print 'Syntax/Example: python newton.py'

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

# Equation:
#       f(x) = -x^4 - 2*x^3 - 6*x^2 - 4*x
def function(x):
    return abs(x - 2.0 * np.sin(x/2.))

# First Derivative: f'(x) = -4*x^3 - 6*x^2 - 12*x - 4
def first_deriv(x):
    return abs(1. - np.cos(x/2.))

# Second Derivative: f''(x) = -12*x^2 - 12*x - 12
def second_deriv(x):
    return abs(0.5 * np.sin(x/2.))

# Initial Guess
xi = 3.0
iterations = 0
relative_error = 1

while (relative_error > 0.1):
    # Equation for Newton's Method:
    #   x_i+1 = x_i - f'(x_i)/f''(x_i)
    x_next = xi - first_deriv(xi)/second_deriv(xi)

    # Relative Error = absolute value(true - approximation)/abs(true)
    relative_error = (xi - x_next)/xi
    iterations += 1
    # Reset the previous value for the next iteration.
    xi = x_next

    if iterations > 10000:
        break

print 'The maximum value of the function occurs at %1.4f' % xi
print 'The maximum value at this point is %1.4f' % function(xi)
print 'The number of iterations was %d.' % iterations

