#!/usr/bin/env python

from containers.Flow import Flow
from containers.Session import Session
import unittest
import pandas as pd
import numpy as np
import os
import subprocess
from conf import conf



"""
Input file
L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_33521_212-179-154-238_443.pcap
ip.ttl == 64 ; for Linux
ip.ttl == 128 ; for Windows
"""
class TestOurFeatures(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		sstr = os.getcwd()
		Linux_pcap = sstr + '/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_33521_212-179-154-238_443.pcap'
		Win_pcap = sstr + '/data/W_Pc_ie_09-17__11_38_10/W_Pc_ie_09-17__11_38_10.pcap.TCP_10-0-0-16_49191_104-244-43-167_443.pcap'
		fields = conf.fields()
		cls.linux = Session.from_filename(Linux_pcap, fields=fields)
		cls.win = Session.from_filename(Win_pcap, fields=fields)


	def test_client_hello_ttl_Linux(self):
		self.assertEqual(self.linux.mean_fttl().all(), np.array([1,0]).all())
		np.testing.assert_array_equal(self.linux.mean_fttl(), np.array([1,0]))

	def test_client_hello_ttl_Windows(self):
		self.assertEqual(self.win.mean_fttl().all(), np.array([0,1]).all())
		np.testing.assert_array_equal(self.win.mean_fttl(), np.array([0,1]))


""" ============================================= """
class TestSession1(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
			pass

	def setUp(self):
		columns = conf.fields()
		self.df1 = pd.DataFrame(np.zeros((5,len(columns))), columns=columns)
		self.df2 = pd.DataFrame(np.zeros((4,len(columns))), columns=columns)
		self.df1['frame.len'] = [10,100,60,40,200]
		self.df2['frame.len'] = [30,70,300,100]
		self.df1['ip.src'] = ['10.1.0.2','10.1.0.2','10.1.0.2','10.1.0.2','10.1.0.2']
		self.df1['ip.dst'] = ['8.8.8.8','8.8.8.8','8.8.8.8','8.8.8.8','8.8.8.8']
		self.df1['tcp.srcport'] = ['2222','2222','2222','2222','2222']
		self.df1['tcp.dstport'] = ['443','443','443','443','443']
		self.df2['ip.src'] = ['8.8.8.8','8.8.8.8','8.8.8.8','8.8.8.8']
		self.df2['ip.dst'] = ['10.1.0.2','10.1.0.2','10.1.0.2','10.1.0.2']
		self.df2['tcp.srcport'] = ['443','443','443','443']
		self.df2['tcp.dstport'] = ['2222','2222','2222','2222']
		self.sess_frame = pd.concat((self.df1, self.df2), ignore_index=True)
		self.s = Session(self.sess_frame)

	def test_len(self):
		self.assertEqual(len(self.s), 9)

	def test_mean(self):
		self.assertAlmostEqual(self.s.mean_packet_size(), 101.11111111)

	def test_variance(self):
		self.assertAlmostEqual(self.s.sizevar(), 8636.11111111)

	def test_min_packet_size(self):
		self.assertAlmostEqual(self.s.min_packet_size(), 10)

	def test_max_packet_size(self):
		self.assertAlmostEqual(self.s.max_packet_size(), 300)

	def test_size_histogram(self):
		np.testing.assert_array_equal(self.s.size_histogram(), [7, 2, 0, 0, 0, 0, 0, 0, 0, 0])


""" ============================================= """
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

	def test_SYN_tcp_winsize(self):
		self.assertEqual(self.s2.SYN_tcp_winsize(), 29200)

	def test_SYN_MSS(self):
		self.assertEqual(self.s2.SYN_MSS(), 1460)

	def test_SYN_tcp_scale(self):
		self.assertEqual(self.s2.SYN_tcp_scale(), 7)

	def test_fSSL_num_compression_methods(self):
		self.assertEqual(self.s2.fSSL_num_compression_methods(), 1)

	def test_fSSL_session_id_len(self):
		self.assertEqual(self.s2.fSSL_session_id_len(), 32)

	def test_fSSL_num_extensions(self):
		self.assertEqual(self.s2.fSSL_num_extensions(), 10)


if __name__ == '__main__':
	unittest.main()
