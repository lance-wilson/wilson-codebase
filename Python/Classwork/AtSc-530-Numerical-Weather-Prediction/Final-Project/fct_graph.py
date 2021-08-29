#!/usr/bin/env python3
#
# Name:
#   fct_graph.py
#
# Purpose:
#   To reproduce figure 5.10 in the Dale Durran book Numerical Methods for Wave
#   Equations in Geophysical Fluid Dynamics, which shows the compared accuracy
#   of the upstream scheme, Lax-Wendroff scheme, and the combined Zalesak
#   flux-corrected transport for a travelling jump problem and for the sum of
#   two sine waves with wavelengths 7.5dx and 10dx.
#
# Syntax:
#   python3 fct_graph.py solution_option
#
#   Input: None.
#
#   Output: A plot containing the comparisons between the exact solution, the
#           upstream scheme, the Lax-Wendroff scheme, and the Zalesak algorithm
#           flux-corrected transport approximations.  Figures a and b are
#           produced separately based on the command-line argument.
#
# Modification History:
#   2019/03/26 - Lance Wilson:  Created.

import math
import matplotlib.pyplot as plt
import numpy as np
import sys

def help_message():
    print('Syntax:  python3 fct_graph.py solution_option')
    print('         Solution Options:  a, b')
    exit()

def u_exact_a(x_range, current_time):
    return [1.0 for x in x_range if x < c * current_time] + [0.0 for x in x_range if x >= c * current_time]

def u_exact_b(x_range, current_time):
    return np.sin((2.*math.pi/(7.5*x_step)) * (x_range - c*current_time)) + np.sin((2.*math.pi/(10.*x_step)) * (x_range - c*current_time))

def u_exact_c(x_range, current_time):
    return np.power(np.sin(x_range - c*current_time), 6)

mu = 0.5  # Defined by Durran
c = 0.3   # m/s (estimated from ~0.6 m / 1.8 s)
x_step = 0.02   # meters
x_min = -3.0
x_max = 4.0
grid_intervals = int((x_max - x_min)/x_step)
x_range = np.linspace(x_min, x_max, num=grid_intervals+1)
time_step = mu * x_step/c   # Seconds

if len(sys.argv) > 1:
    for param in sys.argv:
        if param == 'a' or param == 'A':
            solution = 'a'
            # Criteria for stopping the while loop in time.
            time_limit = 1.8
            u_exact = u_exact_a(x_range, 0.)
        elif param == 'b' or param == 'B':
            solution = 'b'
            # Criteria for stopping the while loop in time.
            time_limit = 24*time_step
            u_exact = u_exact_b(x_range, 0.)
        elif param == 'c' or param == 'C':
            solution = 'c'
            time_limit = 1.8
            u_exact = u_exact_c(x_range, 0.)
else:
    help_message()

# Initializations and array declarations.
u_up = np.zeros(len(x_range))
u_up_old = u_exact

u_lw = np.zeros(len(x_range))
u_lw_old = u_exact

u_fct = np.zeros(len(x_range))
u_fct_old = u_exact

u_td = np.zeros(len(x_range))

low_flux_plus = np.zeros(len(x_range))
low_flux_minus = np.zeros(len(x_range))
high_flux_plus = np.zeros(len(x_range))
high_flux_minus = np.zeros(len(x_range))
antiflux_plus = np.zeros(len(x_range))
antiflux_minus = np.zeros(len(x_range))
r_plus = np.zeros(len(x_range))
r_minus = np.zeros(len(x_range))

##up_flux_plus = np.zeros(len(x_range))
##up_flux_minus = np.zeros(len(x_range))
##lax_flux_plus = np.zeros(len(x_range))
##lax_flux_minus = np.zeros(len(x_range))

current_time = 0.

