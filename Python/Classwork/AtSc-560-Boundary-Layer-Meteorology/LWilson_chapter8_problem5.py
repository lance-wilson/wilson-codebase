#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   LWilson_chapter8_problem5.py
#
# Purpose:
#   Calculate the exact autocorrelation and structure function of vertical
#   velocity and temperature data in Chapter 8, Problem 5, of "An Introduction
#   to Boundary Layer Meteorology" by Roland B. Stull.
#
# Syntax:
#   python3 LWilson_chapter8_problem5.py
#
# Modification History:
#   2020/05/05 - Lance Wilson:  Created.

import matplotlib.pyplot as plt
import numpy as np

def autocorrelation(measurements, N):
    auto_exact = np.empty(N)
    # Exact Method: Equation 8.2.1a
    for j in range(len(measurements)):
        a_k_bar = np.sum(measurements[:N-j])/(N-j)
        a_kj_bar = np.sum(measurements[j:N])/(N-j)
        k_diff = measurements[:N-j] - a_k_bar
        kj_diff = measurements[j:N] - a_kj_bar
        numerator = np.sum(k_diff * kj_diff[:N-j])
        denom1 = np.sqrt(np.sum(k_diff**2))
        denom2 = np.sqrt(np.sum(kj_diff**2))
        auto_exact[j] = numerator/(denom1 * denom2)

    return auto_exact

def structure_fn(measurements, N):
    structure_fn = np.empty(N)
    # Equation 8.3.1a
    for j in range(N):
        structure_fn[j] = np.sum((measurements[:N-j] - measurements[j:N])**2)/(N-j)
    return structure_fn

# Plot the original data with either the autocorrelation or structure function.
def plot_auto_struct(time, original, stat_data, y_label, plot_title, file_label):
    fig = plt.figure()

    fig.add_subplot(211)
    plt.plot(time, original)
    plt.xlabel('Time (s)')
    plt.ylabel(y_label)
    plt.title('Original Data')

    fig.add_subplot(212)
    plt.plot(time, stat_data)
    plt.xlabel('Lag (s)')
    plt.ylabel(y_label)
    plt.title(plot_title)

    fig.tight_layout()
    #plt.show()
    plt.savefig('LWilson_ch8_5_{:s}.png'.format(file_label), dpi=400)

time = np.arange(0, 210, 10)
# Temperature (degrees C)
temperature = np.array([25., 23., 21., 21., 30., 20., 24., 23., 23., 24, 23., 20., 19., 20., 25., 21., 25., 23., 21., 20., 19.])
# Vertical Velocity (m/s)
w = np.array([2., 2., -1., 1., 4., -3., 3., 1., 2., 3., -1., -4., -1., 1., 3., 0., 1., 0., -2., -1., -2.])

NT = len(temperature)
Nw = len(w)

auto_exact_T = autocorrelation(temperature, NT)
auto_exact_w = autocorrelation(w, Nw)

structure_fn_T = structure_fn(temperature, NT)
structure_fn_w = structure_fn(w, Nw)

# Temperature Autocorrelation
plot_auto_struct(time, temperature, auto_exact_T, 'Temperature ($\degree$C)', 'Exact Autocorrelation', 'T_auto')
# Temperature Structure Function
plot_auto_struct(time, temperature, structure_fn_T, 'Temperature ($\degree$C)', 'Structure Function', 'T_struct')
# W Autocorrelation
plot_auto_struct(time, w, auto_exact_w, 'Vertical Velocity (m/s)', 'Exact Autocorrelation', 'w_auto')
# W Structure Function
plot_auto_struct(time, w, structure_fn_w, 'Vertical Velocity (m/s)', 'Exact Structure Function', 'w_struct')

