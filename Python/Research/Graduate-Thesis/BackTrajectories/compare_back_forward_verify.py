#!/usr/bin/env python3
#
# Name:
#   compare_back_forward_verify.py
#
# Purpose:  Compare the parcel positions for initialization positions of back
#           trajectories with forward trajectories integrated for a certain
#           amount of time from positions initialized with the exact back
#           trajectory positions integrated the same amount of time backward,
#           and output the distance (in meters) between the two values.
#
# Syntax:
#   python3 compare_back_forward_verify.py back_parcel_label forward_parcel_label
#
#   Input:  A back trajectory numpy archive, named "backtraj_(parcel_label).npz"
#           (created by "new_writeout_exact_initialization.py"),
#           and a CM1 parcel file, named "cm1out_pdata_(parcel_id).nc"
#
# Execution Example:
#   python3 compare_back_forward_verify.py v5_meso_tornadogenesis 12
#
# Modification History:
#   2021/03/02 - Lance Wilson:  Created.
#   2021/09/08 - Lance Wilson:  Modified to run on any trajectory parcel files.
#

from netCDF4 import Dataset
import matplotlib.pyplot as plt
import numpy as np
import sys

if len(sys.argv) > 2:
    # Label of back trajectory parcel file.
    back_parcel_label = sys.argv[1]
    # Label of forward trajectory parcel file.
    forward_parcel_id = sys.argv[2]
else:
    print('Parcel labels were not specified.')
    print('Syntax: python3 compare_back_forward_verify.py back_parcel_label forward_parcel_label')
    print('Example: python3 compare_back_forward_verify.py v5_meso_tornadogenesis 12')
    sys.exit()

version_number = 'v5'

back_parcel_dir = '75m_100p_{:s}/back_traj_verify/'.format(version_number)
forward_parcel_dir = '75m_100p_{:s}/parcel_files/'.format(version_number)

# Load back trajectory data from uncompressed numpy archive.
back_traj_data = np.load(back_parcel_dir + 'back_verify_back_{:s}.npz'.format(back_parcel_label))
indices = back_traj_data['indices']
xpos_back = back_traj_data['xpos'][indices]
ypos_back = back_traj_data['ypos'][indices]
zpos_back = back_traj_data['zpos'][indices]

# file_num_offset in this case should have been calculated in
#   new_writeout_exact_initialization to match the CM1 file number
#   corresponding to the comparison time.
# Adding 0 to the file value to make sure that the output is an integer.
file_num_offset = back_traj_data['offset'] + 0

forward_parcel_file_name = forward_parcel_dir + 'cm1out_pdata_{:s}.nc'.format(forward_parcel_id)

ds_parcel = Dataset(forward_parcel_file_name, "r")
# Get forward parcel positions at the comparison time.
xpos_forward = np.copy(ds_parcel.variables['x'][file_num_offset-1])
ypos_forward = np.copy(ds_parcel.variables['y'][file_num_offset-1])
zpos_forward = np.copy(ds_parcel.variables['z'][file_num_offset-1])
ds_parcel.close()

x_diff = xpos_back - xpos_forward
y_diff = ypos_back - ypos_forward
z_diff = zpos_back - zpos_forward

mean_x_diff = np.mean(x_diff)
mean_y_diff = np.mean(y_diff)
mean_z_diff = np.mean(z_diff)

print('Differences in x positions (back - forward):')
print(x_diff)
print('Differences in y positions (back - forward):')
print(y_diff)
print('Differences in z positions (back - forward):')
print(z_diff)

print('Mean difference in x positions (back - forward):')
print(mean_x_diff)
print('Mean difference in y positions (back - forward):')
print(mean_y_diff)
print('Mean difference in z positions (back - forward):')
print(mean_z_diff)

# X-Direction Histogram Error
fig1 = plt.figure(figsize=(10,7))
counts, bin_edges, patches = plt.hist(x_diff, bins=20, color='tab:blue')
plt.axvline(x=mean_x_diff, label='Mean X Error = {:.0f} m'.format(mean_x_diff), color='red')
plt.xticks(bin_edges)
plt.xlabel('Position Error in East Direction (m)')
plt.ylabel('Counts per bin')
plt.title('Back Trajectory X Position Difference from Forward Trajectories')
plt.legend()
plt.savefig(back_parcel_dir + 'back_verify_back_{:s}_xdiff.png'.format(back_parcel_label), dpi=400)

# Y-Direction Error Histogram Plot
fig2 = plt.figure(figsize=(10,7))
counts, bin_edges, patches = plt.hist(y_diff, bins=20, color='tab:blue')
plt.axvline(x=mean_y_diff, label='Mean Y Error = {:.0f} m'.format(mean_y_diff), color='red')
plt.xticks(bin_edges)
plt.xlabel('Position Error in North Direction (m)')
plt.ylabel('Counts per bin')
plt.title('Back Trajectory Y Position Difference from Forward Trajectories')
plt.legend()
plt.savefig(back_parcel_dir + 'back_verify_back_{:s}_ydiff.png'.format(back_parcel_label), dpi=400)

# Z-Direction Histogram Error
fig3 = plt.figure(figsize=(10,7))
counts, bin_edges, patches = plt.hist(z_diff, bins=20, color='tab:blue')
plt.axvline(x=mean_z_diff, label='Mean Z Error = {:.0f} m'.format(mean_z_diff), color='red')
plt.xticks(bin_edges)
plt.xlabel('Position Error in Up Direction (m)')
plt.ylabel('Counts per bin')
plt.title('Back Trajectory Z Position Difference from Forward Trajectories')
plt.legend()
plt.savefig(back_parcel_dir + 'back_verify_back_{:s}_zdiff.png'.format(back_parcel_label), dpi=400)

#plt.show()

