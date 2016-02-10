"""
Read / Write hcl files
"""
import hcl
import os

""" Returns a JSON object """
def read_hcl(file_name):
    with open(file_name, 'r') as fp:
        return hcl.load(fp)

""" """
def read_label_data(file_name):
    obj = read_hcl(file_name)
    label_data = obj['label_data']
    os = str(label_data['os'])
    browser = str(label_data['browser'])
    application = str(label_data['application'])
    service = str(label_data['service'])
    return os, browser, application, service

"""
Generate fields, features lists and data source directory from the conf.hcl file.
Assuming conf.hcl lives in the apps' root directory
"""
def parse_conf():
    f = read_hcl(os.getcwd() + '/' + 'conf.hcl')
    fields = [ str(field) for field in f['conf']['fields'] ]
    features = [ str(feature) for feature in f['conf']['features'] ]
    input_directory = str(f['conf']['data'])
    output_filename = str(f['conf']['output'])
    return fields, features, input_directory, output_filename
