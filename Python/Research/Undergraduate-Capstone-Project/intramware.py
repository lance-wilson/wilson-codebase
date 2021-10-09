#!/usr/bin/env python
#
# Name:
#   intramware.py (the INfluence on the atlantic TRopical cyclone season of the
#       AMo (Atlantic Multidecadal oscillation), West African Rainfall, and
#       Enso (the El nino-southern oscillation)
#
# Purpose:
#   The purpose of this program is to process data and assist in the
#   determination of the correlation between ENSO and AMO and West African
#   rainfall, as well as the correlation between the West African rainfall and
#   the tropical cyclone activity in the North Atlantic Ocean Basin. The
#   program calculates the average rainfall in June and July for each station
#   for each year and stores them in a dictionary. An adjusted total is
#   calculated based on how many days of data are available for each year. An
#   overall average of precipitation is then calculated. The Kraus method is
#   used to average the precipitation over the entire region without giving any
#   particular weight to means of wetter stations or large deviations from dry
#   stations. These values are then compared to the El Nino and AMO Phase over
#   the same time period, and to the number of tropical cyclones, hurricanes,
#   and intense hurricanes for each year. Correlations are plotted for several
#   of these variables, and the raw data is output to a text file.
#
# Syntax:
#   python intramware.py
#
#   Input: None.
#
#   Output: Summary.txt, a file which contains the normalized regional rainfall
#           index, the June-July and hurricane season phases of El Nino and the
#           AMO, and the number of tropical cyclones, hurricanes, and major
#           hurricanes for each year.
#
# Execution Example:
#   Linux example: python intramware.py
#
# Modification History:
#   Date         Editor         Version Modifications
#   2017/12/05 - Lance Wilson:  0.1     Created.
#   2017/12/08 - Lance Wilson:  0.1.1   Added importation of data.
#   2017/12/11 - Lance Wilson:  0.2     Completed importation of data.
#   2017/12/15 - Lance Wilson:  1.0     Added averages, standard deviations,
#                                       and the regional rainfall index
#   2017/12/16 - Lance Wilson:  1.1     Added El Nino, AMO, and HURDAT data,
#                                       added data output.
#   2017/12/17 - Lance Wilson:  1.2     Added graphing of results and
#                                       correlations in data output, comments.
#   2017/12/19 - Lance Wilson:  1.2     Added comments, updated the percentile
#                                       list calculations.
#   2018/03/17 - Lance Wilson:  1.2.1   Added a special dot for 2017 season,
#                                       removed best-fit lines for quartiles,
#                                       moved plot_correlation to separate
#                                       file, added correlations for number
#                                       of storm days.
#
# Plan for INTRAMWARE 2.0: convert the code to account for more generalized
#   situations (i.e. check for generalized common years rather than just
#   looping through the hurdat keys). Move the calculation of common years
#   to the plot_correlation function. Perhaps a few more tests of data.
#   Plot the average tropical cyclone activity.
#   Possible future work: pull the (nino,amo) data from a URL instead of downloaded data.
#   Potential adjustment for streamlining: put all of the data in the same dictionary (i.e. have one dictionary with years for keys, and then have all data (rainfall, named storms, enso phase, etc) as dictionaries within that key. (Would get rid of need for having common years, could potentially just skip years that are not in the first loaded dataset) (Could also set different levels of common years so that if El Nino and HURDAT have a greater number of common years than the other datasets, could get a more thorough correlation)
#
# Verification of Data:
#   Took abbreviated form of the Tambacounda, Senegal (1973, 1974, 1975, and through February 1976), and calculated the following values:
#           Precip  Points  Adjusted
#   1973:   8.25    45      11.18
#   1974:   7.02    44      9.73
#   1975:   0.00    41      0.00
#   1976:   0.00    0       0.00
#   Adjusted Average Precipitation:  5.23
#   Standard Deviation:  
#
#   Results from program:
#           Precip  Points  Adjusted
#   1973:   8.25    45      11.18
#   1974:   7.02    44      9.73
#   1975:   0.0     41      0.0
#   1976    0.0     0       0.0
#   Adjusted Average Precipitation:  5.23
#   Standard Deviation:  6.07
#
# Copyright 2017 Lance Wilson

