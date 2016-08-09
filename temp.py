#!/usr/bin/env python

import os
from path import path
from utils.general import *
import csv

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

def add_os_browser(ROOT_DIRECTORY, os_flag, browser_flag):
    d = path(ROOT_DIRECTORY)
    current_dir = os.getcwd()

    if os_flag == 'w' and browser_flag == 'ff':
        head_str = 'w_hi_ff_'
    elif os_flag == 'w' and browser_flag == 'chrome':
        head_str = 'w_hi_chrome_'
    elif os_flag == 'l' and browser_flag == 'ff':
        head_str = 'L_hi_ff_'
    elif os_flag == 'l' and browser_flag == 'chrome':
        head_str = 'L_hi_chrome_'

    for root, dirs, files in os.walk(d):
        print root
        new_folder_name = head_str + root

        for filename in os.listdir(root):

            if filename.endswith(".pcap"):
                new_file_name = head_str + filename
                new_full_file_name = os.path.join(root, new_file_name)
                full_file_name = os.path.join(root, filename)
                os.rename(full_file_name, new_full_file_name)

def transform_dirs(path, os_flag, browser_flag):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for folder in row:
                # print str(repr(folder))
                add_os_browser(folder, os_flag, browser_flag)


def gen_folder_filename_couples(PARENT_DIRECTORY, file_name):
    d = path(PARENT_DIRECTORY)
    l = []
    for root, dirs, files in os.walk(d):
        # if any(file.endswith('.hcl') for file in files) and any(is_pcap_session(file) for file in files):
        if any(is_pcap_session(join(root, file)) for file in files):
            l.append([path.abspath(root), join(root, files[0])])

    with open(file_name, 'wb') as csvfile:
      writer = csv.writer(csvfile, delimiter=',')
      for item in l:
          writer.writerow(item)

def fix_folders():
    path_w_ff = '/home/jon/workspace/pcap-feature-extractor/fix_these_folders_windows_ff.csv'
    path_w_chrome = '/home/jon/workspace/pcap-feature-extractor/fix_these_folders_windows_chrome.csv'
    path_l_ff = '/home/jon/workspace/pcap-feature-extractor/fix_these_folders_linux_ff.csv'
    path_l_chrome = '/home/jon/workspace/pcap-feature-extractor/fix_these_folders_linux_chrome.csv'

    transform_dirs(path_w_ff, os_flag='w', browser_flag='ff')
    transform_dirs(path_w_chrome, os_flag='w', browser_flag='chrome')
    transform_dirs(path_l_ff, os_flag='l', browser_flag='ff')
    transform_dirs(path_l_chrome, os_flag='l', browser_flag='chrome')

if __name__ == "__main__":
