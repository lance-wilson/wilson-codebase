#!/bin/bash
#
# Purpose:  Create a set of back trajectories, plot them, and create a tar
#           file containing the new plots.
#
# Syntax: ./make_plot_tar_back_traj.sh model_version_number parcel_label
#
# Example: ./make_plot_tar_back_traj.sh v5 v5_meso_tornadogenesis
#
# Modification History:
#   2021/10/14 - Lance Wilson:  Created.
#

if [ -z $2 ]
then
    echo "Syntax: $0 model_version_number parcel_label"
    echo "Example: $0 v5 v5_meso_tornadogenesis"
else
    version_number=$1
    parcel_label=$2

    python calc_back_traj_meters_corrected.py $version_number $parcel_label

    ./plot_all_back_traj.sh $version_number $parcel_label

    cd BackTrajectoryImages/75m_"$version_number"
    mkdir "$parcel_label"
    mv ../*.png "$parcel_label"
    tar -cvf "${parcel_label}".tar "${parcel_label}"/*.png
fi