import math
import matplotlib.pyplot as plt
import numpy as np
import os
##import re
from scipy import stats
import sys
from hurdat_test import storm_days
from plot_correlation import plot_correlation

def help_message():
    print 'Syntax/Example: python intramware.py'

# Check whether the user asked for the help message.
for x in range(0,len(sys.argv)):
    if (sys.argv[x].startswith('-h') or sys.argv[x].startswith('--help')):
        help_message()
        exit()

# Flash Drive
##datadir = 'Sites/'
# Laptop
datadir = 'Backup Data/Sites/'

filelist = sorted(os.listdir(('./' + datadir)))

if not filelist:
    print 'No files were found for' + datadir
    exit()

station_data = {}

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# For each file in the list of files in the data directory, the station name
#   will be acquired from the file, and the columns pertaining to the data and
#   the precipitation will be collected. The dates are then partitioned into
#   year, month, and day, and a dictionary is set up for each unique year so
#   that data can be accumulated. The non-missing data from the months of June
#   and July for each year are then accumulated, and an adjusted value is 
#   calculated, given by actual_precip * 61/number of days. The overall average
#   precipitation for the station and the standard deviation is calculated.
#   The normalized values for the station are then calculated and they, along
#   with the average precipitation and the standard deviation, are added to
#   the dictionary.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
for datafile in filelist:
    thisfile = open((datadir + datafile), 'r')

    station_name = datafile.split('.')[0]
    station_data[station_name] = {}

    # Read header line.
    header = thisfile.readline()

    dates, precip = np.loadtxt(thisfile, dtype=np.str,
                               usecols=(2,-3), unpack=True)

    thisfile.close()

    year = np.empty(len(dates), dtype="S4")
    month = np.empty(len(dates))
    day = np.empty(len(dates))

    for x in range(len(dates)):
        year[x] = dates[x][:4]
        month[x] = dates[x][4:6]
        day[x] = dates[x][6:]

    for unique_year in np.unique(year):
        station_data[station_name][unique_year] = {'precip':0.0, 'points':0}

    for z in range(len(year)):
        # Accumulate the data for June and July, except when a missing value.
        if ((month[z] == 6. or month[z] == 7.) and (precip[z] != '99.99')):
            station_data[station_name][year[z]]['precip'] += float(precip[z][:-1])
            station_data[station_name][year[z]]['points'] += 1
        if (station_data[station_name][year[z]]['points'] != 0):
            # Adjusted precip = actual precip * 61/number of data points
            station_data[station_name][year[z]]['adjusted_precip'] = (
                    61.0*station_data[station_name][year[z]]['precip']/
                    float(station_data[station_name][year[z]]['points']))
        else:
            station_data[station_name][year[z]]['adjusted_precip'] = 0.0

    average_precip = sum(station_data[station_name][year]['adjusted_precip']
                            for year in station_data[station_name])/float(
                            len(station_data[station_name]))
    stand_dev = math.sqrt(sum(math.pow(
        station_data[station_name][year]['adjusted_precip'] - average_precip,2)
        for year in station_data[station_name])/(len(
        station_data[station_name])-1))

    for year in station_data[station_name]:
        # normalized value = (period rainfall - mean)/standard deviation
        station_data[station_name][year]['normalized'] = (
            station_data[station_name][year]['adjusted_precip'] - 
            average_precip)/stand_dev

    station_data[station_name]['avg_precip'] = average_precip
    station_data[station_name]['stand_dev'] = stand_dev
# End of datafile loop.

regional_index = {}
min_year = '8020'
max_year = '0'

