#!/bin/bash
#
# Takes in files of two soundings, reads the data from awk and sorts the data into three new
#   files for each, then compiles the sonde_derive.c program, and runs the executable file
#   for each sounding, and then creates the gnu plots for wind chill for each and the
#   combined helicity plot.
#
# Input: Two Sounding files, currently from ABQ and LIH
#
# Output:  Outputs two wind chill plot graphs, a helicity graph, and the text files of
#          sorted data.
#
# Syntax: ./automation_script.bash inSounding1 inSounding2
#
# Written: Lance Wilson, Mar. 2016
#

#if the filename was not entered
if [ -z $2 ]
then
  echo "Syntax: $0 sonde1_name sonde2_name"
  # exit from script
  exit
fi


# Sort first sounding into the three file types.
./bash_script.bash $1 "sonde_tv.out" "sonde_t.out" "sonde_v.out"
# Compile sonde_derive.c
gcc -o sonde_derive sonde_derive.c -lm
# Run sonde_derive with the data from the first sounding
./sonde_derive "sonde_tv.out" "sonde_v.out" "ABQ_out.txt" "ABQ_out_wc.txt"
# Plot wind chill over Albuquerque
gnuplot wind_chill_plot.gnu

# Sort second sounding into the three file types.
./bash_script.bash $2 "sonde_tv2.out" "sonde_t2.out" "sonde_v2.out"
# Run sonde_derive with the data from the second sounding
./sonde_derive "sonde_tv2.out" "sonde_v2.out" "LIH_out.txt" "LIH_out_wc.txt"
# Plot wind chill Lihue
gnuplot wind_chill_plot2.gnu

# Plot helicity for both Albuquerque and Lihue
gnuplot helicity_plot.gnu
