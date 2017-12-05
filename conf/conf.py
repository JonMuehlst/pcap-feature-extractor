from utils.hcl_helpers import read_hcl
import os
import csv
from path import path


"""
Assuming conf.hcl lives in the apps' root directory
"""

# SSLv3/TLS versions
SSL3_V = 0x0300
TLS1_V = 0x0301
TLS11_V = 0x0302
TLS12_V = 0x0303

client_hello_num = 1
server_hello_num = 2


""" Globals """
conf_filename = 'conf.hcl'
conf_file_full_path = os.getcwd() + os.path.sep + conf_filename
""" Globals """

"""
"""
def label_type():
    f = read_hcl(conf_file_full_path)
    return f['conf']['label_type']

"""
"""
def id_table_path():
    f = read_hcl(conf_file_full_path)
    return f['conf']['id_table_path']

"""
"""
def label_df_path():
    f = read_hcl(conf_file_full_path)
    return f['conf']['label_df_path']

"""
"""
def get_data_folders():
    f = read_hcl(conf_file_full_path)
    sample_type = f['conf']['sample_type']

    if sample_type == 'session':
        filename = session_data_folders_filename()
    elif sample_type == 'time_segment':
        filename = time_segment_data_folders_filename()
    if sample_type == 'traffic_type':
        filename = session_data_folders_filename()

    l = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for col in row:
                dir_val = str(col)
                l.append(os.path.abspath(dir_val))

    return l


"""
"""
def get_temp_folder():
    f = read_hcl(conf_file_full_path)
    return f['conf']['temp_folder']

"""
"""
def sample_type():
    f = read_hcl(conf_file_full_path)
    return f['conf']['sample_type']


"""
Rename space to underscore?
"""
def space_to_underscore():
    f = read_hcl(conf_file_full_path)
    flag_var = f['conf']['rename_space_underscore']
    return flag_var


"""
Generate fields list
"""
def fields():
    f = read_hcl(conf_file_full_path)
    fields = [ str(field) for field in f['conf']['fields'] ]
    return fields


"""
Generate features list
"""
def features():
    f = read_hcl(conf_file_full_path)
    features = [ str(feature) for feature in f['conf']['features'] ]
    return features


"""
Generate data source directory
"""
def input_directory():
    f = read_hcl(conf_file_full_path)
    input_directory = str(f['conf']['data'])
    return input_directory


"""
Generate output filename
"""
def output_filename():
    f = read_hcl(conf_file_full_path)
    output_filename = str(f['conf']['output'])
    return output_filename


"""
Generate sni_csv
"""
def sni_csv():
    f = read_hcl(conf_file_full_path)
    sni_csv = str(f['conf']['sni_csv'])
    return sni_csv


"""
Generate Session data Folders - Include only folders containing sessions

Notice - If one session pcap is contained in a folder it is added to the list.
         Do not mix session pcaps with non-session pcaps
"""
def session_data_folders_filename():
    f = read_hcl(conf_file_full_path)
    filename = str(f['conf']['session_folders_filename'])
    return filename

""" Get Session Data folders list """
def get_session_data():
    filename = session_data_folders_filename()
    l = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            for col in row:
                dir_val = str(col)
                l.append(os.path.abspath(dir_val))

    return l

"""
"""
def time_segment_data_folders_filename():
    f = read_hcl(conf_file_full_path)
    filename = str(f['conf']['time_segment_folders_filename'])
    return filename