for station in station_data:
    keys = sorted(station_data[station].keys())
    if (keys[0] < min_year):
        min_year = keys[0]
    if (keys[-3] > max_year):
        max_year = keys[-3]

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Used the normalized rainfall indices for each station in each year to get the
#   regionally averaged rainfall index. This is in line with the Kraus method,
#   as presented in "The Strong Association between Western Sahelian Monsoon
#   Rainfall and Intense Atlantic Hurricanes", Section 3b, Landsea and Gray,
#   1991.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
for year in range(int(min_year), int(max_year)+1):
    total_norm = 0
    station_num = 0
    for station in station_data:
        if str(year) in station_data[station].keys():
            total_norm += station_data[station][str(year)]['normalized']
            station_num += 1
    if (station_num > 2):
        # Regional index = sum of the normalized values divided by the
        #   number of stations.
        regional_index[str(year)] = {'index':total_norm/station_num, 'station_num':station_num}
    # Version 1.2: for now, fill in the data points that don't exist so that
    #   the output to the data file is not compromised (but ignore the 1940's
    #   data since there is not El Nino and AMO data for all of the
    #   intervening years).
    if (str(year) not in regional_index.keys()) and (year > 1957):
        regional_index[str(year)] = {'index':99.9, 'station_num':0}

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get the three month averaged Nino-3.4 indices, find the means for the
#   June-July period (with a one month buffer on either side) and for the
#   June-November hurricane season (with the same buffer). The phase (warm,
#   cold, or neutral) is then determined for each period for each year.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ninofile = open('Backup Data/OceanicNinoIndex.txt', 'r')

nino_indices = {}
for line in ninofile:
    nino = line.split()
    # Only take valid lines from this type of file.
    if not line.startswith('Year'):
        nino_indices[nino[0]] = {'Indices':[float(i) for i in nino[1:]]}

ninofile.close()

for year in nino_indices:
    nino_indices[year]['JJMean'] = np.mean(nino_indices[year]['Indices'][4:8])
    nino_indices[year]['SeasonMean'] = np.mean(nino_indices[year]['Indices'][4:])

    # Phases for June-July.
    if (nino_indices[year]['JJMean'] >= 0.5):
        nino_indices[year]['JJPhase'] = 'Warm'
    elif (nino_indices[year]['JJMean'] <= -0.5):
        nino_indices[year]['JJPhase'] = 'Cold'
    else:
        nino_indices[year]['JJPhase'] = 'Ntrl'

    # Phases for hurricane season.
    if (nino_indices[year]['SeasonMean'] >= 0.5):
        nino_indices[year]['SeasonPhase'] = 'Warm'
    elif (nino_indices[year]['SeasonMean'] <= -0.5):
        nino_indices[year]['SeasonPhase'] = 'Cold'
    else:
        nino_indices[year]['SeasonPhase'] = 'Ntrl'

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Get the departure from average temperatures for the North Atlantic Ocean, and
#   find the means for the June-July period (with a one month buffer on either
#   side) and for the June-November hurricane season (with the same buffer).
#   The phase (warm or cold) is then determined for each period for each year.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
amofile = open('Backup Data/AMOShortUnsmoothed.txt', 'r')
amofile.readline()

amo_indices = {}
for line in amofile:
    amo = line.split()
    for value in amo:
        # Remove values with a missing value code.
        if (value == '-99.990'):
            amo.remove(value)
    # Only take valid lines from this type of file.
    if not line.startswith('  '):
        amo_indices[amo[0]] = {'Indices':[float(i) for i in amo[1:]]}

amofile.close()

for year in amo_indices:
    amo_indices[year]['JJMean'] = np.mean(amo_indices[year]['Indices'][4:8])
    amo_indices[year]['SeasonMean'] = np.mean(amo_indices[year]['Indices'][4:])

    # Phases for June-July.
    if (amo_indices[year]['JJMean'] >= 0.0):
        amo_indices[year]['JJPhase'] = 'Warm'
    elif (amo_indices[year]['JJMean'] <= 0.0):
        amo_indices[year]['JJPhase'] = 'Cold'

    # Phases for hurricane season.
    if (amo_indices[year]['SeasonMean'] >= 0.0):
        amo_indices[year]['SeasonPhase'] = 'Warm'
    elif (amo_indices[year]['SeasonMean'] <= 0.0):
        amo_indices[year]['SeasonPhase'] = 'Cold'

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Takes in the number of named storms, hurricanes, and major hurricanes from a
#   data file based on the table found at
#   http://www.aoml.noaa.gov/hrd/hurdat/comparison_table.html
#   Only the original values are taken for now, as many revisions are still
#   pending as of 2017.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
hurdatfile = open('Backup Data/HURDATSeasonal.txt', 'r')
hrd_header = hurdatfile.readline()

