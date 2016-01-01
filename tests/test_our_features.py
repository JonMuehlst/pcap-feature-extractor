#!/usr/bin/env python

from containers.Flow import Flow
from containers.Session import Session
import unittest
import pandas as pd
import numpy as np
import os
import subprocess

"""
Input file
L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_33521_212-179-154-238_443.pcap
ip.ttl == 64 ; for Linux
ip.ttl == 128 ; for Windows
"""

class TestOutFeatures(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sstr = os.getcwd()
		Linux_pcap = sstr + '/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_33521_212-179-154-238_443.pcap'
		Win_pcap = sstr + '/data/W_Pc_ie_09-17__11_38_10/W_Pc_ie_09-17__11_38_10.pcap.TCP_10-0-0-16_49191_104-244-43-167_443.pcap'
		cls.linux = Session.from_filename(Linux_pcap)
		cls.win = Session.from_filename(Win_pcap)


	def test_client_hello_ttl_Linux(self):
		self.assertEqual(self.linux.mean_fttl().all(), np.array([1,0]).all())
		np.testing.assert_array_equal(self.linux.mean_fttl(), np.array([1,0]))

	def test_client_hello_ttl_Windows(self):
		self.assertEqual(self.win.mean_fttl().all(), np.array([0,1]).all())
		np.testing.assert_array_equal(self.win.mean_fttl(), np.array([0,1]))


if __name__ == '__main__':
	unittest.main()
