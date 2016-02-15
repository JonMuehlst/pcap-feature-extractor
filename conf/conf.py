from utils.hcl_helpers import read_hcl
import os


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
