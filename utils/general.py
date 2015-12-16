import os
from path import path
from os import listdir
from os.path import isfile, join

def cleanup_pyc(DIRECTORY):
    d = path(DIRECTORY)
    files = d.walkfiles("*.pyc")
    for file in files:
        file.remove()
        print "Removed {} file".format(file)


"""
Assuming a relevant pcap directory contains a .hcl file with label details.
This allows a non strict folder hierarchy i.e.
data/
    any_folder_order/
        relevant_folder1/
            label_data.hcl
            *.pcap
    dummy_folder_name/
        relevant_folder2/
            label_data.hcl
            *.pcap
"""
def gen_data_folders(PARENT_DIRECTORY):
    d = path(PARENT_DIRECTORY)
    l = []
    for root, dirs, files in os.walk(d):
        if any(file.endswith('.hcl') for file in files):
            l.append(path.abspath(root))
    return l

""" Returns a list of pcap file names from a given folder """
def gen_pcap_filenames(folder_name):
        return [join(folder_name, f) for f in listdir(folder_name) if (isfile(join(folder_name, f)) and ('hcl' not in f) and ('pcap' in f)) ]


"""
Labels per combination:
    os = { Linux, Windows, OSX }
    browser = { Chrome, FireFox, IExplorer }
    application = { , }
    service = { , }

    0 = (Linux, Chrome)
    1 = (Linux, FireFox)
    2 = (Windows, Chrome)
    3 = (Windows, FireFox)
    4 = (Windows, IExplorer)
    5 = (OSX, Safari)

"""
def gen_label(os, browser, application, service):
    """
    if os == 'Linux':
        if browser == 'Chrome':
            return 0
        elif browser == 'FireFox':
            return 1
    elif os == 'Windows':
        if browser == 'Chrome':
            return 2
        elif browser == 'FireFox':
            return 3
        elif browser == 'IExplorer':
            return 4
    elif os == 'OSX':
        if browser == 'Safari':
            return 5
    """
    if os == 'Linux':
        return 0
    elif os == 'Windows':
        return 1
    elif os == 'OSX':
        return 2


"""
Parse a folder name and return the os + browser
Currently returns os only.
Assumes the following format:
L_cyber_chrome_09-17__11_38_11
"""
def parse_folder_name(folder_name):
    temp = folder_name.split(os.sep)
    temp.reverse()
    tokens = temp[0].split('_')
    if tokens[0] == 'L':
        return 'Linux'
    elif tokens[0] == 'W':
        return 'Windows'
