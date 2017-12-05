from containers.ContainerWrapper import ContainerWrapper
from utils.general import gen_pt_csv_filenames, gen_data_folders, gen_label_triple, read_sni_csv, gen_app_name_by_sni
from utils.general import gen_label, get_pcap_id
from utils.hcl_helpers import read_label_data
from functools import partial
# from multiprocessing import Pool
import pathos.multiprocessing as mp
# from pathos.multiprocessing import ProcessingPool
import numpy as np
import pandas as pd
from conf import conf
import os

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
	def __init__(self):
		print 'Initializing...'
		PARENT_DIRECTORY = conf.input_directory()
		# self.p = Pool(16)
		self.p = mp.ProcessingPool(16)
		# self.data_folders = gen_data_folders(PARENT_DIRECTORY)
		self.data_folders = conf.get_data_folders()
		self.feature_methods = conf.features()
		self.all_samples = np.array([])
		print 'Done Initializing'


	""" Return a list of sample feature vectors for a given child data directory """
	def sessions_to_samples(self, CHILD_DIRECTORY):
		print 'In: ' + repr(str(CHILD_DIRECTORY))
		only_pcap_files = gen_pt_csv_filenames(CHILD_DIRECTORY)
		if len(only_pcap_files) > 0:
			samples = self.p.map(self.pcap_to_feature_vector, only_pcap_files)
			# samples = map(self.pcap_to_feature_vector, only_pcap_files)
			return samples
		return np.array([])


	"""
	Dynamically call feature methods and generate feature vector from pcap file
	"""
	def pcap_to_feature_vector(self, pcap_path):
		# print 'Processing: ' + repr(str(pcap_path))
		# pcap_id = pcap_path.split(os.path.sep)[-1].split('.pcap')[0]
		cont_wrap = ContainerWrapper(pcap_path)
		label = gen_label(pcap_path)
		pcap_id = get_pcap_id(pcap_path)
		feature_vector = np.array([int(pcap_id)])
		# feature_vector = np.array([])
		# feature_vector = np.array([pcap_path.split(os.path.sep)[-1]])
		for method_name in self.feature_methods:
			method = getattr(cont_wrap, method_name)
			if not method:
			    raise Exception("Method %s not implemented" % method_name)
			feature_vector = np.append(feature_vector, method())
		feature_vector = np.append(feature_vector, label)
		# If the sample contains NaN values remove the pcap file
		# if  np.isnan(np.sum(feature_vector)):
		# 	os.remove(pcap_path)

		return feature_vector


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
		# sdf.to_csv(file_name, sep=separator, index=0, header=False)
		# sdf = sdf.dropna()
		sdf.to_csv(file_name, sep=separator)
