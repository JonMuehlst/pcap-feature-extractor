import os
import pandas as pd
import numpy as np
import numbers

from Session import Session
from TimeSegment import TimeSegment
from TTSession import TTSession
from conf import conf

def ContainerWrapper(path_str=None):
    sample_type = conf.sample_type()
    cont_wrap = None
    if sample_type == 'session':
        cont_wrap = Session.from_filename(path_str)#, fields=conf.fields())
    elif sample_type == 'time_segment':
        cont_wrap = TimeSegment.from_filename(path_str)#, fields=conf.fields())
    elif sample_type == 'traffic_type':
        # cont_wrap = TTSession.from_filename(path_str)#, fields=conf.fields())
        cont_wrap = Session.from_filename(path_str)#, fields=conf.fields())
    return cont_wrap
