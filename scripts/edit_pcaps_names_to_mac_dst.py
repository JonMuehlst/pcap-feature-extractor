import os
import subprocess
import sys
import shutil
import shutil
import numpy as np
import pandas as pd
import time

from Over_load_mac import data_to_mac_encoder
from utils import assure_path_exists

current_milli_time = lambda: int(round(time.time() * 1000))


def add_mac_column(src_dir):
    mac_utility(src_dir)

def create_new_pcaps_with_modified_mac_dst(src_dir, dst_dir):
    mac_utility(src_dir, dst_dir, 1)

"""
flag = 0 add mac column to ID table
flag = 1 create new modified pcaps
"""
def mac_utility(src_dir, dst_dir="", flag=0):
    # read ids csv
    ids_csv_file = os.path.join(src_dir,'all_ids.csv')

    ids_df = pd.read_csv(ids_csv_file)

    idxs = ids_df.index.tolist()

    def get_vals_from_row(idx):
        TBD = int(0)
        label = int(ids_df.loc[idx,'label'])
        fileID = int(ids_df.loc[idx,'id'])
        sample_type = int(ids_df.loc[idx,'sample_type'])

        pcap_folder = ids_df.loc[idx,'folder']
        pcap_name = ids_df.loc[idx,'fname']

        return TBD, label, fileID, sample_type, pcap_folder, pcap_name


    for idx in idxs:
        TBD, label, fileID, sample_type, pcap_folder, pcap_name = get_vals_from_row(idx)

        encoded_mac = data_to_mac_encoder(label=label,
                                          fileID=fileID,
                                          Brr=sample_type,
                                          TBD=TBD)

        if flag == 0:
            ids_df.loc[idx,'modified_mac'] = encoded_mac
        else:
            input_pcap = os.path.join(src_dir,pcap_folder,pcap_name)
            new_pcap_name=encoded_mac.replace(':','_')+"_@_"+str(current_milli_time())+".pcap"
            output_pcap = os.path.join(dst_dir,pcap_folder,new_pcap_name)

            # output_dir = os.path.join(dst_dir,pcap_folder)
            assure_path_exists(output_pcap)
            #print(output_pcap)
            shutil.copy(input_pcap,output_pcap)

    if flag == 0:
        ids_df.to_csv(os.path.join(src_dir,'all_ids_mac.csv'))


if __name__ == '__main__':
    #src_dir = '/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016'
    #dst_dir = '/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016_new_mac'
    src_dir = '/mnt/25b3e4f3-b870-4e3c-9bce-9c59cd160d11/nehor/2018/TestSet/filtered_raw_dataset_temu2016'
    dst_dir = '/mnt/25b3e4f3-b870-4e3c-9bce-9c59cd160d11/nehor/2018/TestSetMacName/fullsession'

    create_new_pcaps_with_modified_mac_dst(src_dir, dst_dir)
    # src_dir = '/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016_new_mac'
    # add_mac_column(src_dir)