hurdat = {}
for line in hurdatfile:
    hurdat_line = line.split()
    hurdat[hurdat_line[0]] = {'Named':hurdat_line[1], 'Hurricanes':hurdat_line[3], 'Intense':hurdat_line[5]}

hurdatfile.close()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculates the full Hurricane Database, version 2, and determines the number
#   of tropical storm days, hurricane days, and intense hurricane days for
#   each year. Calls storm_days function from hurdat_test.py.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
hurdat_days = storm_days('Backup Data/HURDAT.txt')

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Calculate the minimum and maximum total years that are common to all of
#   the datasets.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
total_min_year = max(min(regional_index.keys()), min(nino_indices.keys()),
                     min(amo_indices.keys()), min(hurdat.keys()),
                     min(hurdat_days.keys()))
total_max_year = min(max(regional_index.keys()), max(nino_indices.keys()),
                     max(amo_indices.keys()), max(hurdat.keys()),
                     max(hurdat_days.keys()))

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create a list of the common years that are in the regional index, El Nino,
#   and AMO datasets. (As of version 1.2, hurdat is used as the baseline
#   because it is known to have the largest and most complete set of years.)
#   This will likely be moved to plot_correlation in version 2.0.
#   In intermediate versions, there will be more than one of these.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
common_year = []
for year in hurdat.keys():
    if year in regional_index.keys() and year in nino_indices.keys() and year in amo_indices.keys():
        common_year.append(year)

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Create graphs of the the data for each set of years to measure the
#   correlations between the various sets of variables.
#   Example:  the regional rainfall index and the number of named tropical
#             cyclones.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
axis_info_rain = 'Regionally Averaged Normalized Rainfall Index'
title_info_rain = '\nand Western Sahel Rainfall in June and July'
title_info_JJnino = 'June-July Average El Ni$\mathregular{\\tilde{n}}$o Phase'
title_info_SeasonNino = 'June-November Average El Ni$\mathregular{\\tilde{n}}$o Phase'
axis_info_SeasonNino = 'May-December Averaged El Ni$\mathregular{\\tilde{n}}$o Phase'
axis_info_JJNino = 'May-August Averaged El Ni$\mathregular{\\tilde{n}}$o Phase'
title_info_named = 'Named Storms in the North Atlantic Ocean Tropical Cyclone Basin'
title_info_hurr = 'Hurricanes in the North Atlantic Ocean Tropical Cyclone Basin'
title_info_major = 'Intense (Cat. 3+) Hurricanes in the North Atlantic Ocean Tropical Cyclone Basin'
title_info_named_days = 'Named Storm Days in the North Atlantic Ocean Tropical Cyclone Basin'
title_info_hurr_days = 'Hurricane Days in the North Atlantic Ocean Tropical Cyclone Basin'
title_info_major_days = 'Intense (Cat. 3+) Hurricane Days in the North Atlantic Tropical Cyclone Basin'

# June-July El Nino Phase and the Regional Rainfall Index
nino_indices['JJR'], nino_indices['JJCorrelation'] = (
    plot_correlation(nino_indices, regional_index, 'JJMean', 'index',
    common_year, title_info_JJnino + title_info_rain, axis_info_JJNino,
    axis_info_rain, 'NinoJJ.png'))

