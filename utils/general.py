import os
from path import path
from os import listdir
from os.path import isfile, join
from utils.read_pcap import read_pcap
import csv
import pandas as pd
import numpy as np
from collections import Counter
from conf import conf

def cleanup_pyc(DIRECTORY):
    d = path(DIRECTORY)
    files = d.walkfiles("*.pyc")
    for file in files:
        file.remove()
        print "Removed {} file".format(file)


"""
"""
def gen_label(pcap_path):
    label = 0
    label_type = conf.label_type()
    # assuming /path/to/pcap/123.pcap
    pcap_id = int(pcap_path.split(os.path.sep)[-1].split('.pcap')[0])
    if label_type == 'triple':
        sni_df = read_sni_csv(conf.sni_csv())
    	os_str, browser_str = parse_folder_name(pcap_path)
    	app_str = gen_app_name_by_sni(sni_df,gen_sni(pcap_path)[0])
    	label = gen_label_triple(os_str,browser_str,app_str)
    elif label_type == 'action':
        label = get_twitter_action_label(pcap_id)
    elif label_type == 'mobile_action':
        label = get_mobile_action_label(pcap_id)
    return label

"""
mobile action df format:
{'id': 123, 'label': '1'}
"""
def get_mobile_action_label(pcap_id):
    label_df = pd.read_csv(conf.label_df_path())
    return label_df[label_df['id'] == pcap_id]['label'].values[0]


"""
twitter action df format:
{'action': 'silence', 'side': 'follower', 'os': 'L', 'id': 412006, 'browser': 'firefox'}
"""
def get_twitter_action_label(pcap_id):
    label_df = pd.read_csv(conf.label_df_path())
    action_type = label_df[label_df['id'] == pcap_id]['action'].values[0]
    label = -1
    if action_type == 'silence':
        label = 0
    elif action_type == 'photo':
        label = 1
    elif action_type == 'text':
        label = 2
    return label

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
def gen_data_folders_sessions(PARENT_DIRECTORY):
    d = path(PARENT_DIRECTORY)
    l = []
    for root, dirs, files in os.walk(d):
        # if any(file.endswith('.hcl') for file in files) and any(is_pcap_session(file) for file in files):
        if any(is_pcap_session(join(root, file)) for file in files):
            l.append(path.abspath(root))
    return l

"""
"""
def gen_data_folders(PARENT_DIRECTORY):
    d = path(PARENT_DIRECTORY)
    l = []
    for root, dirs, files in os.walk(d):
        # if any(file.endswith('.hcl') for file in files) and any(is_pcap_session(file) for file in files):
        if any([1 for f in files if f.endswith('.pcap')]):
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
    os = { Linux, Windows, OSX, Unknown }
    browser = { Chrome, FireFox, IExplorer, Unknown }
    application = { Twitter, Youtube, Unknown }

    The input is non case sensitive
"""
def gen_label_triple(input_os, input_browser, input_application):

    input_os = input_os.lower()
    input_browser = input_browser.lower()
    input_application = input_application.lower()

    label = 10000

    if input_os == 'linux':
        label = label + 1
    elif input_os == 'windows':
        label = label + 2
    elif input_os == 'osx':
        label = label + 3
    elif input_os == 'unknown':
        label = label + 4

    if input_browser == 'chrome':
        label = label + 100
    elif input_browser == 'firefox':
        label = label + 200
    elif input_browser == 'iexplorer':
        label = label + 300
    elif input_browser == 'safari':
        label = label + 400
    elif input_browser == 'unknown':
        label = label + 500

    if input_application == 'dropbox':
        label = label + 1000
    elif input_application == 'facebook':
        label = label + 2000
    elif input_application == 'google':
        label = label + 3000
    elif input_application == 'microsoft':
        label = label + 4000
    elif input_application == 'teamviewer':
        label = label + 5000
    elif input_application == 'twitter':
        label = label + 6000
    elif input_application == 'youtube':
        label = label + 7000
    else:
        label = label + 8000

    return label


"""
Parse a folder name and return the os + browser
Currently returns os only.
Assumes the following format:
L_cyber_chrome_09-17__11_38_11
where folder_name is the full path i.e. /home/user/folder

Non case sensitive

Assuming the entire folder contains pcaps of the same os, browser
"""
def parse_folder_name(folder_name):
    temp = folder_name.split(os.sep)
    temp.reverse()
    tokens = temp[0].split('_')

    input_os = tokens[0].lower()
    input_browser = tokens[2].lower()

    os_str = ''
    browser_str = ''

    if input_os == 'l':
        os_str = 'Linux'
    elif input_os == 'w':
        os_str = 'Windows'
    elif input_os == 'd':
        os_str = 'OSX'
    else:
        """ TEMP """
        os_str = 'OSX'

    if input_browser == 'chrome':
        browser_str = 'Chrome'
    elif input_browser == 'ff':
        browser_str = 'Firefox'
    elif input_browser == 'firefox':
        browser_str = 'Firefox'
    elif input_browser == 'ie':
        browser_str = 'IExplorer'
    elif input_browser == 'safari':
        browser_str = 'Safari'

    return os_str, browser_str

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


""" Generate SNI csv from each pcap in root folder """
def gen_sni_csv(ROOT_FOLDER):
    d = path(ROOT_FOLDER)
    current_dir = os.getcwd()
    csv_file = current_dir + "/sni.csv"
    sni_list = []
    for root, dirs, files in os.walk(d):

        for filename in os.listdir(root):

            if filename.endswith(".pcap"):
                pcap_sni_list = gen_sni(root+"/"+filename)
                sni_list.extend(pcap_sni_list)

    sni_list = list(set(sni_list))
    with open(csv_file, "wb") as f:
            writer = csv.writer(f, delimiter='\n')
            writer.writerow(sni_list)

"""
Generate all SNI from specific pcap file
"""
def gen_sni(filename):
    pcap_sni_list = []
    #
    df = read_pcap(filename=filename, fields=['ssl.handshake.extensions_server_name'] , dtype = {'ssl.handshake.extensions_server_name':'string'})
    df = df[df['ssl.handshake.extensions_server_name'].notnull()]
    for index, row in df.iterrows():

        val = str(row['ssl.handshake.extensions_server_name'])
        pcap_sni_list.append(val)

    pcap_sni_list.append('unknwon')
    return pcap_sni_list

"""
Get sni_df
Return app_name
"""
def gen_app_name_by_sni(df, sni):
    app_name =df.loc[df['sni'] == sni]['app_name']
    if len(app_name) == 0:
        return 'unknown'
    else:
        return app_name.iloc[0]

"""
Read sni csv and return sni data frame
"""
def read_sni_csv(sni_csv):
    df = pd.read_csv(sni_csv,names=['sni','app_name'])
    df.fillna('unknwon')
    return df

""" Show duplicates in an array """
def show_dups(array):
    print repr([item for item, count in Counter(array).iteritems() if count > 1])

"""  """
def write_data_folders_to_file(file_name, PARENT_DIRECTORY):
    l = gen_data_folders(PARENT_DIRECTORY)

    with open(file_name, 'wb') as csvfile:
      writer = csv.writer(csvfile, delimiter=',')
      writer.writerow(l)
