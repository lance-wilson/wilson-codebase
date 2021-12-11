#!/bin/bash
#
# Plot back trajectory images for all variables.
#
# Syntax: ./plot_all_forward_traj.sh model_version_number parcel_label
#

if [ -z $2 ]
then
    echo "Syntax: $0 model_version_number parcel_label"
    echo "Syntax: $0 v5 v5_meso_tornadogenesis"
else
    version_number=$1
    parcel_label=$2

    #python -W ignore plot_back_traj_elev_color_1Darray.py $version_number $parcel_label thpert &
    python -W ignore plot_back_traj_simpler_loop.py $version_number $parcel_label thpert &
    python -W ignore plot_back_traj_simpler_loop.py $version_number $parcel_label xvort &
    python -W ignore plot_back_traj_simpler_loop.py $version_number $parcel_label dbz &
    python -W ignore plot_back_traj_simpler_loop.py $version_number $parcel_label u &
    python -W ignore plot_back_traj_simpler_loop.py $version_number $parcel_label v &
    python -W ignore plot_back_traj_simpler_loop.py $version_number $parcel_label w
fi
