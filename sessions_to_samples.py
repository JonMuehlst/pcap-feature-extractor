from os import listdir
from os.path import isfile, join
from pcap_to_feature_vector import pcap_to_feature_vector

"""
FIX:
Add a function which adds a feature_methods list and a label to each file_name
"""

def sessions_to_samples(folder_name):
    only_pcap_file = [join(folder_name, f) for f in listdir(folder_name) if (isfile(join(folder_name, f)) and ('hcl' not in f)) ]
    for f in only_pcap_file:
        print repr(f)
        print
    samples = map(pcap_to_feature_vector, only_pcap_file)
    for sample in samples:
        print repr(sample)
        print