# Season El Nino Phase and the Regional Rainfall Index
nino_indices['SeasonR'], nino_indices['SeasonCorrelation'] = (
    plot_correlation(nino_indices, regional_index, 'SeasonMean', 'index',
    common_year, title_info_SeasonNino + title_info_rain, axis_info_SeasonNino,
    axis_info_rain, 'NinoSeason.png'))

# June-July AMO Phase and the Regional Rainfall Index
amo_indices['JJR'], amo_indices['JJCorrelation'] = (
    plot_correlation(amo_indices, regional_index, 'JJMean', 'index',
    common_year, 'June-July Average AMO Phase' + title_info_rain,
    'May-August Averaged AMO Phase', axis_info_rain, 'amoJJ.png'))

# Season AMO Phase and the Regional Rainfall Index
amo_indices['SeasonR'], amo_indices['SeasonCorrelation'] = (
    plot_correlation(amo_indices, regional_index, 'SeasonMean', 'index',
    common_year, 'June-November Average AMO Phase' + title_info_rain,
    'May-December Averaged AMO Phase', axis_info_rain, 'amoSeason.png'))

# Regional Rainfall Index and Number of Named Tropical Cyclones
hurdat['NamedR'], hurdat['NamedCorrelation'] = plot_correlation(regional_index,
    hurdat, 'index', 'Named', common_year, title_info_named + title_info_rain,
    axis_info_rain, 'Named Storm Frequency', 'named.png')

# Regional Rainfall Index and Number of Hurricanes
hurdat['HurricaneR'], hurdat['HurricaneCorrelation'] = (
    plot_correlation(regional_index, hurdat, 'index', 'Hurricanes',
    common_year, title_info_hurr + title_info_rain, axis_info_rain,
    'Hurricane Frequency', 'Hurricane.png'))

# Regional Rainfall Index and Number of Major Hurricanes
hurdat['IntenseR'], hurdat['IntenseCorrelation'] = (
    plot_correlation(regional_index, hurdat, 'index', 'Intense', common_year,
    title_info_major + title_info_rain, axis_info_rain,
    'Intense Hurricane Frequency', 'Intense.png'))

# Seasonal El Nino Phase and Seasonal AMO Phase
nino_indices['SeasonNinoAmoR'], nino_indices['SeasonNinoAmoCorrelation'] = (
    plot_correlation(nino_indices, amo_indices, 'SeasonMean', 'SeasonMean',
    common_year, title_info_SeasonNino+'\nand June-November Average AMO Phase',
    axis_info_SeasonNino,'May-December Averaged AMO Phase','NinoAmoSeason.png'))

# Seasonal El Nino Phase and Number of Named Tropical Cyclones
nino_indices['SeasonNinoNamedR'], nino_indices['SeasonNinoNamedCorrelation'] =(
    plot_correlation(nino_indices, hurdat, 'SeasonMean', 'Named', common_year,
    title_info_SeasonNino + '\nand Named Storms', axis_info_SeasonNino,
    'Named Storm Frequency', 'NinoSeasonNamed.png'))

# Seasonal AMO Phase and Number of Named Tropical Cyclones
amo_indices['SeasonAmoNamedR'], amo_indices['SeasonAmnoNamedCorrelation'] = (
    plot_correlation(amo_indices, hurdat, 'SeasonMean', 'Named', common_year,
    'June-November Average AMO Phase\nand Named Storms', 'May-December'
    + ' Averaged AMO Phase', 'Named Storm Frequency', 'AmoSeasonNamed.png'))

# Remove 2017 from the longer term data.
common_year.remove('2017')

# Regional Rainfall Index and Named Tropical Cyclone Days
hurdat_days['NamedR'], hurdat_days['NamedCorrelation'] = plot_correlation(
    regional_index, hurdat_days, 'index', 'Named Days', common_year,
    title_info_named_days + title_info_rain, axis_info_rain, 'Named Storm Days',
    'named_days.png')

# Regional Rainfall Index and Hurricane Days
hurdat_days['HurricaneR'], hurdat_days['HurricaneCorrelation'] = (
    plot_correlation(regional_index, hurdat_days, 'index', 'Hurricane Days',
    common_year, title_info_hurr_days + title_info_rain, axis_info_rain,
    'Hurricane Days', 'Hurricane_days.png'))

