"""
This script iterates all pcaps in a folder and reorganizes them by capture.
In other words, if some sessions originate from the same capture they will
be grouped into one folder.
"""

import os
import shutil
from utils import assure_folder_exists

def group_pcaps(root_dir):
    sep = '.pcap'

    files = os.listdir(root_dir)
    pcaps = [f for f in files if '.pcap' in f]

    for p in pcaps:
        capture = p.split(sep)[0]
        assure_folder_exists(os.path.join(root_dir, capture))
        src = os.path.join(root_dir,p)
        dst = os.path.join(root_dir,capture,p)
        shutil.move(src,dst)

if __name__ == '__main__':
    root_dir = '/media/jon/ge60_data1/infomedia_data'

    one_s = 'filtered_raw_dataset_temu2016_first_1_sec'
    ten_s = 'filtered_raw_dataset_temu2016_first_10_sec'
    one_m = 'filtered_raw_dataset_temu2016_first_60_sec'
    ten_m = 'filtered_raw_dataset_temu2016_first_600_sec'

    strings = [one_s, ten_s, one_m, ten_m]
    folder_list = [ os.path.join(root_dir,f) for f in strings ]

    for folder in folder_list:
        group_pcaps(folder)
