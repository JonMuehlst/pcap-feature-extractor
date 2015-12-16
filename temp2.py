#!/usr/bin/env python

from utils.hcl_helpers import read_label_data

file_path = '/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/label_data.hcl'
os, browser, application, service = read_label_data(file_path)
print 'os: ' + os + ' browser: ' + browser + ' application: ' + application + ' service: ' + service
