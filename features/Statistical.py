import numpy as np

from containers.PacketContainer import PacketContainer
from utils.read_pcap import read_pt_csv
from conf import conf

import os
import pandas as pd
import numpy as np
import numbers



def size(container):
    """
    Size of all packets in bytes
    """
    df = container.get_df()
    return df['frame.len'].sum()


def std_packet_size(container):
    """
    Std packet size
    """
    df = container.get_df()
    if len(df) < 2:
        return 0
    return df['frame.len'].std()

def packet_count(container):
    """
    Number of packets
    """
    df = container.get_df()
    return len(df)


def mean_packet_size(container):
    """
    Mean of packet size
    """
    df = container.get_df()
    if len(df) == 0:
        return 0
    if len(df) == 1:
        return df['frame.len'].values[0]
    return df['frame.len'].mean()


def sizevar(container):
    """
    Variance of packet size
    """
    df = container.get_df()
    if len(df) < 2:
        return 0
    return df['frame.len'].var()


def max_packet_size(container):
    """
    Max packet size
    """
    df = container.get_df()
    return df['frame.len'].max()


def min_packet_size(container):
    """
    Min packet size
    """
    df = container.get_df()
    return df['frame.len'].min()


def std_time_delta(container):
    """
    Return unbiased standard deviation of the packet flow time deltas.
    Normalized by N-1 by default. This can be changed using the
    ddof argument - pandas
    """
    df = container.get_df()
    if len(df['frame.time_delta']) < 2:
        return 0
    return df['frame.time_delta'].std()


def min_time_delta(container):
    """
    Min time delta
    """
    df = container.get_df()
    return df['frame.time_delta'].min()

""" Max time delta """
def max_time_delta(container):
    df = container.get_df()
    return df['frame.time_delta'].max()

""" time delta mean """
def mean_time_delta(container):
    df = container.get_df()
    if len(df) == 0:
        return 0
    if len(df) == 1:
        return df['frame.time_delta'].values[0]
    return df['frame.time_delta'].mean()

def size_histogram(container):
    """
    Packet size histogram of 10 bins

    The original Ethernet IEEE 802.3 standard defined the minimum Ethernet
    frame size as 64 bytes and the maximum as 1518 bytes.
    The maximum was later increased to 1522 bytes to allow for VLAN tagging.
    The minimum size of an Ethernet frame that carries an
    ICMP packet is 74 bytes.
    """
    df = container.get_df()
    hist = np.histogram(df['frame.len'], bins=[ 0.,   160.,   320.,
                                                    480.,   640.,   800.,
                                                    960.,  1120., 1280.,
                                                    1440.,  1600. ])
    return hist[0]
