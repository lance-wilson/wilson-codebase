#!/bin/bash
#
# Purpose:  Create and plot all analysis data for forward trajectories.
#
# Syntax: ./make_forward_traj_plots_onetar.sh model_version_number parcel_label number_traj_plots
#
# Example: ./make_forward_traj_plots_onetar.sh v5 1000parcel_tornadogenesis 4
#
# Modification History:
#   2022/06/07 - Lance Wilson:  Created.
#

if [ -z $3 ]
then
    echo "Syntax: $0 model_version_number parcel_label number_traj_plots"
    echo "Example: $0 v5 1000parcel_tornadogenesis 4"
else
    version_number=$1
    parcel_label=$2
    number_trajectories=$3

    script_dir=$(pwd)
    #cd "$script_dir"

    timestamp=$(date +"%Y%m%d_%H%M")

    image_dir=75m_100p_"$version_number"/forward_traj_analysis/ForwardTrajectoryImages/

    output_dir=75m_100p_"$version_number"/forward_traj_analysis/full_output/"$version_number"_"$parcel_label"_"$timestamp"/

    model_fields=(dbz thpert)
    #model_fields=(dbz thpert xvort zvort u v w)

    parcel_categories=(forward_flank up_over wraparound)

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    # Parentheses in function run the block/list in a subshell, so shouldn't 
    #   have to change the directory back.
    mv_images () { (
        dir_name=$1
        cd "$output_dir"
        mkdir -p "$dir_name"
        mv "$image_dir"/*.png "$dir_name"
        #cd "$script_dir"
    ) }

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    mkdir -p /vortex2/lwilson/75m_100p_"$version_number"/forward_traj_analysis/parcel_interpolation/
    mkdir -p "$image_dir"
    mkdir -p "$output_dir"
    mkdir -p /vortex2/lwilson/75m_100p_"$version_number"/forward_traj_analysis/categorized_trajectories/index_order_from_mean/
    mkdir -p /vortex2/lwilson/75m_100p_"$version_number"/forward_traj_analysis/categorized_trajectories/vorticity_source_percent/

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    echo
    echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    echo "calc_forward_traj_vort_tendency"
    python calc_forward_traj_vort_tendency.py $version_number $parcel_label

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    echo
    echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    echo "categorize_forward_trajectories"
    python categorize_forward_trajectories.py $version_number $parcel_label

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    for parcel_category in "${parcel_categories[@]}"
    do
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "calc_mean_forward_trajectories, $parcel_category"
        python calc_mean_forward_trajectories.py $version_number $parcel_label $parcel_category $number_trajectories

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "meso_vort_source_forward_percentage.py, $parcel_category"
        python meso_vort_source_forward_percentage.py $version_number $parcel_label $parcel_category

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_prog_vort.py, $parcel_category"
        python -W ignore plot_forward_prog_vort.py $version_number $parcel_label $parcel_category $number_trajectories
        mv_images prog_vort_"$version_number"_"$parcel_label"_"$parcel_category"

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_traj_vort_component, $parcel_category"
        python -W ignore plot_forward_traj_vort_component.py $version_number $parcel_label $parcel_category $number_trajectories
        mv_images vort_component_"$version_number"_"$parcel_label"_"$parcel_category"

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_traj_integrated_vort_comp, $parcel_category"
        python -W ignore plot_forward_traj_integrated_vort_comp.py $version_number $parcel_label $parcel_category $number_trajectories
        mv_images "$version_number"_"$parcel_label"_"$parcel_category"_integrated_comp

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_traj_integrated_svort_comp, $parcel_category"
        python -W ignore plot_forward_traj_integrated_svort_comp.py $version_number $parcel_label $parcel_category $number_trajectories
        mv_images "$version_number"_"$parcel_label"_"$parcel_category"_integrated_svort

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_traj_integrated_vort_comp, $parcel_category"
        python -W ignore plot_forward_traj_vort_magnitude.py $version_number $parcel_label $parcel_category $number_trajectories
        mv_images "$version_number"_"$parcel_label"_"$parcel_category"_vort_mag
    done

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    for model_field in "${model_fields[@]}"
    do
        for parcel_category in "${parcel_categories[@]}"
        do
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            echo
            echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
            echo "plot_forward_categorized_trajectories, $model_field, $parcel_category, all"
            python -W ignore plot_forward_categorized_trajectories.py $version_number $parcel_label $parcel_category $model_field zpos all
            mv_images "$version_number"_"$parcel_label"_"$parcel_category"_"$model_field"

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            echo
            echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
            echo "plot_forward_categorized_trajectories, $model_field, $parcel_category, select"
            python -W ignore plot_forward_categorized_trajectories.py $version_number $parcel_label $parcel_category $model_field zpos $number_trajectories
            mv_images "$version_number"_"$parcel_label"_"$parcel_category"_"$model_field"_selected

            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            echo
            echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
            echo "plot_forward_cat_traj_vectors, $model_field, $parcel_category"
            /usr/local/anaconda3/bin/python -W ignore plot_forward_cat_traj_vectors.py $version_number $parcel_label $parcel_category $model_field zvort $number_trajectories
            mv_images "$version_number"_"$parcel_label"_"$parcel_category"_"$model_field"_vectors

            #python -W ignore plot_forward_categorized_trajectories.py $version_number $parcel_label forward_flank thpert all
        done

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_traj_budgets, $model_field"
        python -W ignore plot_forward_traj_budgets.py $version_number $parcel_label $model_field all
        mv_images "$version_number"_"$parcel_label"_vortbudget_"$model_field"

        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        echo
        echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
        echo "plot_forward_trajectory_analysis, $model_field"
        python -W ignore plot_forward_trajectory_analysis.py $version_number $parcel_label $model_field
        mv_images "$version_number"_"$parcel_label"_analysis_"$model_field"
    done
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    echo
    echo '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    echo "Final tar file"
    cd "$output_dir"/..
    tar -cf "$version_number"_"$parcel_label"_"$timestamp".tar "$version_number"_"$parcel_label"_"$timestamp"/*

fi
