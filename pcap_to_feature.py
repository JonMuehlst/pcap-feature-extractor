from Session import Session
import numpy as np

""" 
FIX - Doing manual work, get a list parameter contatining desired features
"""

def pcap_to_feature(pcap_path, label):
	sess = Session.from_filename(pcap_path)
	return np.array([len(sess), sess.sizemean(), sess.sizevar(), label])
