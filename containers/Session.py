#inherits from Packet_container

import os
from utils.read_pcap import gen_data_frame, gen_flows_up_down, read_pt_csv
from containers.Flow import Flow
import pandas as pd
import numpy as np
import numbers
from conf.conf import client_hello_num, server_hello_num, SSL3_V, TLS1_V, TLS11_V, TLS12_V, get_temp_folder, TCP_PROTOCOL, UDP_PROTOCOL

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

import scapy
from scapy.all import rdpcap
# import scapy.layers.ssl_tls as scssl
import scapy_ssl_tls.ssl_tls as scssl

"""
FIX:
"""

"""
Class fields:
sess - Session DataFrame
"""

class Session(object):

    def __init__(self, s, path_str=None):
        self.first_packet = s.head(1)
        self.df = s
        self.flow_up, self.flow_down = gen_flows_up_down(s)
        self.flow_up, self.flow_down = Flow(self.flow_up), Flow(self.flow_down)
        self.pcap_path = path_str

        """ Get client hello """
        fu_df = self.flow_up.get_df()
        self.client_hello_pkt = fu_df[fu_df['ssl.handshake.extensions_server_name'].notnull()]

        """ Get SYN packet """
        self.syn_pkt = fu_df[(fu_df['tcp.flags.syn'] == 1) & (fu_df['tcp.flags.ack'] == 0)]

        """ Transport layer protocol """
        if len(self.df[self.df['tcp.srcport'].notnull()]) > 0:
            self.transport_proto = TCP_PROTOCOL
        elif len(self.df[self.df['udp.srcport'].notnull()]) > 0:
            self.transport_proto = UDP_PROTOCOL


    @classmethod
    def from_filename(cls, path_str):
        # sess = gen_data_frame(path_str)
        sess = read_pt_csv(path_str)
        return cls(sess,path_str)


    def get_client_hello(self):
        return self.client_hello_pkt

    def get_syn_pkt(self):
        return self.syn_pkt

    def get_df(self):
        return self.df

    def get_flow_up(self):
        return self.flow_up

    def get_flow_down(self):
        return self.flow_down

    def transport_protocol(self):
        return self.transport_proto

    def __len__(self):
        return len(self.df)
