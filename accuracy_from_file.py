#!/usr/bin/env python
import os
import sys
import numpy as np

from sklearn.externals.joblib import Memory
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import accuracy_score

cwd_path = str(os.getcwd())

# mem = Memory(cwd_path)

# y_pred_path = cwd_path + '/result/30_12_15_libSVM_samples_multiclass_down_test.predict'
# y_path = cwd_path + '/original_data/30_12_15_libSVM_samples_multiclass_down_test'
"""
Assuming y_pred is a plain text file with a single column
Assuming y is contained in a libSVM format file
"""

def get_accuracy(y_path, y_pred_path):

    y_pred = np.fromfile(y_pred_path, sep='\n', dtype=int)

    # data = load_svmlight_file(y_path)
    # y = data[1]

    y = load_svmlight_file(y_path)[1]

    print 'y_pred: ' + repr(y_pred)
    print 'y_pred len: ' + repr(len(y_pred))

    print 'y: ' + repr(y)
    print 'y len: ' + repr(len(y))

    print 'Accuracy is: ' + repr(accuracy_score(y, y_pred))

if __name__ == '__main__':

    get_accuracy(sys.argv[1], sys.argv[2])
