import numpy as np
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

def peak_features(container):
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
    feature_arr = np.zeros(9)


    df = container.get_df()

    peak_df = df

    peak_df['size_cumsum'] = peak_df['frame.len'].cumsum()

    """ Add a column stating whether a certain packet represents a peak """
    peak_df['isPeak'] = np.where(peak_df['frame.time_delta'] > 0.05, True, False)

    """ A DataFrame containing only peak representing packets """
    peak_df = peak_df[peak_df['isPeak'] == True]

    # """ Getting rid of RST packets which cause undesired behaviour (negative ack diffs)"""
    # peak_df = peak_df[peak_df['tcp.flags.reset'] == False]

    """ For every trailing couple of peak representing packets (rows) compute the difference """
    peak_diff_ack = peak_df['size_cumsum'].diff()

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


    return feature_arr
