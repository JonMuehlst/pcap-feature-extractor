from containers.Session import Session
import numpy as np

"""
Dynamically call feature methods and generate feature vector from pcap file
"""
def pcap_to_feature_vector(pcap_path, feature_methods=['packet_count', 'sizemean', 'sizevar'], label=1):
	sess = Session.from_filename(pcap_path)
	feature_vector = np.array([])
	for method_name in feature_methods:
		method = getattr(sess, method_name)
		if not method:
		    raise Exception("Method %s not implemented" % method_name)
		feature_vector = np.append(feature_vector, method())
	feature_vector = np.append(feature_vector, label)
	return feature_vector
