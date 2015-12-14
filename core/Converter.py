from containers.Session import Session
from utils.general import gen_pcap_filenames, gen_data_folders
import numpy as np


"""
FIX:
"""
"""
Instructions:
	1. Create a converter object
	2. activate
	3. Access / get / write data
"""
class Converter(object):

	def __init__(self, PARENT_DIRECTORY, feature_methods_list=['packet_count', 'sizemean', 'sizevar']):
		self.data_folders = gen_data_folders(PARENT_DIRECTORY)
		self.feature_methods = feature_methods_list
		self.all_samples = np.array([])

	"""
	Dynamically call feature methods and generate feature vector from pcap file
	"""
	def pcap_to_feature_vector(self, pcap_path, label=1):
		sess = Session.from_filename(pcap_path)
		feature_vector = np.array([])
		for method_name in self.feature_methods:
			method = getattr(sess, method_name)
			if not method:
			    raise Exception("Method %s not implemented" % method_name)
			feature_vector = np.append(feature_vector, method())
		feature_vector = np.append(feature_vector, label)
		return feature_vector


	""" Return a list of sample feature vectors for a given child data directory """
	def sessions_to_samples(self, CHILD_DIRECTORY):
		only_pcap_files = gen_pcap_filenames(CHILD_DIRECTORY)
		samples = map(self.pcap_to_feature_vector, only_pcap_files)
		return samples


	""" Push the button """
	def activate(self):
		samples = map(self.sessions_to_samples, self.data_folders)
		self.all_samples = np.concatenate(samples)

	"""  """
	def get_samples(self):
		return self.all_samples

	""" TEST THIS ... [] operator """
	def __getitem__(self,index):
		return self.all_samples[index]


	""" TEST THIS ... return an iterator """
	def __iter__(self):
		return iter(self.all_samples)
