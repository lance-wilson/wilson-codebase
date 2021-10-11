#!/usr/bin/env python
#
# Name:
#   quadraticinterpolation.py
#
# Purpose:
#   The purpose of this program is to find the maximum value of the function
#       f(x) = -x^4-2x^3-6x^2-4x using the quadratic interpolation method. The
#       quadratic interpolation method uses three initial guesses and a formula
#       to approximate the maximum value of the function. Recalculating this
#       function over multiple iterations will cause the result to slowly
#       converge on the correct value.
#
# Syntax:
#   python quadraticinterpolation.py
#
#   Input: None.
#
#   Output: Maximum of the function -x^4-2x^3-6x^2-4x.
#
# Execution Example:
#   Linux example: python quadraticinterpolation.py
#
# Modification History:
#   2017/10/15 - Lance Wilson:  Created.
#
# Verification of Data:
#   Test case of f(x) = 2*sin(x)-(x^3)/69
#   Initial Guesses: x0 = 0, x1 = 1, x2 = 2.5
#   Value at initial guess: fx0 = 0, fx1 = 1.669, fx2 = 0.970
#   First iteration: x3 = 1.477, fx3 = 1.945
#   Second iteration: x0 = x1_old, x1 = x3_old, x2 = x2
#                     fx0 = 1.668, fx1 = 1.945, fx2 = 0.970
#                     x3 = 1.522, fx3 = 1.947
#   Third iteration: x0 = 1.0, x1 = x1, x2 = x3_old
#                    fx0 = 1.668, fx1 = 1.945, fx2 = 1.947
#                    x3 = 1.521, fx3 = 1.947
#   Fourth iteration: x0 = x1_old, x1 = x3_old, x2 = x2
#                     fx0 = 1.945, fx1 = 1.947, fx2 = 1.947
#                     x3 = 1.521, fx3 = 1.947
#
# Copyright 2017 Lance Wilson

import math
import numpy as np
import sys

def help_message():
    print 'Syntax/Example: python quadraticinterpolation.py'

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):

        help_message()
        exit()

# Equation:
#       f(x) = -x^4 - 2*x^3 - 6*x^2 - 4*x
def function(x):
    return -1.0*math.pow(x,4) - 2.0*math.pow(x,3) - 6.0*math.pow(x,2) - 4.0*x

# Initial guesses
x0 = 1.5
x1 = 2.0
x2 = 3.0
iterations = 0
relative_error = 1.0
previous_value = x1

# Perform calculations of the maximum value until the relative error
#   is less than 0.1 percent.
while (relative_error > 0.001):
    fx0 = function(x0)
    fx1 = function(x1)
    fx2 = function(x2)

    # The unwieldy formula of approximating the location of the maximum:
    # x3 = (fx0(x1^2-x2^2)+fx1(x2^2-x0^2)+fx2(x0^2-x1^2))/
    #      (2fx0(x1-x2)+2fx1(x2-x0)+2fx2(x0-x1))
    x3 = (function(x0)*(math.pow(x1,2) - math.pow(x2,2)) + \
          function(x1)*(math.pow(x2,2) - math.pow(x0,2)) + \
          function(x2)*(math.pow(x0,2) - math.pow(x1,2)))/\
          (2.0*function(x0)*(x1 - x2) + 2.0*function(x1)*(x2 - x0)\
          + 2.0*function(x2)*(x0 - x1))

    fx3 = function(x3)

    # Relative Error = absolute value(true - approximation)/abs(true)
    relative_error = abs(previous_value-x3)/abs(previous_value)
    # Reset the previous value for the next iteration.
    previous_value = x3
    iterations += 1

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # If fx0 is the lowest value, we can cut that point out of the next
    #   iteration. Generically, the algorithm for reassigning values is to set
    #   the lowest value (x0 in this case) equal to the minimum of the
    #   remaining values, and if the new value is equal to x3, move on to the
    #   next iteration; if not, repeat for the next lowest value (in this case
    #   x1, and then x2).
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if (min(fx0,fx1,fx2,fx3) == fx0):
        # The new lower bound will be the smallest of the remaining points
        #   (x2 is not included because it will not be less than x1).
        x0 = min(x1,x3)
        # If the new lower bound is x3, then x1 will be in between the new
        #   lower bound and the old upper bound, so x1 and x2 (upper bound)
        #   can remain the same. Otherwise further calculations are needed.
        if (x0 == x1):
            # If the new lower bound is x1, x3 is greater than x1, which means
            #   we must entertain the thought that x3 might be larger than x2,
            #   and therefore the new x1 will be the smaller of the x2 and x3.
            x1 = min(x2,x3)
            # If the new x1 is the old x3, then x2 is the largest value and
            #   remains unchanged; otherwise, x3 is the largest and becomes
            #   the new upper bound.
            if (x1 == x2):
                x2 = x3

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # This is a check to affirm that everything is running correctly. If we are
    #   finding the maximum, then the function should be concave down, and thus
    #   there will usually (depending on the initial guesses and the behavior
    #   of the function) only be one maximum within the interval, so f(x1)
    #   should never be the minimum of the function.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if (min(fx0,fx1,fx2,fx3) == fx1):
        print 'If everything works right this should never happen.'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # If fx2 is the lowest value, then we can cut that point out of the next
    #   iteration. Generically, the algorithm for reassigning values is to set
    #   the highest value (x2 in this case) equal to the maximum of the
    #   remaining values, and if the new value is equal to x3, move on to the
    #   next iteration; if not, repeat for the next highest value (in this case
    #   x1, and then x0).
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if (min(fx0,fx1,fx2,fx3) == fx2):
        # The new upper bound will be the largest of the remaining points
        #   (x0 is not included because it will not be greater than x1).
        x2 = max(x1,x3)
        # If the new upper bound is x3, then x1 will be between the old lower
        #   bound and the new upper bound, so x0 (lower bound) and x1 can
        #   remain the same. Otherwise further calculations are needed.
        if (x2 == x1):
            # If the new upper bound is x1, x3 is less than x1, which means we
            #   must entertain the thought that x3 might be smaller than x0,
            #   and therefore the new x1 will be the larger of x0 and x3.
            x1 = max(x0,x3)
            # If the new x1 is the old x3, then x0 is the smallest value and
            #   remains unchanged; otherwise, x3 is the smallest and becomes
            #   the new lower bound.
            if (x1 == x0):
                x0 = x3

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # This is a check to make affirm that everything is running correctly. If
    #   we're finding the maximum value of the function, f(x3) should be our
    #   approximation for the maximum of the function, so it should never be a
    #   minimum.
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    if (min(fx0,fx1,fx2,fx3) == fx3):
        print 'This should also never happen as long as we\'re finding the max'

print 'The maximum value of the function occurs at %1.4f' % x3
print 'The maximum value at this point is %1.4f' % fx3
print 'The number of iterations was %d.' % iterations
