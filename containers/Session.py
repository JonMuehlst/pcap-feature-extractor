#inherits from Packet_container

from PacketContainer import PacketContainer
from utils.read_pcap import gen_data_frame, gen_flows_up_down, read_pcap
import pandas as pd

"""
FIX:
"""

"""
Class fields:
sess - Session DataFrame
"""

class Session(PacketContainer):

    def __init__(self, s):
        self.sess = s
        self.flow_up, self.flow_down = gen_flows_up_down(self.sess)


    """  """
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
        pass

    """ Amount of packets """
    def __len__(self):
        return len(self.sess)

    """ Total number of packets """
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
