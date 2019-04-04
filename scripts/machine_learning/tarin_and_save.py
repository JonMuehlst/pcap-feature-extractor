"""
Simple script to train a random forest and save to file
"""
import os
import numpy as np
from sklearn.externals import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

"""remove an wanted features from the table"""
def get_feature_group(df, features_to_remove=[]):
    return df.drop(features_to_remove, axis=1)


""" load a csv file of the vectors and return an np array
     of all vectors"""
def loadData(data_fname,label_tag='label'):
    # Load data
    data_path = os.getcwd()
    df = pd.read_csv(os.path.join(data_path, data_fname), sep=',')
    df = df.dropna(axis=0)
    df= df.loc[:, ~df.columns.str.contains('^Unnamed')]
    #get label
    print list(df.columns.values)
    y = df[label_tag]
    y = y.astype(int)
    # drop label from table
    df = df.drop([label_tag], axis=1)
    # convert
    df.columns = np.array([int(x) for x in df.columns])
    return df, y

""" save as clf """
def save_clf(clf, output_path):
    joblib.dump(clf, output_path)



if __name__ == '__main__':
    ## set the classifiers to train
    rf = RandomForestClassifier(n_estimators=100, oob_score=True,
                                    n_jobs=-1)
    classifiers = [(rf, 'RandomForest')]
    features_to_drop=[([],'all')]
    # load the data
    min_data= 'first_600_sec_27.4.17/real_time_600_sec_27.4.17.csv'
    df, y = loadData(min_data,'69')

    # train
    for clf, clf_name in classifiers:
        for drop_feature_set, set_name in features_to_drop:
            X = get_feature_group(df, drop_feature_set)

            clf = clf.fit(X,y)
            save_clf(clf, os.path.join(os.getcwd(), set_name+'_'+clf_name+'.pkl'))
