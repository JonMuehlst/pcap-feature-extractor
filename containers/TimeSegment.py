#inherits from Packet_container

from UniversalSample import UniversalSample
from utils.read_pcap import read_pt_csv
from conf import conf

import os
import pandas as pd
import numpy as np
import numbers

class TimeSegment(UniversalSample):
    """
    Assuming TCP traffic.
    """


    def __init__(self, s, path_str=None):
        super(TimeSegment, self).__init__(s, path_str=None)


    @classmethod
    def from_filename(cls, path_str):
        super(TimeSegment, cls).from_filename(path_str)


    def peak_features(self):
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