# Loop for travelling jump problem.
while (current_time <= time_limit):
    current_time += time_step
    # Exact Solution
    if solution == 'a':
        u_exact = u_exact_a(x_range, current_time)
    elif solution == 'b':
        u_exact = u_exact_b(x_range, current_time)
    elif solution == 'c':
        u_exact = u_exact_c(x_range, current_time)

    for j in range(0,grid_intervals):
        # Upstream Difference.
        u_up[j] = u_up_old[j] - mu * (u_up_old[j] - u_up_old[j-1])
        # Lax-Wendroff.
        u_lw[j] = u_lw_old[j] - 0.5*mu*(u_lw_old[j+1] - u_lw_old[j-1]) + 0.5*(mu**2)*(u_lw_old[j+1] - 2.0*u_lw_old[j] + u_lw_old[j-1])

        # Flux Corrected Transport, following procedure in Durran book 5.4.
        # F^l_j+1/2
        low_flux_plus[j] = 0.5*c*(u_fct_old[j] + u_fct_old[j+1]) - 0.5*abs(c)*(u_fct_old[j+1] - u_fct_old[j])
        # F^l_j-1/2
        low_flux_minus[j] = 0.5*c*(u_fct_old[j-1] + u_fct_old[j]) - 0.5*abs(c)*(u_fct_old[j] - u_fct_old[j-1])

        # F^h_j+1/2
        high_flux_plus[j] = 0.5*c*(u_fct_old[j] + u_fct_old[j+1]) - 0.5*(c**2)*(time_step/x_step)*(u_fct_old[j+1] - u_fct_old[j])
        # F^h_j-1/2
        high_flux_minus[j] = 0.5*c*(u_fct_old[j-1] + u_fct_old[j]) - 0.5*(c**2)*(time_step/x_step)*(u_fct_old[j] - u_fct_old[j-1])

        ##up_flux_plus[j] = 0.5*c*(u_up_old[j] + u_up_old[j+1]) - 0.5*abs(c)*(u_up_old[j+1] - u_up_old[j])
        ##up_flux_minus[j] = 0.5*c*(u_up_old[j-1] + u_up_old[j]) - 0.5*abs(c)*(u_up_old[j] - u_up_old[j-1])
        ##lax_flux_plus[j] = 0.5*c*(u_lw_old[j] + u_lw_old[j+1]) - 0.5*(c**2)*(time_step/x_step)*(u_lw_old[j+1] - u_lw_old[j])
        ##lax_flux_minus[j] = 0.5*c*(u_lw_old[j-1] + u_lw_old[j]) - 0.5*(c**2)*(time_step/x_step)*(u_lw_old[j] - u_lw_old[j-1])

        ##u_up[j] = u_up_old[j] - (time_step/x_step)*(up_flux_plus[j] - up_flux_minus[j])
        ##u_lw[j] = u_lw_old[j] - (time_step/x_step)*(lax_flux_plus[j] - lax_flux_minus[j])

        # Antidiffusive fluxes
        antiflux_plus[j] = high_flux_plus[j] - low_flux_plus[j]
        antiflux_minus[j] = high_flux_minus[j] - low_flux_minus[j]

        # Transported and diffused solution (monotone estimate).
        u_td[j] = u_fct_old[j] - (time_step/x_step)*(low_flux_plus[j] - low_flux_minus[j])

    # Second loop so that the preliminary step can be done with the full set
    #   of u_td values.
    for j in range(0,grid_intervals):
        # --------------------------------------------------------------------
        # Calculate correction coefficient using Zalesak Corrector algorithm.
        # Procedure can be found in the Durran book, section 5.4.2.
        # --------------------------------------------------------------------

        # Preliminary step ("cosmetic correction").
        if j < grid_intervals-1:
            term_a = antiflux_plus[j] * (u_td[j+1] - u_td[j])
            term_b = antiflux_plus[j] * (u_td[j+2] - u_td[j+1])
            term_c = antiflux_plus[j] * (u_td[j] - u_td[j-1])
            term_d = antiflux_minus[j] * (u_td[j] - u_td[j-1])
            term_e = antiflux_minus[j] * (u_td[j+1] - u_td[j])
            term_f = antiflux_minus[j] * (u_td[j-1] - u_td[j-2])

            if term_a < 0 and (term_b < 0 or term_c < 0):
                antiflux_plus[j] = 0

            if term_d < 0 and (term_e < 0 or term_f < 0):
                antiflux_minus[j] = 0

        # Permissible values for u[j][n+1].
        u_max = max(u_fct[j-1], u_fct[j], u_fct[j+1], u_td[j-1], u_td[j], u_td[j+1])
        u_min = min(u_fct[j-1], u_fct[j], u_fct[j+1], u_td[j-1], u_td[j], u_td[j+1])

        # Sum of all antidiffusive fluxes into grid point j.
        p_plus = max(0, antiflux_minus[j]) - min(0, antiflux_plus[j])

        # Maximum net antidiffusive flux that will preserve u[j][n+1] <= u[j]_max.
        q_plus = (u_max - u_td[j])*(x_step/time_step)

        # Required limitation on the net antidiffuxive flux into grid point j.
        if (p_plus == 0):
            r_plus[j] = 0
        elif (p_plus > 0):
            r_plus[j] = min(1, (q_plus/p_plus))

        # Sum of all antidiffusive fluxes out of grid point j.
        p_minus = max(0, antiflux_plus[j]) - min(0, antiflux_minus[j])

        # Minimum net antidiffusive flux that will preserve u[j][n+1] >= u[j]_min.
        q_minus = (u_td[j] - u_min)*(x_step/time_step)

        # Required limitation on the net antidiffuxive flux out of grid point j.
        if (p_minus == 0):
            r_minus[j] = 0
        elif (p_minus > 0):
            r_minus[j] = min(1, (q_minus/p_minus))

    # Third loop since all R values must be calculated before calculating C+/-1/2.
    for j in range(0,grid_intervals):
        # Limit antidiffusive flux so that it doesn't generate an overshoot
        #   into the grid cell or an undershoot out of it.
        if (antiflux_plus[j] >= 0):
            cor_plus = min(r_plus[j+1], r_minus[j])
        else:
            cor_plus = min(r_plus[j], r_minus[j+1])

        if (antiflux_minus[j] >= 0):
            cor_minus = min(r_plus[j], r_minus[j-1])
        else:
            cor_minus = min(r_plus[j-1], r_minus[j])

        # Corrected antidiffusive fluxes
        antiflux_plus_corrected = cor_plus * antiflux_plus[j]
        antiflux_minus_corrected = cor_minus * antiflux_minus[j]

        # Perform the antidiffusion.
        u_fct[j] = u_fct_old[j] - (time_step/x_step)*(low_flux_plus[j] - low_flux_minus[j]) - (time_step/x_step)*(antiflux_plus_corrected - antiflux_minus_corrected)

    # Copy values into old areas for next time step.
    u_up_old = np.copy(u_up)
    u_lw_old = np.copy(u_lw)
    u_fct_old = np.copy(u_fct)

