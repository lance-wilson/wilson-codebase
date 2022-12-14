#!/bin/bash
#
# Purpose:  Move model files between vortex2 and home partitions to backup
#           important information for specific runs or move data in for new
#           runs.
# Files:    Parcel data file (cm1out_pdata.nc)
#           Stats file (e.g. JS_75m_run5_stats.nc)
#           Namelist (namelist.input)
#           CM1 Log (cm1.out)
#
# Syntax: ./move_model_files.sh parcel_label direction
#
# Example: ./move_model_files.sh v5_meso_tornadogenesis vortex2
#
# Modification History:
#   2022/02/22 - Lance Wilson:  Created.
#

if [ -z $2 ]
then
    echo "Syntax: $0 model_version_number parcel_label"
    echo "Example: $0 v5 v5_meso_tornadogenesis"
else
    version_number=$1
    parcel_label=$2

    model_dir=/home/lance.wilson/cm1r16_wforce_ncdf_budget/run/
    vortex_dir=/vortex2/lwilson/75m_"$version_number"/

    cp "${model_dir}"cm1.out "{$vortex_dir}"cm1_output_logs/cm1_"{$parcel_label}".out

    cp "${model_dir}"namelist.input "{$vortex_dir}"namelists/namelist_"{$parcel_label}".input

    cp "${model_dir}"cm1out_pdata.nc "{$vortex_dir}"parcel_files/cp_files/cm1out_pdata_"{$parcel_label}"_cp.nc
    nccopy "${model_dir}"cm1out_pdata.nc "{$vortex_dir}"parcel_files/cm1out_pdata_"{$parcel_label}".nc

    cp "${model_dir}"JS_75m_run5_stats.nc "{$vortex_dir}"stats_files/cp_files/JS_75m_run5_stats_"{$parcel_label}"_cp.nc
    nccopy "${model_dir}"JS_75m_run5_stats.nc "{$vortex_dir}"stats_files/JS_75m_run5_stats_"{$parcel_label}".nc

fi
