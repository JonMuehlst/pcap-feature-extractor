#inherits from Packet_container

from PacketContainer import PacketContainer
from utils.read_pcap import gen_data_frame, gen_flows
import pandas as pd

"""
FIX:
Set flow up as the flow with dst_port 443
Check why 'pcap_to_feature_vector' generates different 'packet_count' values
"""

"""
Class fields:
sess - Session DataFrame
"""

class Session(PacketContainer):

    def __init__(self, s):
        self.sess = s
        self.flow_up, self.flow_down = gen_flows(self.sess)

    """  """
    @classmethod
    def from_filename(cls, path_str):
        sess = gen_data_frame(path_str)
        return cls(sess)

    """ Length in seconds """
    def duration(self):
        pass

    """ Total number of packets """
    def total_packets(self):
        pass

    """ Total number of packets with payload """
    def pl_total_packets(self):
        pass

    """ Total number of packets without payload """
    def no_pl_total_packets(self):
        pass

    """ Size of all packets in bytes """
    def size(self):
        pass

    """ Amount of packets """
    def __len__(self):
        return len(self.sess)

    """ """
    def packet_count(self):
        return len(self)

    """ Mean of packet size """
    def sizemean(self):
        return self.sess['tcp.len'].mean()

    """ Variance of packet size """
    def sizevar(self):
        return self.sess['tcp.len'].var()

    """ Max packet size """
    def max_packet_size(self):
        pass

    """ Min packet size """
    def min_packet_size(self):
        pass
