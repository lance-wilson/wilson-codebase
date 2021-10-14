#!/bin/bash
#
# The purpose of this script is to take in a sounding file and sort its data using awk\
#     to create three new files.
#
# Input: Sounding file with the standard radiosonde format.
#
# Output: Three text files with data sorted into soundings, one at mandatory, surface, and
#         tropopause levels only, and the others with additional data for significant or 
#         wind levels.
#
# Syntax: ./bash_script.bash sonde_name
#
# Written: Lance Wilson, Mar. 2016
#

#if the filename was not entered
if [ -z $4 ]
then
  echo "Syntax: $0 sonde_name outfile1 outfile2 outfile 3"
  # exit from script
  exit
fi

# if first column equals 4, 7, or 9 AND if the data is valid
#   print columns at the specified levels to sonde_tv.out 
#echo "Outputting pressure, height, temperature, dewpoint, wind direction, and wind speed data at mandatory, tropopause, and surface levels to sonde_tv.out..."
awk '{if (($1 == 4) || ($1 == 7) || ($1 == 9) && ($4 != 99999) && ($5 != 99999) && ($6 != 99999) && ($7 != 99999)) print $2/10,$3,$4/10,$5/10,$6,$7/10}' $1 > $2

# Output pressure, height, temperature, and dew point to specified levels.
#echo "Outputting pressure, height, temperature, and dewpoint data at mandatory, tropopause, surface, and significant levels to sonde_t.out..."
awk '{if (($1 == 4) || ($1 == 7) || ($1 == 9) || ($1 == 5) && ($4 != 99999) && ($5 != 99999)) print $2/10,$3,$4/10,$5/10}' $1 > $3

# Output pressure, height, wind direction, and wind speed to specifiel levels
#   print columns at the specified levels to sonde_tv.out 
#echo "Outputting pressure, height, temperature, dewpoint, wind direction, and wind speed data at mandatory, tropopause, surface, and wind levels to sonde_v.out..."
awk '{if (($1 == 4) || ($1 == 7) || ($1 == 9) || ($1 == 6) && ($6 != 99999) && ($7 != 99999)) print $2/10,$3,$6,$7/10}' $1 > $4
