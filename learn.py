#!/usr/bin/env python

import pandas as pd
from sklearn import svm
import numpy as np

"""
Read source data created with our "pcap-feature-extractor"

The source parameter can be either a filename or a DataFrame
"""
def create_data_libSVM(source, output_filename, isDataFrame=False):
    if not(isDataFrame):
        # Step 1 - Read dataset
        df = pd.read_csv(source, sep='\t')
    elif isDataFrame:
        df = source
    # Delete uncalc feature
    df = df.dropna()
    """ use only for try """
    num_rows = len(df)
    num_columns = len(df.columns)
    # Shuffle all rows
    index_permutation = np.random.permutation(num_rows)
    df = df.iloc[index_permutation]
    # Get label vector
    df_y = df.iloc[:,num_columns-1]
    df = df.drop('label',1)
    df.insert(0,'label',df_y)
    for i in range(1,len(df.columns)):
        for j in range(0,len(df)):
            df.iloc[j,i] = str(i) + ':' + str(df.iloc[j,i])
    # Assuming the label is incorrect
    for j in range(0,len(df)):
        if df.iloc[j,0] == 3:
            df.iloc[j,0] = 2
    #     else:
    #         df.iloc[j,0] = '-' + str(1)
    df.to_csv(output_filename, sep='\t', index=False, header=False)

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

"""
Wrapper for run create_data_libSVM
Get "file_name" and "output_filename"
Cut to train and test and call "create_data_libSVM" for each DataFrame
Wrire result to "file_name+train/test"
"""

def prepare_libSVM_train_test(file_name, output_filename):
    # Step 1 - Read dataset
    df = pd.read_csv(file_name, sep='\t')
    # Delete uncalc feature
    df = df.dropna()
    # Calc size of data set
    num_rows = len(df)
    num_columns = len(df.columns)
    # Calc size of train and test
    train_rows = int(num_rows * 0.7)
    test_rows = num_rows - train_rows
    # Cut data to train and test
    df_x_train = df.head(train_rows)
    df_x_test = df.tail(test_rows)

    train_output_filename = output_filename + '_train'
    test_output_filename = output_filename + '_test'

    create_data_libSVM(df_x_train, output_filename=train_output_filename, isDataFrame=True)
    create_data_libSVM(df_x_test, output_filename=test_output_filename, isDataFrame=True)



if __name__ == '__main__':

    import sys

    print 'Number of arguments:', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    # run_sklearn()
    prepare_libSVM_train_test(sys.argv[1], sys.argv[2])
