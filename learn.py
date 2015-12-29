#!/usr/bin/env python

import pandas as pd
from sklearn import svm
import numpy as np

"""
Read data_csv that create with our "pcap-feature-extractor"
"""
def create_data_libSVM(file_name = '/home/jony/infomedia/pcap-feature-extractor/real_data/20_12_15_samples_clean.csv'):
    # Step 1 - Read dataset
    df = pd.read_csv(file_name, sep='\t')
    # Delete uncalc feature
    # df = df.drop('sizemean', 1)
    # df = df.dropna()
    """ use only for try """
    num_rows = len(df)
    num_columns = len(df.columns)
    df_y = df.iloc[:,num_columns-1]
    df = df.drop('label',1)
    df.insert(0,'label',df_y)
    for i in range(1,len(df.columns)):
        for j in range(0,len(df)):
            df.iloc[j,i] = str(i) + ':' + str(df.iloc[j,i])
    for j in range(0,len(df)):
        if df.iloc[j,0] == 1:
            df.iloc[j,0] = '+' + str(1)
        else:
            df.iloc[j,0] = '-' + str(1)
    df.to_csv('/home/jony/infomedia/pcap-feature-extractor/real_data/20_12_15_samples_clean_for_libsvm.csv', separator='\t', index=False)

    """ end part try only """




def run_sklearn(file_name = '/home/jony/infomedia/pcap-feature-extractor/real_data/20_12_15_samples.csv'):
    # Step 1 - Read dataset
    df = pd.read_csv(file_name, sep='\t')
    # Delete uncalc feature
    df = df.drop('sizemean', 1)
    # df = df.dropna()
    # Calc size of data set
    num_rows = len(df)
    num_columns = len(df.columns)
    # Calc size of train and test
    train_rows = int(num_rows * 0.7)
    test_rows = num_rows - train_rows
    # Cut data to train and test
    df_x_train = df.head(train_rows)
    df_x_test = df.tail(test_rows)
    # Crate labels vector for test and train
    df_y_train = df_x_train.iloc[:,num_columns-1]
    df_y_test = df_x_test.iloc[:,num_columns-1]
    print df_x_train
    # Delete label colums from train and test
    df_x_train = df_x_train.drop('label',1)
    df_x_test = df_x_test.drop('label',1)
    """ Learn part """
    X_train = np.array(df_x_train)
    y_train = np.array(df_y_train)
    X_test = np.array(df_x_test)
    y_test = np.array(df_y_test)
    clf = svm.SVC()
    clf.fit(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    print test_score

    """ End learn part """
if __name__ == '__main__':
    run_sklearn()
