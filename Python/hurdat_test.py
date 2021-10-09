#!/usr/bin/env python
#
# Name:
#   hurdat_test.py
#
# Purpose:
#   The purpose of this function is to calculate the number of days in each
#   year in which there are named storms, hurricanes, and intense hurricanes,
#   to produce correlation plots with West African Rainfall in INTRAMWARE.
#
# Syntax:
#   Call function: from hurdat_test import storm_days
#
#   Input:  storm_days function requires the name of the file, which should be
#           a file formatted as the HURDAT2 format.
#
#   Output: Returns dictionary containing each year, and the number of storm
#           days,  hurricane days, and intense hurricane days for that year.
#
# Modification History:
#   Date         Editor         Version Modifications
#   2017/03/15 - Lance Wilson:  0.1     Created.
#   2017/03/16 - Lance Wilson:  0.2     Adjusted calculations.
#   2017/03/17 - Lance Wilson:  1.0     Obtained correct output, and accounted
#                                       for seasons that end in January.
#
# Verification of Data:
#   Manually evaluated a smaller file containing only two storms, one of
#   which had one advisory. Noted that calculations assume that a storm
#   did not maintain its status before the first advisory at that strength
#   or after the last advisory with that strength.
#
# Copyright 2017 Lance Wilson

import datetime
import numpy as np

# Takes in a date as a string, the time as a string, the format utilized by
#   the datetime module (example: '%Y%m%d for YYYYMMDD date format), and the
#   current_year as a string.
def day_of_year(date, time, format, current_year):
    # Create an object with the date split up from defined form specified in format.
    date_object = datetime.datetime.strptime(date, format)
    # Convert the date object into a tuple (really more of a dictionary).
    time_tuple = date_object.timetuple()
    # Take the day of the year from this 'tuple' and add the fraction of the
    #   day, taken from the time. (This results in some error when the advisory
    #   isn't on the hour, but those advisories are so infrequent that the
    #   error is generally on the order of a tenth of a percent or less.)
    day_of_year = float(time_tuple.tm_yday) + (time/2400.)

    if (int(current_year) != time_tuple.tm_year):
        day_of_year += 365.
        if (int(current_year) % 4 == 0) and (int(current_year) % 100 != 0):
            day_of_year += 1.

    return day_of_year

def storm_days(filename):
    full_hurdatfile = open(filename, 'r')
    major_strength = 95  # Major hurricanes have greater wind speeds, in Knots.

    # List of formats:
    # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
    format = '%Y%m%d'
    hurdat_days = {}

    first_line = full_hurdatfile.readline()
    first_header = first_line.split(',')

    # Need the year before the first year so all variables are initialized.
    start_year = str(int(first_header[0][-4:]) - 1)
    current_year = start_year
    previous_time = 0.0

    # Return to beginning of file.
    full_hurdatfile.seek(0,0)
    new_storm = False

    for line in full_hurdatfile:
        this_advisory = line.split(',')

        # If the current line is a header for a storm (e.g. AL012003) and it
        #   represents a new year.
        if (this_advisory[0].startswith('AL') and this_advisory[0].endswith(str(int(current_year)+1))):
            # If statement is used to skip the dictionary entry on the first
            #   run, but still initialize the variables inside the loop.
            if (current_year != start_year):
                hurdat_days[current_year] = {'Named Days':storm_days, 'Hurricane Days':hurricane_days, 'Intense Days':intense_days}

            # Reset the output variables and current year for the next year.
            storm_days = 0
            hurricane_days = 0
            intense_days = 0
            current_year = str(int(current_year)+1)

        # Set new_storm to true if this line is a header to a new storm.
        if(this_advisory[0].startswith('AL')):
            new_storm = True
        else:
            this_date = this_advisory[0]
            adv_hour = int(this_advisory[1])
            end_time = day_of_year(this_date, adv_hour, format, current_year)
            time_since_last_adv = end_time - previous_time
            previous_time = end_time

            this_strength = int(this_advisory[6])

            # Only check the status and calculate the duration at this strength
            #   if this isn't a new storm (otherwise it will calculate the time
            #   since the last storm).
            if not new_storm:
                status = this_advisory[3].strip()
                # If the storm is of Tropical Storm strength.
                if (status == 'TS'):
                    storm_days += time_since_last_adv
                # If the storm is of Hurricane strength.
                if (status == 'HU'):
                    storm_days += time_since_last_adv
                    hurricane_days += time_since_last_adv
                    # Manual check for Cat 3+, since there is no preset for it.
                    if (this_strength > major_strength):
                        intense_days += time_since_last_adv

            new_storm = False

    full_hurdatfile.close()

    # An extra if statement on the off chance that the input file is empty.
    if (current_year != start_year):
        hurdat_days[current_year] = {'Named Days':storm_days, 'Hurricane Days':hurricane_days, 'Intense Days':intense_days}

    return hurdat_days