# Regional Rainfall Index and Major Hurricane Days
hurdat_days['IntenseR'], hurdat_days['IntenseCorrelation'] = (
    plot_correlation(regional_index, hurdat_days, 'index', 'Intense Days',
    common_year, title_info_major_days + title_info_rain, axis_info_rain,
    'Intense Hurricane Days', 'Intense_days.png'))

# Seasonal El Nino Phase and Number of Named Tropical Cyclone Days
nino_indices['SeasonNinoNamedDaysR'], nino_indices['SeasonNinoNamedDaysCorrelation'] =(
    plot_correlation(nino_indices, hurdat_days, 'SeasonMean', 'Named Days', common_year,
    title_info_SeasonNino + '\nand Named Storms', axis_info_SeasonNino,
    'Named Storm Days', 'NinoSeasonNamedDays.png'))

# Seasonal AMO Phase and Number of Named Tropical Cyclone Days
amo_indices['SeasonAmoNamedDaysR'], amo_indices['SeasonAmoNamedDaysCorrelation'] = (
    plot_correlation(amo_indices, hurdat_days, 'SeasonMean', 'Named Days', common_year,
    'June-November Average AMO Phase\nand Named Storms', 'May-December'
    + ' Averaged AMO Phase', 'Named Storm Days', 'AmoSeasonNamedDays.png'))

eeaanhi = (nino_indices['JJCorrelation'] + nino_indices['SeasonCorrelation']
    + amo_indices['JJCorrelation'] + amo_indices['SeasonCorrelation'] +
    hurdat['NamedCorrelation'] + hurdat['HurricaneCorrelation'] +
    hurdat['IntenseCorrelation'])

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Output information to the file. Contains the Regionally Averaged
#   Precipitation Index, the number of stations used for each year, the phases
#   of El Nino and the AMO for both the June-July early season period and the
#   hurricane season overall, the number of tropical cyclones, hurricanes, and
#   major hurricanes, and the results of whether there was a correlation
#   coefficient of greater than 0.9 for each category.
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
outfile = open('Summary.txt', 'w')

outfile.write('RPI: Regionally Averaged Precipitation Index\n')
outfile.write('Stat: Number of Stations\n')
outfile.write('JJNino: El Nino Phase averaged May through August ' +
              '(the phase during the June-July period)\n')
outfile.write('SeasonNino: El Nino Phase averaged May through December ' +
              '(the phase during the hurricane season)\n')
outfile.write('JJAMO: AMO Phase averaged May through August (the phase ' +
              'during the June-July period)\n')
outfile.write('SeasonAMO: AMO Phase averaged May through December (the ' +
              'phase during the hurricane season)\n')
outfile.write('Named: Named storms\n')
outfile.write('Intense: Major (Cat 3+) hurricanes\n')
outfile.write('EEAANHI: Correlation (Y or N) between El Nino (June-July and' +
              ' for the hurricane season), AMO (for the same two periods), ' +
              'and for named storms, hurricanes, and major hurricanes for ' +
              'the overall period of the dataset.\n\n')
outfile.write('Year   RPI  Stat  JJNino  SeasonNino  JJAMO  SeasonAMO  Named' +
              '  Hurricanes  Intense  EEAANHI\n')

for intyear in range(int(total_min_year), int(total_max_year)+1):
    year = str(intyear)
    outfile.write('%4d %6.2f %3d %7s %9s %8s %8s %7s %8s %10s %11s\n' % (intyear, regional_index[year]['index'], regional_index[year]['station_num'], nino_indices[year]['JJPhase'], nino_indices[year]['SeasonPhase'], amo_indices[year]['JJPhase'], amo_indices[year]['SeasonPhase'], hurdat[year]['Named'], hurdat[year]['Hurricanes'], hurdat[year]['Intense'], eeaanhi))

outfile.close()

