#!/usr/bin/env python

from read_pcap import *
from Flow import Flow
from Session import Session
from pcap_to_feature import *
import pandas as pd
import numpy as np

pcap1_path = '/home/jon/workspace/fe/data/t.pcap'
pcap2_path = '/home/jon/workspace/fe/data/t2.pcap'

p1 = gen_data_frame(pcap1_path)
#p2 = gen_data_frame(pcap2_path)

fp1, fp2 = gen_flows(p1)

#print fp1[['ip.src','ip.dst']]
#print 
#print fp2[['ip.src','ip.dst']]

f1 = Flow(fp1)
f2 = Flow(fp2)


""" """
np.set_printoptions(precision=2, suppress=True)
sample = pcap_to_feature('/home/jon/workspace/fe/data/t.pcap',1)


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
