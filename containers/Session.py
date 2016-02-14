#inherits from Packet_container

from PacketContainer import PacketContainer
from utils.read_pcap import gen_data_frame, gen_flows_up_down, read_pcap
from containers.Flow import Flow
import pandas as pd
import numpy as np

"""
FIX:
"""

"""
Class fields:
sess - Session DataFrame
"""

class Session(PacketContainer):

    def __init__(self, s):
        self.flow_up, self.flow_down = gen_flows_up_down(s)
        self.flow_up, self.flow_down = Flow(self.flow_up), Flow(self.flow_down)


    """ Whats the difference between this function and the ctor? """
    @classmethod
    def from_filename(cls, path_str, fields=['frame.time_epoch', 'frame.time_delta', 'frame.len', 'frame.cap_len', 'frame.marked', 'ip.src', 'ip.dst', 'ip.len', 'ip.flags', 'ip.flags.rb', 'ip.flags.df', 'ip.flags.mf', 'ip.frag_offset', 'ip.ttl', 'ip.proto', 'ip.checksum_good', 'tcp.srcport', 'tcp.dstport', 'tcp.len', 'tcp.nxtseq', 'tcp.hdr_len', 'tcp.flags.cwr', 'tcp.flags.urg', 'tcp.flags.push', 'tcp.flags.syn' ,'tcp.window_size','tcp.checksum','tcp.checksum_good', 'tcp.checksum_bad']):
        # sess = gen_data_frame(path_str)
        sess = read_pcap(path_str,fields=fields)
        return cls(sess)

    """ Length in seconds """
    def duration(self):
        pass

    """ Total number of packets with payload """
    def pl_total_packets(self):
        pass

    """ Total number of packets without payload """
    def no_pl_total_packets(self):
        pass

    """ Size of all packets in bytes """
    def size(self):
        return self.flow_up.size() + self.flow_down.size()

    """ Amount of packets """
    def __len__(self):
        return len(self.flow_up) + len(self.flow_down)

    """ Total number of packets """
    def packet_count(self):
        return len(self)

    """ Get the entire session DataFrame from flow up + down """
    def get_session_df(self):
        fu_df = self.flow_up.get_df()
        fd_df = self.flow_down.get_df()
        return pd.concat([fu_df, fd_df], axis=0, ignore_index=True)

    """ Mean of packet size """
    def mean_packet_size(self):
        fu_fd_df = self.get_session_df()
        return fu_fd_df['frame.len'].mean()

    """ Variance of packet size """
    def sizevar(self):
        fu_fd_df = self.get_session_df()
        return fu_fd_df['frame.len'].var()

    """ Max packet size """
    def max_packet_size(self):
        fu_fd_df = self.get_session_df()
        return fu_fd_df['frame.len'].max()

    """ Min packet size """
    def min_packet_size(self):
        fu_fd_df = self.get_session_df()
        return fu_fd_df['frame.len'].min()

    """ # Packets in forward direction (fpackets) """
    def fpackets(self):
        return len(self.flow_up)

    """ # Packets in backward direction (bpackets) """
    def bpackets(self):
        return len(self.flow_down)

    """ # Bytes in forward direction (fbytes) """
    def fbytes(self):
        return self.flow_up.size()

    """ # Bytes in backward direction (bbytes) """
    def bbytes(self):
        return self.flow_down.size()

    """ Min forward inter-arrival time (min_fiat) """
    def min_fiat(self):
        return self.flow_up.min_time_delta()

    """ Min backward inter-arrival time (min_biat) """
    def min_biat(self):
        return self.flow_down.min_time_delta()

    """ Max forward inter-arrival time (max_fiat) """
    def max_fiat(self):
        return self.flow_up.max_time_delta()

    """ Max backward inter-arrival time (max_biat) """
    def max_biat(self):
        return self.flow_down.max_time_delta()

    """ Standard deviation of forward inter- arrival times (std_fiat) """
    def std_fiat(self):
        return self.flow_up.std_time_delta()

    """ Standard deviation of backward inter- arrival times (std_biat) """
    def std_biat(self):
        return self.flow_down.std_time_delta()

    """ Mean forward inter-arrival time (mean_fiat) """
    def mean_fiat(self):
        return self.flow_up.mean_time_delta()

    """ Mean backward inter-arrival time (mean_biat) """
    def mean_biat(self):
        return self.flow_down.mean_time_delta()

    """ Min forward packet length (min_fpkt) """
    def min_fpkt(self):
        return self.flow_up.min_packet_size()

    """ Min backward packet length (min_bpkt) """
    def min_bpkt(self):
        return self.flow_down.min_packet_size()

    """ Max forward packet length (max_fpkt) """
    def max_fpkt(self):
        return self.flow_up.max_packet_size()

    """ Max backward packet length (max_bpkt) """
    def max_bpkt(self):
        return self.flow_down.max_packet_size()

    """ Std deviation of forward packet length (std_fpkt) """
    def std_fpkt(self):
        return self.flow_up.std_packet_size()

    """ Std deviation of backward packet length (std_bpkt) """
    def std_bpkt(self):
        return self.flow_down.std_packet_size()

    """ Mean forward packet length (mean_fpkt)	"""
    def mean_fpkt(self):
        return self.flow_up.mean_packet_size()

    """ Mean backward packet length (mean_bpkt) """
    def mean_bpkt(self):
        return self.flow_down.mean_packet_size()

    """
    Our features
    """

    """
    Discretized upstream TTL values.
    Assuming Two bins: 0-64, 65-128
    """
    def mean_fttl(self):
        if self.flow_up.get_mean_ttl() <= 64:
            return np.array([1,0])
        elif self.flow_up.get_mean_ttl() > 64:
            return np.array([0,1])
        else:
            return np.array([0,0])

    """ Forward peak features """
    def fpeak_features(self):
        return self.flow_up.peak_features()

    """ Backward peak features """
    def bpeak_features(self):
        return self.flow_down.peak_features()

    """
    Packet size histogram of 10 bins

    The original Ethernet IEEE 802.3 standard defined the minimum Ethernet frame size as 64 bytes
    and the maximum as 1518 bytes.
    The maximum was later increased to 1522 bytes to allow for VLAN tagging.
    The minimum size of an Ethernet frame that carries an ICMP packet is 74 bytes.
    """
    def size_histogram(self):
        fu_fd_df = self.get_session_df()
        hist = np.histogram(fu_fd_df['frame.len'], bins=[ 0.,   160.,   320.,   480.,   640.,   800.,   960.,  1120., 1280.,  1440.,  1600. ])
        return hist[0]
