import os
import pandas as pd
import numpy as np
import pathos.multiprocessing as mp

from utils.general import gen_label

root_folder = '/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016'
input_csv_file = os.path.join(os.getcwd(),'data','all_ids.csv')
output_csv_file = os.path.join(os.getcwd(),'data','all_ids_with_label.csv')

df = pd.read_csv(input_csv_file)

idxs = df.index.tolist()

p = mp.ProcessingPool(16)

df['label'] = float('nan')

global i

i = 0

def work(idx):
    global i
    folder_path = df.loc[idx,'folder']
    file_path = df.loc[idx,'fname']
    pcap_path = os.path.join(root_folder,folder_path,file_path)
    label = gen_label(pcap_path)
    df.loc[idx,'label'] = label
    # print repr(label)
    # print repr(df.head())
    if i % 1000 == 0:
        print np.divide(np.float(i),np.float(len(df)))
    i += 1

map(work, idxs)

print repr(df.head())

df.to_csv(output_csv_file, index=False)
