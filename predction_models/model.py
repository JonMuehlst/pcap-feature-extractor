import pandas as pd
from sklearn.externals import joblib
import threading
from utils.csvutil import append_result,verify_results_csv_exists
from utils.general import gen_label
class model():


    """pkl_path - pkl file contains the model from tensor flow
       results_file_path - the output file to write in"""
    def __init__(self,pkl_path,results_file_path):
        self.clf = self.load_model(pkl_path)
        self.results_file_path=results_file_path
        #self.some_rlock = threading.RLock()
        verify_results_csv_exists(results_file_path)



    """ get a X returned from the feature extractor
                   and return a predication     """
    def predict(self,x,mac):
        new_x=x[:-1]
        df = pd.DataFrame([new_x])
        predicted = self.clf.predict(df)[0]
       # mac=x[-1]
        self.write_result(predicted,mac)
        return predicted

    """ write the result to the outputfile """
    def write_result(self,predicted,mac_dst):
        #with some_rlock:
        append_result(self.results_file_path,predicted,mac_dst)

    """ load the modle"""
    def load_model(self,full_path):
       return joblib.load(full_path)
