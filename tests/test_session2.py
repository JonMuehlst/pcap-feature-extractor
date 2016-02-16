#!/usr/bin/env python

from containers.Flow import Flow
from containers.Session import Session
import unittest
import pandas as pd
import os
import subprocess
from conf import conf
import numpy as np

"""
FIX:
The data is recreated for each test
"""

class TestSession2(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sstr = os.getcwd() + '/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_35015_192-229-233-25_443.pcap'
		sstr2 = os.getcwd() + '/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_34965_192-229-233-25_443.pcap'
		fields = conf.fields()
		cls.s = Session.from_filename(sstr, fields=fields)
		cls.s2 = Session.from_filename(sstr2, fields=fields)
		cmd = 'tshark -r /home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_35015_192-229-233-25_443.pcap -T fields -E occurrence=a -E aggregator=, -e frame.time_epoch -e frame.time_delta -e frame.len -e frame.cap_len -e frame.marked -e ip.src -e ip.dst -e ip.len -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum_good -e tcp.srcport -e tcp.dstport -e tcp.len -e tcp.nxtseq -e tcp.hdr_len -e tcp.flags.cwr -e tcp.flags.urg -e tcp.flags.push -e tcp.flags.syn -e tcp.window_size -e tcp.checksum -e tcp.checksum_good -e tcp.checksum_bad -e tcp.analysis.keep_alive -e tcp.analysis.keep_alive_ack'
		cls.table = subprocess.check_output(cmd.split()).splitlines()


	"""
	def setUp(self):
		self.s = Session(self.sess_frame)
	"""

	def test_len(self):
		# print '===='
		# print 'tshark output lines: ' + repr(len(self.table))
		# print '===='
		for i in range(1000):
			self.assertEqual(len(self.s), 5890)
			# self.assertEqual(len(self.s), 196)

	def test_mean(self):
		self.assertAlmostEqual(self.s2.mean_packet_size(), 824.8367346939)

	def test_variance(self):
		self.assertAlmostEqual(self.s2.sizevar(), 867079.583464156)

	def test_size(self):
		self.assertEqual(self.s2.size(), 161668)

	def test_max_packet_size(self):
		self.assertEqual(self.s2.max_packet_size(), 4110)

	def test_min_packet_size(self):
		self.assertEqual(self.s2.min_packet_size(), 66)

	def test_packet_count(self):
		self.assertEqual(self.s2.packet_count(), 196)

	def test_bpackets(self):
		self.assertEqual(self.s2.bpackets(), 98)

	def test_bbytes(self):
		self.assertEqual(self.s2.bbytes(), 153729)

	def test_min_biat(self):
		self.assertAlmostEqual(self.s2.min_biat(), 0.000003)

	def test_max_biat(self):
		self.assertAlmostEqual(self.s2.max_biat(), 0.095984)

	def test_std_biat(self):
		self.assertAlmostEqual(self.s2.std_biat(), 0.023467158)

	def test_mean_biat(self):
		self.assertAlmostEqual(self.s2.mean_biat(), 0.0077052551)

	def test_min_bpkt(self):
		self.assertEqual(self.s2.min_bpkt(), 66)

	def test_max_bpkt(self):
		self.assertEqual(self.s2.max_bpkt(), 4110)

	def test_std_bpkt(self):
		self.assertAlmostEqual(self.s2.std_bpkt(), 787.6863411528)

	def test_mean_bpkt(self):
		self.assertAlmostEqual(self.s2.mean_bpkt(), 1568.6632653061)

	def test_mean_fttl(self):
		np.testing.assert_array_equal(self.s2.mean_fttl(), [1,0])

	def test_keep_alive(self):
		self.assertEqual(self.s.num_keep_alive(), 3)

	def test_back_peak_features(self):
		bpeak_features = self.s2.bpeak_features()
		np.testing.assert_array_almost_equal(bpeak_features, [183, 0, 368, 172.5961429796, 8, 6.34664, 0.077698, 30.152365, 11.8889010853])

	def test_fSSLv(self):
		# 0x0301 - TLS1_V - [0, 1, 0, 0]
		np.testing.assert_array_equal(self.s2.fSSLv(), [0, 1, 0, 0])

	# def test_bSSLv(self):
	# 	# 0x0303 - TLS12_V - [0, 0, 0, 1]
	# 	np.testing.assert_array_equal(self.s2.bSSLv(), [0, 0, 0, 1])

	def test_fcipher_suites(self):
		# self.assertEqual(self.s2.fcipher_suites(), 13)
		np.testing.assert_array_equal(self.s2.fcipher_suites(), [0, 1, 0])


if __name__ == '__main__':
	unittest.main()
