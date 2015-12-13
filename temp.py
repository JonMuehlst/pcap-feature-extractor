#!/usr/bin/env python

from utils.read_pcap import gen_data_frame, gen_flows
from utils.general import gen_data_folders
from containers.Flow import Flow
from containers.Session import Session
from core.Converter import Converter
import pandas as pd
import numpy as np
import os
from os.path import join


np.set_printoptions(precision=2, suppress=True)

"""
pcap1_path = '/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_33521_212-179-154-238_443.pcap'
pcap2_path = '/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_34965_192-229-233-25_443.pcap'

p1 = gen_data_frame(pcap2_path)
#p2 = gen_data_frame(pcap2_path)

fp1, fp2 = gen_flows(p1)

#print fp1[['ip.src','ip.dst']]
#print
#print fp2[['ip.src','ip.dst']]

f1 = Flow(fp1)
f2 = Flow(fp2)


""" """
sample = pcap_to_feature_vector(pcap2_path, ['packet_count', 'sizemean', 'sizevar'],1)


print len(f1)
print len(f2)
print 'min packet size'
print f1.min_packet_size()
print f2.min_packet_size()
print 'mean'
print f1.sizemean()
print f2.sizemean()
print 'variance'
print f1.sizevar()
print f2.sizevar()
print 'sum bytes'
print f1.size()
print f2.size()
print '--------'
print repr(sample)
"""

#sessions_to_samples('/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11')

#gen_data_folders('/home/jon/workspace/pcap-feature-extractor/data')
sstr = os.getcwd()
sstr = sstr + '/data'
gen_data_folders(sstr)

conv = Converter(sstr)
conv.activate()
for sample in conv:
    print sample
