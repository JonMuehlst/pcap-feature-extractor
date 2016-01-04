import os
from path import path
from os import listdir
from os.path import isfile, join
from utils.read_pcap import read_pcap
import csv

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

-----------------
Currently assuming that if a single pcap file in a directory is a session
pcap, all other pcap files in the directory are also session pcaps.
Therefor the if clause checks if any of the pcap files in a given
directory is a session pcap. If true the directory is added to the list
of relevant directories.
"""
def gen_data_folders(PARENT_DIRECTORY):
    d = path(PARENT_DIRECTORY)
    l = []
    for root, dirs, files in os.walk(d):
        # if any(file.endswith('.hcl') for file in files) and any(is_pcap_session(file) for file in files):
        if any(is_pcap_session(join(root, file)) for file in files):
            l.append(path.abspath(root))
    return l

""" Returns a list of pcap file names from a given folder """
def gen_pcap_filenames(folder_name):
        # return [join(folder_name, f) for f in listdir(folder_name) if (isfile(join(folder_name, f)) and ('hcl' not in f) and ('pcap' in f)) ]
        file_names = [join(folder_name, f) for f in listdir(folder_name) if (isfile(join(folder_name, f)) and ('hcl' not in f) and (f.endswith('pcap'))) ]
        # print file_names
        return file_names


"""
Write a list of pcap file names to a given filename
DOES NOT WORK YET
"""
def write_pcap_filenames(filename_list, file_name):
        with open(file_name, "wb") as f:
            writer = csv.writer(f)
            writer.writerow(filename_list)


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
    elif os == 'Unknown':
        return 3


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
    elif tokens[0] == 'D':
        return 'OSX'
    else:
        return 'Unknown'

""" Return True if the given pcap is a session """
def is_pcap_session(pcap_path):
    if pcap_path.endswith('.pcap'):
        df = read_pcap(pcap_path, fields=['frame.time_epoch','ssl.handshake.extensions_server_name'])
        sni_count = len(df[df['ssl.handshake.extensions_server_name'].notnull()])
        if sni_count == 1:
            return True
    return False

""" Replace space with underscore for all folder and file names """
def space_to_underscore(ROOT_FOLDER):
        d = path(ROOT_FOLDER)


        for root, dirs, files in os.walk(d):
            # print 'In ' + repr(str(root))
            # print '================='

            for filename in os.listdir(root): # parse through file list in the current directory
                # print 'Filename: ' + repr(str(filename))
                # print '================='

            	if filename.find(" ") > 0: # if an underscore is found
                    newfilename = filename.replace(' ','_')
                    # print 'newfilename: ' + repr(str(newfilename))

                    os.rename(join(root, filename), join(root, newfilename))

"""
Parse a folder name and return the browser
Assumes the following format:
L_cyber_chrome_09-17__11_38_11
"""
def parse_folder_name_for_browser(folder_name):
    temp = folder_name.split(os.sep)
    temp.reverse()
    if folder_name.find("_chrome_") > 0: # if an underscore is found
            return 'Chrome'
    elif folder_name.find("_ff_") > 0: # if an underscore is found
            return 'FireFox'
    elif folder_name.find("_ie_") > 0: # if an underscore is found
            return 'IExplorer'
    elif folder_name.find("_Safari_") > 0: # if an underscore is found
            return 'Safari'
    else:
        return 'Unknown'
