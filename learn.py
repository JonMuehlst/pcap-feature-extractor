#!/usr/bin/env python

import pandas as pd
from sklearn import svm
import numpy as np
from sklearn.datasets import dump_svmlight_file

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
    # df = df.drop(str(num_columns-1),1)
    dump_svmlight_file (df,df_y,output_filename,zero_based=False,multilabel=False)
    # df.insert(0,'label',df_y)
    # for i in range(1,len(df.columns)):
    #     for j in range(0,len(df)):
    #         df.iloc[j,i] = str(i) + ':' + str(df.iloc[j,i])
    # Assuming the label is incorrect
    # for j in range(0,len(df)):
    #     if df.iloc[j,0] == 3:
    #         df.iloc[j,0] = 2
    #     else:
    #         df.iloc[j,0] = '-' + str(1)
    # df.to_csv(output_filename, sep='\t', index=False, header=False)

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

def prepare_libSVM_train_test(file_name, output_filename, sinds):
    # Step 1 - Read dataset
    df = pd.read_csv(file_name, sep='\t')
    # Delete uncalc feature
    df = df.dropna()
    # sinds = np.random.permutation(len(df))
    df = df.iloc[sinds]
    print 'Num samples: ' + repr(len(df))
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



def prepare_libSVM_current():
    import sys

    # print 'Number of arguments:', len(sys.argv), 'arguments.'
    # print 'Argument List:', str(sys.argv)
    # run_sklearn()

    folder = '/home/cyber/InfoMedia/clf-compare/new/24.2.16/'
    path1 = folder + 'samples_25.2.16_all_features_triple.csv'
    path2 = folder + 'samples_25.2.16_common_features_triple.csv'
    path3 = folder + 'samples_25.2.16_no_ttl_feature_triple.csv'
    path4 = folder + 'samples_25.2.16_our_features_triple.csv'
    path5 = folder + 'samples_25.2.16_peak_features_triple.csv'

    df = pd.read_csv(path1, sep='\t')
    df = df.dropna()
    num_samples = len(df)

    filenames = [path1, path2, path3, path4, path5]

    for i in range(5):
        sinds = np.random.permutation(num_samples)
        print repr(sinds)
        for filename in filenames:
            output_filename = filename + '_libSVM_' + repr(i)
            prepare_libSVM_train_test(filename, output_filename=output_filename, sinds=sinds)

def run_easy_py():
    import os

    folder = '/home/cyber/InfoMedia/clf-compare/new/24.2.16'
    train_test_couples = [[folder + '/samples_24.2.16_fixed_labels_all_features_triple_dropna.csv_libSVM_{}_train'.format(i), folder + '/samples_24.2.16_fixed_labels_all_features_triple_dropna.csv_libSVM_{}_test'.format(i)] for i in range(5)]
    for train_name, test_name in train_test_couples:
        os.system('python /home/cyber/InfoMedia/libsvm-3.21/tools/easy.py ' + train_name + ' ' + test_name + ' >> all_features.output')

""" choose list of features (aotumaticly append lables in the end)"""
def choose_feature(input_filename, output_filename, features_list):
    features_list =features_list.append('label')
    df = pd.read_csv(input_filename, sep='\t')
    df[features_list].to_csv(output_filename,sep='\t', index=False)

# cols_our=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11','12', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '68', 'label']
# cols_common=['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67','label']
# cols_peak=['23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40', 'label']
if __name__ == '__main__':
    # run_easy_py()
    prepare_libSVM_current()
