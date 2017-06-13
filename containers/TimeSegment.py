#inherits from Packet_container

from PacketContainer import PacketContainer
from utils.read_pcap import read_pcap
from conf import conf

import os
import pandas as pd
import numpy as np
import numbers

class TimeSegment(PacketContainer):

    def __init__(self, s, path_str=None):
        self.df = s
        self.pcap_path = path_str


    """ Whats the difference between this function and the ctor? """
    @classmethod
    def from_filename(cls, path_str, fields=['frame.time_epoch', 'frame.time_delta', 'frame.len', 'frame.cap_len', 'frame.marked', 'ip.src', 'ip.dst', 'ip.len', 'ip.flags', 'ip.flags.rb', 'ip.flags.df', 'ip.flags.mf', 'ip.frag_offset', 'ip.ttl', 'ip.proto', 'ip.checksum_good', 'tcp.srcport', 'tcp.dstport', 'tcp.len', 'tcp.nxtseq', 'tcp.hdr_len', 'tcp.flags.cwr', 'tcp.flags.urg', 'tcp.flags.push', 'tcp.flags.syn' ,'tcp.window_size','tcp.checksum','tcp.checksum_good', 'tcp.checksum_bad']):
        # segment = gen_data_frame(path_str)
        segment = read_pcap(path_str,fields=fields)
        return cls(segment,path_str)

    """ Size of all packets in bytes """
    def size(self):
        return self.df['frame.len'].sum()

    """ Amount of packets """
    def __len__(self):
        return len(self.df)

    """ Total number of packets """
    def packet_count(self):
        return len(self)

    """ Get the segment DataFrame """
    def get_segment_df(self):
        return self.df

    """ Mean of packet size """
    def mean_packet_size(self):
        if len(self.df) == 0:
            return 0
        if len(self.df) == 1:
            return self.df['frame.len'].values[0]
        return self.df['frame.len'].mean()

    """ Variance of packet size """
    def sizevar(self):
        if len(self.df) < 2:
            return 0
        return self.df['frame.len'].var()

    """ Max packet size """
    def max_packet_size(self):
        return self.df['frame.len'].max()

    """ Min packet size """
    def min_packet_size(self):
        return self.df['frame.len'].min()

    """
    Return unbiased standard deviation of the packet flow time deltas.
    Normalized by N-1 by default. This can be changed using the ddof argument - pandas
    """
    def std_time_delta(self):
        if len(self.df['frame.time_delta']) < 2:
            return 0
        return self.df['frame.time_delta'].std()

    """ Min time delta """
    def min_time_delta(self):
        return self.df['frame.time_delta'].min()

    """ Max time delta """
    def max_time_delta(self):
        return self.df['frame.time_delta'].max()

    """ time delta mean """
    def mean_time_delta(self):
        if len(self.df) == 0:
            return 0
        if len(self.df) == 1:
            return self.df['frame.time_delta'].values[0]
        return self.df['frame.time_delta'].mean()



    """
    Our features
    """

    """
    Peak features:
           peak mean
           peak min
           peak max
           peak std
           Number Of peaks

           peak inter arrival time std
           peak inter arrival time mean
           peak inter arrival time min
           peak inter arrival time max

    """
    def peak_features(self):

        self.df['tcp.ack'].fillna(0)

        """ Add a column stating whether a certain packet represents a peak """
        self.df['isPeak'] = np.where(self.df['frame.time_delta'] > 0.05, True, False)

        """ A DataFrame containing only peak representing packets """
        peak_df = self.df[self.df['isPeak'] == True]

        """ Getting rid of RST packets which cause undesired behaviour (negative ack diffs)"""
        peak_df = peak_df[peak_df['tcp.flags.reset'] == False]

        """ For every trailing couple of peak representing packets (rows) compute the difference """
        peak_diff_ack = peak_df['tcp.ack'].diff()

        """ Peak inter arrival times """
        piat = peak_df['frame.time_epoch'].diff()

        """ Remove first value since peaks are num (representing) packets - 1 """
        peak_diff_ack = peak_diff_ack[1:]

        """ Same for piat """
        piat = piat[1:]

        if len(peak_df) > 0 :
            """ Features """

            peak_mean = 0
            peak_min = 0
            peak_max = 0
            peak_std = 0
            num_of_peaks = 0
            piat_mean = 0
            piat_min = 0
            piat_max = 0
            piat_std = 0


            if len(peak_diff_ack) > 0:
                if len(peak_diff_ack) == 1:
                    peak_mean = peak_diff_ack.values[0]
                    peak_min = peak_diff_ack.min()
                    peak_max = peak_diff_ack.max()
                    num_of_peaks = len(peak_diff_ack)
                else:
                    peak_mean = peak_diff_ack.mean()
                    peak_min = peak_diff_ack.min()
                    peak_max = peak_diff_ack.max()
                    peak_std = peak_diff_ack.std()
                    num_of_peaks = len(peak_diff_ack)

            if len(piat) > 0:
                if len(piat) == 1:
                    piat_mean = piat.values[0]
                    piat_min = piat.min()
                    piat_max = piat.max()
                else:
                    piat_mean = piat.mean()
                    piat_min = piat.min()
                    piat_max = piat.max()
                    piat_std = piat.std()

            feature_arr = np.array([peak_mean, peak_min, peak_max, peak_std, num_of_peaks, piat_mean, piat_min, piat_max, piat_std])

        else:
            feature_arr = np.zeros(9)


        return feature_arr


    """
    Packet size histogram of 10 bins

    The original Ethernet IEEE 802.3 standard defined the minimum Ethernet frame size as 64 bytes
    and the maximum as 1518 bytes.
    The maximum was later increased to 1522 bytes to allow for VLAN tagging.
    The minimum size of an Ethernet frame that carries an ICMP packet is 74 bytes.
    """
    def size_histogram(self):
        hist = np.histogram(self.df['frame.len'], bins=[ 0.,   160.,   320.,   480.,   640.,   800.,   960.,  1120., 1280.,  1440.,  1600. ])
        return hist[0]
