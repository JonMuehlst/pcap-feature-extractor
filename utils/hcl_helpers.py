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
