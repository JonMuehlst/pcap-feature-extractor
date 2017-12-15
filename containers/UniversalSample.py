from utils.read_pcap import read_pt_csv
from conf import conf

import os
import pandas as pd
import numpy as np
import numbers

class UniversalSample(object):

    def __init__(self, s, path_str=None):
        self.df = s
        self.pcap_path = path_str

        """ Transport layer protocol """
        if len(self.df[self.df['tcp.srcport'].notnull()]) > 0:
            self.transport_proto = conf.TCP_PROTOCOL
        elif len(self.df[self.df['udp.srcport'].notnull()]) > 0:
            self.transport_proto = conf.UDP_PROTOCOL


    @classmethod
    def from_filename(cls, path_str):
        segment = read_pt_csv(path_str)
        return cls(segment,path_str)


    def get_df(self):
        return self.df

    def transport_protocol(self):
        return self.transport_proto


    def __len__(self):
        """
        Amount of packets
        """
        return len(self.df)
