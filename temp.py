#!/usr/bin/env python

import os
from path import path

def add_d_safari(ROOT_DIRECTORY):
    d = path(ROOT_DIRECTORY)
    current_dir = os.getcwd()
    head_str = 'd_hi_safari_'

    for root, dirs, files in os.walk(d):
        print root
        new_folder_name = head_str + root

        for filename in os.listdir(root):

            if filename.endswith(".pcap"):
                new_file_name = head_str + filename
                new_full_file_name = os.path.join(root, new_file_name)
                full_file_name = os.path.join(root, filename)
                os.rename(full_file_name, new_full_file_name)
