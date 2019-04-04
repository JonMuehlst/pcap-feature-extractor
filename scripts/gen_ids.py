"""
This script manages pcap ids

1. Get a list of indexed files from the all_ids.csv file.
2. Check if there are new files which were not indexed.
3. If there exist new files, save the last id number and increment by one.
4. For each file save the id, relative folder, file name and sample type.
   additionally generate the label number and the encoded mac address.
5. If an id file exists append the new entries, otherwise create a new file.

Assuming the following folder structure:

root:
    subfolder 1
    .
    .
    .
    subfolder n
    all_ids.csv

subfolder:
    pcap 1
    .
    .
    .
    pcap m
    id.csv

"""

'TODO: implement the above'

import os
import pandas as pd
from utils import get_triple_label
from Over_load_mac import data_to_mac_encoder

def id_file_exists(full_path):
    return os.path.isfile(full_path)

def init(root_dir, id_file):
    """
    Checks whether 'all_ids.csv' exists. If it does the table and last id+1
    are returned. If it does not exist a new table
    is returned together with the index 0.
    """

    if id_file_exists(os.path.join(root_dir, id_file)):
        df = pd.read_csv(os.path.join(root_dir, id_file))
        return df, df['id'].max()+1
    else:
        columns = [u'id', u'folder', u'fname', u'sample_type', u'label', u'modified_mac']
        return pd.DataFrame(columns=columns), 0


def check_new_files(root_dir, id_file):
    """
    If id_file does not exist all files are assumed to be new.
    A list of all files is returned.
    Otherwise the difference between files in the index and in
    the folder is computed. If the diff is greater than 0 a
    list of those files is returned. Otherwise this function returns
    an empty list.
    """

    files = os.listdir(root_dir)
    pcaps = [f for f in files if '.pcap' in f]

    if id_file_exists(os.path.join(root_dir, id_file)):
        df = pd.read_csv(os.path.join(root_dir, id_file))
        l1 = set(df['fname'])
        l2 = set(pcaps)
        l3 = list(l2 - l1)
        if len(l3) > 0:
            return l3
        else:
            return []
    else:
        return pcaps



def process_subfolder(root_dir, sub_dir, sample_type, current_free_id):

    id_file = 'id.csv'
    idi = current_free_id
    loc_df, _ = init(os.path.join(root_dir, sub_dir), id_file)
    pcaps = check_new_files(os.path.join(root_dir, sub_dir), id_file)

    for f in pcaps:
        label = get_triple_label(os.path.join(root_dir, sub_dir, f))
        mod_mac = data_to_mac_encoder(label, idi, sample_type)
        val_dict = {'id':idi,'folder':sub_dir,'fname':f, 'sample_type':sample_type, 'label':label, 'modified_mac':mod_mac}
        idi = idi + 1
        loc_df = loc_df.append(val_dict,ignore_index=True)

    loc_df.to_csv(os.path.join(root_dir, sub_dir, id_file),index=False)
    return loc_df, idi

def generate_ids(root_dir, sample_type):
    """
    Entry point.
    """
    id_file = 'all_ids.csv'
    gen_df, idi = init(root_dir, id_file)
    dirs = [ d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d)) ]

    for d in dirs:
        loc_df, idi = process_subfolder(root_dir, d, sample_type, idi)
        gen_df = gen_df.append(loc_df,ignore_index=True)

    gen_df.to_csv(os.path.join(root_dir, id_file),index=False)


if __name__ == '__main__':
    root_dir = '/home/jon/infomedia_data/2018'

    # Folder and sample type
    one_s = ('filtered_raw_dataset_temu2016', 0)
    one_s = ('filtered_raw_dataset_temu2016_first_1_sec', 1)
    ten_s = ('filtered_raw_dataset_temu2016_first_10_sec', 2)
    one_m = ('filtered_raw_dataset_temu2016_first_1_min', 3)
    ten_m = ('filtered_raw_dataset_temu2016_first_10_min', 4)


    folders = [one_s, ten_s, one_m, ten_m]

    for folder in folders:
        path = os.path.join(root_dir,folder[0])
        sample_type = folder[1]
        generate_ids(path, sample_type)
