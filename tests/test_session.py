#!/usr/bin/env python

from containers.Flow import Flow
from containers.Session import Session
import unittest
import pandas as pd

""" 
FIX: 
The data is recreated for each test 
"""

class TestSession(unittest.TestCase):
	
	def setUp(self):
		columns = [
		'frame.time_epoch',
		'frame.time_delta',
		'frame.len',
		'frame.cap_len',
		'frame.marked',
		'ip.src', 
		'ip.dst',
		'ip.len',
		'ip.flags',
		'ip.flags.rb',
		'ip.flags.df',
		'ip.flags.mf',
		'ip.frag_offset',
		'ip.ttl', 
		'ip.proto',
		'ip.checksum_good',
		'tcp.srcport',
		'tcp.dstport',
		'tcp.len', 
		'tcp.nxtseq', 
		'tcp.hdr_len',
		'tcp.flags.cwr',
		'tcp.flags.urg',
		'tcp.flags.push',
		'tcp.flags.syn',
		'tcp.window_size',
		'tcp.checksum',
		'tcp.checksum_good',
		'tcp.checksum_bad',
		]
		self.df1 = pd.DataFrame(index=range(5), columns=columns)
		self.df2 = pd.DataFrame(index=range(4), columns=columns)
		self.df1['tcp.len'] = [10,100,60,40,200]
		self.df2['tcp.len'] = [30,70,300,100]
		self.sess_frame = pd.concat((self.df1, self.df2), ignore_index=True)		
		self.s = Session(self.sess_frame)
	
	def test_len(self):
		self.assertEqual(len(self.s), 9)

	def test_mean(self):
		self.assertAlmostEqual(self.s.sizemean(), 101.11111111)

	def test_variance(self):
		self.assertAlmostEqual(self.s.sizevar(), 8636.11111111)

if __name__ == '__main__':
	unittest.main()
