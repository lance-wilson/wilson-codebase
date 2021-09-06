#!/usr/bin/env python3
#                                                               Lance Wilson
# Name:
#   backup.py
#
# Purpose:
#   Backup my computer to an external hard drive, hopefully with the following
#   behaviors:
#       - If file is on computer but not drive:  copy to drive
#       - If file is on drive but not computer:  print file with path to screen
#       - If on both:  copy from computer to drive if timestamps different.
#
# Syntax:
#   python backup.py
#
# Modification History:
#   2020/11/14 - Lance Wilson:  Created.

import glob
import numpy as np
import os
import re
import subprocess
import sys

# Also a file at '/mnt/c/Users/Lance/OneDrive/desktop.ini'; not sure if need to worry about it for this program
folder_list = [ 'Program Files (x86)/Bridge Building Game',
                'Program Files (x86)/FrontPainter',
                'Program Files (x86)/gedit',
                'Program Files (x86)/Steam/steamapps/common/Star Wars Battlefront (Classic 2004)/GameData/SaveGames',
                'Program Files (x86)/Steam/steamapps/common/Star Wars Battlefront II/GameData/SaveGames',
                'Users/Lance/AppData/Local/LucasArts',
                'Users/Lance/AppData/LocalLow/2K',
                'Users/Lance/AppData/LocalLow/HB Studios Multimedia Ltd_',
                'Users/Lance/AppData/Roaming/LucasArts/LEGO® Indiana Jones™ 2/SavedGames',
                'Users/Lance/AppData/Roaming/WB Games',
                'Users/Lance/Desktop',
                'Users/Lance/Documents',
                'Users/Lance/Downloads',
                'Users/Lance/Music',
                'Users/Lance/OneDrive/Documents',
                'Users/Lance/OneDrive/Pictures/Screenshots',
                'Users/Lance/Paint Pictures',
                'Users/Lance/Pictures',
                'Users/Lance/Videos',
                'Users/Lance/VirtualBox VMs'
                ]

# Old Folders:
# 'Users/Lance/AppData/Local/Vivaldi/User Data/Default', 'Users/Lance/OneDrive/Email attachments',

computer_prefix = '/mnt/c/'
drive_prefix = '/mnt/d/Feanor/C/'

def print_changes(folder_list):
    for folder in folder_list:
        print('Searching folder: ' + folder)
        computer_path = computer_prefix + folder + '/**'
        computer_files = glob.glob(computer_path, recursive=True)

        drive_path = drive_prefix + folder + '/**'
        drive_files = glob.glob(drive_path, recursive=True)

        for file_name in drive_files:
            base_match = re.match(drive_prefix + '(.*)', file_name)
            base_name = base_match.group(1)

            if not os.path.isdir(file_name):
                if not (os.path.exists(computer_prefix + base_name)):
                    print(base_name)

def backup(folder_list):
    # Backup the files.
    for folder in folder_list:
        print(folder)
        computer_folder = computer_prefix + folder
        drive_folder = drive_prefix + folder + '/..'
        subprocess.run(['rsync', '-r', computer_folder, drive_folder])

if 'changes' in sys.argv:
    print_changes(folder_list)
else:
    backup(folder_list)

