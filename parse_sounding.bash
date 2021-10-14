#!/bin/bash
#
# The purpose of this script is to take in a sounding file and sort its data using awk\
#     to create new files containing just temperature and pressure.
#
# Input: Sounding file with the standard radiosonde format.
#
# Output: Three text files with data sorted into soundings, one at mandatory, surface, and
#         tropopause levels only, and the others with additional data for significant or 
#         wind levels.
#
# Syntax: ./bash_script.bash sonde_name1 sonde_name2
#
# Written: Lance Wilson, Apr. 2016
#

#if the filename was not entered
if [ -z $2 ]
then
  echo "Syntax: $0 sonde_name1 sonde_name2"
  # exit from script
  exit
fi

# Output pressure and temperature from sounding to new text file.
awk '{if (($1 != 254) && ($1 != 1) && ($1 != 2) && ($1 != 3) && ($4 != 99999)) print $2/10,$4/10}' $1 > observe_start.txt

# Output pressure and temperature from sounding to new text file.
awk '{if (($1 != 254) && ($1 != 1) && ($1 != 2) && ($1 != 3) && ($4 != 99999)) print $2/10,$4/10}' $2 > observe_end.txt
