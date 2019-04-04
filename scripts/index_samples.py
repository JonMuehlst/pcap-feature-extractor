import argparse
import shelve
# import glob
import os
import numpy as np
from sklearn.datasets import load_svmlight_file
import pandas as pd
from pprint import pprint
from pathos import multiprocessing as mp
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist
from sklearn.neighbors import KDTree, BallTree
from scipy.spatial.distance import sqeuclidean
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
# p = mp.ProcessingPool(16)

# checked
# '/home/jon/workspace/pcap-feature-extractor/output/temu_sessions_w_id_24.5.17.csv',
# all sessions are unique and have id's

# /home/jon/wip/infomedia/data_set/libSVM/samples_25.2.16_comb_triple.csv_libSVM_0_train

# python index_samples.py -i /home/jon/wip/infomedia/data_set/libSVM/samples_25.2.16_comb_triple.csv_libSVM_0_train -r /home/jon/workspace/pcap-feature-extractor/output/temu_sessions_w_id_24.5.17.csv -l y -o out

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True,
	help = "path to input dataset")
ap.add_argument("-r", "--reference", required = True,
	help = "path to the dataset containing id's")
ap.add_argument("-l", "--libsvm", required = True,
	help = "is the input in libsvm format? y/n")
ap.add_argument("-o", "--output", required = True,
	help = "output file name")
args = vars(ap.parse_args())
# /home/jon/workspace/pcap-feature-extractor/output

libsvm = args["libsvm"]

# np.allclose(a,b,equal_nan=True)

# open input and reference dataset according to format
# iterate over input samples and search them in the reference
#   add id
# save back to file according to format

if libsvm == 'y':
    lsvm_format = True
elif libsvm == 'n':
    lsvm_format = False
else:
    raise Exception('libsvm should be either \'y\' or \'n\'')

if lsvm_format:
    in_samples, y = load_svmlight_file(args['input'])
    in_df = pd.DataFrame(in_samples.toarray())
    in_df['69'] = y
else:
    in_df = pd.read_csv(args['input'])

ans = np.zeros(len(in_df))

r_df = pd.read_csv(args['reference'], index_col='70').drop('Unnamed: 0', axis=1)
r_df.index = r_df.index.astype(int)

in_df = in_df.drop('69', axis=1)
r_df = r_df.drop('69', axis=1)

# le = LabelEncoder()
# le.fit(r_df['69'].astype(int))

# print 'contains'
# print repr(any(i == 11602 for i in r_df['69']))

# r_df['69'] = le.transform(r_df['69'].astype(int))
# in_df['69'] = le.transform(in_df['69'].astype(int))

i = 0

# for ix in in_df.index:
#     ref = r_df[r_df['69'] == in_df.loc[ix,'69']]
#     # print repr(ref.index)
#     for jx in ref.index:
#
#             if(np.allclose(in_df.loc[ix],r_df.loc[jx],equal_nan=True)):
#                 ans[ix] = r_df.loc[jx].name
#                 # print r_df.loc[jx].name
#                 # in_df.drop(ix, axis=0, inplace=True)
#                 # r_df.drop(jx, axis=0, inplace=True)
#                 break
    # i += 1
    # if i % 100 == 0:
    #     print i

l = r_df.index
ta = all(l[i] <= l[i+1] for i in xrange(len(l)-1))
print 'Are all index elements sorted?'
print repr(ta)
print repr(ta)
print repr(ta)
print repr(ta)
print repr(ta)

def close_dist(a,b):
    # if(np.allclose(a,b,equal_nan=True)):
    #     return 0
    print '---'
    print repr(a[-1])
    print repr(b[-1])
    print '---'
    if(a[-1] != b[-1]):
        return 1000000000.0
    else:
        return sqeuclidean(a,b)

rrr = r_df.as_matrix()
# pprint(rrr)


# mytree = KDTree(r_df, leaf_size=40, metric='minkowski', p=2)
# mytree = BallTree(rrr, leaf_size=40, metric=close_dist)
mytree = cKDTree(r_df)

# pprint(set(in_df['69']))
# pprint(set(r_df['69']))


for ix in in_df.index:

    # label = in_df.loc[ix,'69']
    # print repr(label)

    q = in_df.loc[ix].as_matrix().reshape(1, -1)
    k = 5
    dist, inds = mytree.query(q, k=k)

    # while(not any(r_df.loc[inds[0],'69'].isin([label]))):
    #     k += 30
    #     dist, inds = mytree.query(q, k=k)
    #     print 'k: ' + repr(k)
    # k = 0
    # print repr(indexes)
    for jx in inds[0]:
        # print '==='
        # print in_df.loc[ix,'69']
        # print r_df.loc[jx,'69']
        # print '==='
        if(np.allclose(in_df.loc[ix],r_df.loc[jx],equal_nan=True)):
            ans[ix] = r_df.loc[jx].name
            # print r_df.loc[jx].name
    i += 1
    if i % 500 == 0:
        print i

ta = len(ans) == len(set(ans))
print 'Are all indexes unique?'
print ta
print ta
print ta
print ta
print ta

def close_dist(a,b):
    if(np.allclose(a,b,equal_nan=True)):
        return 1
    return 0
# Y = cdist(in_df, r_df, 'euclidean')
# Y = cdist(in_df, r_df, close_dist)

# for i in range(len(Y)):
#     for j in range(len(Y[0])):
#         if Y[i,j] == 0:
#             ans[i] = j


# pprint(ans)
np.savetxt(args['output'], ans, delimiter=',')
# np.savetxt('dist_mat.csv', Y, delimiter=',')
"""
"""
