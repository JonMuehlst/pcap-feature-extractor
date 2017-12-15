import numpy as np
from conf.conf import client_hello_num, server_hello_num, SSL3_V, TLS1_V, TLS11_V, TLS12_V, get_temp_folder, TCP_PROTOCOL, UDP_PROTOCOL

class Flow(object):

    def __init__(self, p):
        self.df = p

        """ Transport layer protocol """
        if len(self.df[self.df['tcp.srcport'].notnull()]) > 0:
            self.transport_proto = TCP_PROTOCOL
        elif len(self.df[self.df['udp.srcport'].notnull()]) > 0:
            self.transport_proto = UDP_PROTOCOL

    def get_df(self):
	    return self.df

    def transport_protocol(self):
        return self.transport_proto

    """ Amount of packets """
    def __len__(self):
        return len(self.df)
