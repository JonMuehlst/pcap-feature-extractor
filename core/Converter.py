from containers.Session import Session
from utils.general import gen_pcap_filenames, gen_data_folders, parse_folder_name, gen_label_triple
from utils.hcl_helpers import read_label_data
from functools import partial
from multiprocessing import Pool
import numpy as np
import pandas as pd



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
	""" FIX - Fix default feature_methods_list """
	def __init__(self, PARENT_DIRECTORY, feature_methods_list=['packet_count', 'sizemean', 'sizevar'], fields_list=[]):
		print 'Initializing...'
		print
		self.p = Pool(16)
		self.data_folders = gen_data_folders(PARENT_DIRECTORY)
		self.feature_methods = feature_methods_list
		self.fields = fields_list
		self.all_samples = np.array([])
		print 'Done Initializing'

	"""
	Dynamically call feature methods and generate feature vector from pcap file
	"""
	def pcap_to_feature_vector(self, pcap_path, label=1):
		# print 'Processing: ' + repr(str(pcap_path))
		sess = Session.from_filename(pcap_path, fields=self.fields)
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
		print 'In: ' + repr(str(CHILD_DIRECTORY))
		only_pcap_files = gen_pcap_filenames(CHILD_DIRECTORY)
		if len(only_pcap_files) > 0:
			""" IMPLEMENT """
			# label_data_file = get_label_data_hcl_file()
			# label = gen_label_triple(label_data_file)
			os_str, browser_str = parse_folder_name(CHILD_DIRECTORY)
			label = gen_label_triple(os_str,browser_str,'')
			func = partial(self.pcap_to_feature_vector, label=label)
			samples = map(func, only_pcap_files)
			return samples
		return np.array([])


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

	""" Write samples to csv """
	def write_to_csv(self, file_name, separator):
		sdf = pd.DataFrame(self.all_samples)
		sdf.to_csv(file_name, sep=separator, index=False)
