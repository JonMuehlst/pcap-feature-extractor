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
