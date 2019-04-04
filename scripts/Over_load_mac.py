import sys
import os

import numpy as np
import csv
import pandas as pd

def int_to_hexStr_two_byte(num):
    hex_val = hex(num).split('x')[-1]
    if len(hex_val) == 1:
        return '00:0' + str(hex_val)
    if len(hex_val) == 2:
        return '00:' + str(hex_val)
    if len(hex_val) == 3:
        return '0' + str(hex_val[0]) + ':' + str(hex_val[1:3])
    if len(hex_val) == 4:
        return str(hex_val[0:2]) + ':' + str(hex_val[2:4])
    else:
        return float('nan')

def int_to_hexStr_one_byte(num):
    hex_val = hex(num).split('x')[-1]
    if len(hex_val) == 1:
        return '0' + str(hex_val)
    if len(hex_val) == 2:
        return str(hex_val)
    if len(hex_val) == 3:
        return '0' + str(hex_val[0]) + ':' + str(hex_val[1:3])
    if len(hex_val) == 4:
        return str(hex_val[0:2]) + ':' + str(hex_val[2:4])
    else:
        return float('nan')

def hex_to_int(num):
    print(str(num))
    return int(num,16)


def translate_sample_type_brr(Brr):
    if Brr == 0:
        # Full session
        return 80
    elif Brr == 1:
        # 1 sec session
        return 64
    elif Brr == 2:
        # 10 sec session
        return 48
    elif Brr == 3:
        # 60 sec session
        return 32
    elif Brr == 4:
        # 600 sec session
        return 16
    else:
        return None

def data_to_mac_encoder(label, fileID, Brr, TBD = 0 ):
    """
    All inputs need to be int of decimal base
    TBD(To Be Determined) - for extra info , by default '00'
    label - label number
    fileID - fileID number
    sample_type - type of sample - translates into Brr
    Return - MAC address string containing the encoding of the input
    """
    label_hex = int_to_hexStr_two_byte(label)
    fileID_hex = int_to_hexStr_two_byte(fileID)
    type_hex = int_to_hexStr_one_byte(translate_sample_type_brr(Brr))
    TBD_hex = int_to_hexStr_one_byte(TBD)

    return TBD_hex + ':' + label_hex + ':' + fileID_hex + ':' + type_hex

"""
The opposite of the encoder.
"""
def mac_to_data_decoder(mac_string):
    print(mac_string)
    TBD = hex_to_int(mac_string[0:2])
    label = hex_to_int(mac_string[3:5] + mac_string[6:8])
    fileID = hex_to_int(mac_string[9:11] + mac_string[12:14])
    Brr = hex_to_int(mac_string[15:17])
    return TBD , label , fileID , Brr
