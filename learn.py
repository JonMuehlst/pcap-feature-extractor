#!/usr/bin/env python

import pandas as pd
from sklearn import svm
import numpy as np



# Step 1 - Read dataset
df = pd.read_csv('/home/jony/infomedia/pcap-feature-extractor/real_data/20_12_15_samples.csv', sep='\t')

# Delete uncalc feature
df = df.drop('sizemean', 1)
df = df.dropna()

# write clean data to file
df.to_csv('/home/jony/infomedia/pcap-feature-extractor/real_data/20_12_15_samples_clean.csv', separator='\t', index=False)

""" use only for try """
# df = df.head(5)

num_rows = len(df)
num_columns = len(df.columns)
df_y = df.iloc[:,num_columns-1]
# df = df.drop(['packet_count','sizevar', 'std_fiat', 'std_biat', 'fpackets', 'bpackets', 'fbytes', 'bbytes', 'min_fiat', 'min_biat', 'max_fiat', 'max_biat', 'std_fiat', 'std_biat', 'mean_fiat', 'mean_biat', 'min_fpkt', 'min_bpkt', 'max_fpkt', 'max_bpkt', 'std_fpkt', 'std_bpkt','label'],1)
df = df.drop('label',1)
# print repr(df)
# print
# print repr(df_y)
df.insert(0,'label',df_y)
# print
# print repr(df)
# print repr(df_y)
for i in range(1,len(df.columns)):
    for j in range(0,len(df)):
        df.iloc[j,i] = str(i) + ':' + str(df.iloc[j,i])
        # a=str(i) + ':' + str(df.iloc[j,i])
for j in range(0,len(df)):
    if df.iloc[j,0] == 1:
        df.iloc[j,0] = '+' + str(1)
    else:
        df.iloc[j,0] = '-' + str(1)
# print df
df.to_csv('/home/jony/infomedia/pcap-feature-extractor/real_data/20_12_15_samples_clean_for_libsvm.csv', separator='\t', index=False)

""" end part try only """



# # Calc and print size of data set
# num_rows = len(df)
# num_columns = len(df.columns)
# train_rows = int(num_rows * 0.7)
# test_rows = num_rows - train_rows
#
# print num_rows
# print num_columns
#
# # Cut data to train and test
# df_x_train = df.head(train_rows)
# df_x_test = df.tail(test_rows)
#
# # Crate labels vector for test and train
# df_y_train = df_x_train.iloc[:,num_columns-1]
# df_y_test = df_x_test.iloc[:,num_columns-1]
#
# # Delete label colums from train and test
# df_x_train = df_x_train.drop('label',1)
# df_x_test = df_x_test.drop('label',1)
#
#
#
# # print repr(df_x_train)
#
# print len(df_x_train)
# print len(df_x_test)
#
#
# # Learning try
# #
# # """ use only for try """
# # X_train = np.array(df_x_train)
# # y_train = np.array(df_y_train)
# # X_test = np.array(df_x_test)
# # y_test = np.array(df_y_test)
# # print
# # clf = svm.SVC()
# # clf.fit(X_train, y_train)
# # test_score = clf.score(X_test, y_test)
# # print test_score
# #
# # """ end part try only """
