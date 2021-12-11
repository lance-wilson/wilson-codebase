#!/bin/bash
#
# Plot forward trajectory images for all variables.
#
# Syntax: ./plot_all_forward_traj.sh model_version_number parcel_label file_num_offset
#

if [ -z $3 ]
then
    echo "Syntax: $0 model_version_number parcel_label file_num_offset"
else
    version_number=$1
    parcel_id=$2
    file_num_offset=$3

    python -W ignore plot_forward_trajectory_elevation_color.py $version_number $parcel_id thpert $file_num_offset &
    python -W ignore plot_forward_trajectory_elevation_color.py $version_number $parcel_id xvort $file_num_offset &
    python -W ignore plot_forward_trajectory_elevation_color.py $version_number $parcel_id dbz $file_num_offset &
    python -W ignore plot_forward_trajectory_elevation_color.py $version_number $parcel_id u $file_num_offset &
    python -W ignore plot_forward_trajectory_elevation_color.py $version_number $parcel_id v $file_num_offset &
    python -W ignore plot_forward_trajectory_elevation_color.py $version_number $parcel_id w $file_num_offset
fi
