#inherits from Packet_container

from PacketContainer import PacketContainer
from utils.read_pcap import read_pt_csv
from conf import conf

import os
import pandas as pd
import numpy as np
import numbers

class UniversalSample(PacketContainer):

    def __init__(self, s, path_str=None):
        self.df = s
        self.pcap_path = path_str

        """ Transport layer protocol """
        if len(self.df[self.df['tcp.srcport'].notnull()]) > 0:
            self.transport_proto = TCP_PROTOCOL
        elif len(self.df[self.df['udp.srcport'].notnull()]) > 0:
            self.transport_proto = UDP_PROTOCOL


    @classmethod
    def from_filename(cls, path_str):
        segment = read_pt_csv(path_str)
        return cls(segment,path_str)


    def get_df():
        return self.df

    def transport_protocol(self):
        return self.transport_proto


    def size(self):
        """
        Size of all packets in bytes
        """
        return self.df['frame.len'].sum()


    def __len__(self):
        """
        Amount of packets
        """
        return len(self.df)


    def packet_count(self):
        """
        Total number of packets
        """
        return len(self)


    def get_segment_df(self):
        """
        Get the segment DataFrame
        """
        return self.df


    def mean_packet_size(self):
        """
        Mean of packet size
        """
        if len(self.df) == 0:
            return 0
        if len(self.df) == 1:
            return self.df['frame.len'].values[0]
        return self.df['frame.len'].mean()


    def sizevar(self):
        """
        Variance of packet size
        """
        if len(self.df) < 2:
            return 0
        return self.df['frame.len'].var()


    def max_packet_size(self):
        """
        Max packet size
        """
        return self.df['frame.len'].max()


    def min_packet_size(self):
        """
        Min packet size
        """
        return self.df['frame.len'].min()


    def std_time_delta(self):
        """
        Return unbiased standard deviation of the packet flow time deltas.
        Normalized by N-1 by default. This can be changed using the
        ddof argument - pandas
        """
        if len(self.df['frame.time_delta']) < 2:
            return 0
        return self.df['frame.time_delta'].std()


    def min_time_delta(self):
        """
        Min time delta
        """
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


    def peak_features(self):
        """

        TODO: Implement transport protocol agnostic peak analysis

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
        pass



    def size_histogram(self):
        """
        Packet size histogram of 10 bins

        The original Ethernet IEEE 802.3 standard defined the minimum Ethernet
        frame size as 64 bytes and the maximum as 1518 bytes.
        The maximum was later increased to 1522 bytes to allow for VLAN tagging.
        The minimum size of an Ethernet frame that carries an
        ICMP packet is 74 bytes.
        """
        hist = np.histogram(self.df['frame.len'], bins=[ 0.,   160.,   320.,
                                                        480.,   640.,   800.,
                                                        960.,  1120., 1280.,
                                                        1440.,  1600. ])
        return hist[0]