# Main plot components
plt.plot(x_range, u_exact, color='b', label='Exact')
plt.plot(x_range, u_up, color='firebrick', label='Upstream')
plt.plot(x_range, u_lw, color='indigo', label='Lax-Wendroff')
plt.plot(x_range, u_fct, color='green', label='FCT')
plt.xlabel('X (m)')
plt.ylabel('U (m s$^-1$)')
plt.legend(loc='upper right')
# Specific to solution a
if solution == 'a':
    plt.xlim(0,1.0)
    plt.title('Travelling Jump Discontinuity')
    plt.savefig('TravellingJump.png', dpi=400)
# Specific to solution b
elif solution == 'b':
    plt.xticks([0, 5.*x_step, 10.*x_step, 15.*x_step, 20.*x_step, 25.*x_step, 30.*x_step],\
        ['$0$', r'5.0$\Delta$x', r'10.0$\Delta$x', r'15.0$\Delta$x', r'20.0$\Delta$x', r'25.0$\Delta$x', r'30.0$\Delta$x'])
    plt.xlim(0,30.*x_step)
    plt.title('Sum of 7.5$\Delta$x and 10.0$\Delta$x Sine Waves')
    plt.savefig('SineSum.png', dpi=400)
# Specific to solution c
elif solution == 'c':
    plt.xlim(0, 4.*math.pi)
    # Set x tick marks to be in terms of pi.
    plt.xticks([0, math.pi, 2.0*math.pi, 3.0*math.pi, 4.0*math.pi],\
        ['$0$', r'$\mathregular{\pi}$', r'$2\mathregular{\pi}$', r'$3\mathregular{\pi}$', r'$4\mathregular{\pi}$'])
    plt.title('Sine Power')
    plt.savefig('SinePower.png', dpi=400)

