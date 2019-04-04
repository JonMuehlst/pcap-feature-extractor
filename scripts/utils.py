import os
import subprocess
from StringIO import StringIO

import numpy as np
import pandas as pd


# from utils import get_mac_from_pcap
# get_mac_from_pcap('/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016/W_Pc_ie_11-16__10_09_10/W_Pc_ie_11-16__10_09_10.pcap.TCP_10-0-0-11_49297_104-244-42-1_443.pcap')

# from utils.read_pcap import read_pcap

sni_path = os.path.join('/home/jon/infomedia_data', 'sni.csv')

def assure_path_exists(path):
    dir = os.path.dirname(path)
    # print 'in utils'
    # print repr(dir)
    if not os.path.exists(dir):
            os.makedirs(dir)

def assure_folder_exists(path):
    dir = path
    # print 'in utils'
    # print repr(dir)
    if not os.path.exists(dir):
            os.makedirs(dir)

def get_mac_from_pcap(pcap_path):
    df = read_pcap(filename=pcap_path, fields=['eth.dst'])
    mac_string = df.iloc[0,0]
    return mac_string

def get_triple_label(pcap_path):

    os_name, browser_name = parse_pcap_name(pcap_path)

    # Assuming session pcap
    sni = gen_sni(pcap_path)[0]

    # sni_path is a global variable
    sni_df = read_sni_csv(sni_path)
    app_name = gen_app_name_by_sni(sni_df, sni)

    return gen_label_triple(os_name, browser_name, app_name)

"""
Input label and return int values of os browser and app
"""
def translate(label):
    os = label % 10
    browser = (label % 1000) / 100
    app = (label % 10000) / 1000
    # browser = (label % 1000)
    # app = (label % 10000)
    return int(os), int(browser), int(app)


"""
Input brr int value
Return brr or session type string
"""
def get_brr_string(brr):
    brr_str = ""

    if brr == 0:
        brr_str = 'No Bearer detection' #TODO - supposed to be NA too?
    elif brr == 1:
        brr_str = 'Bearer 2G'
    elif brr == 2:
        brr_str = 'Bearer 3G'
    elif brr == 3:
        brr_str = 'Bearer 4G'
    elif brr == 4:
        brr_str = 'Bearer 4G_far'
    elif brr == 5:
        brr_str = 'Bearer CA'
    else:
        brr_str = 'NA'

    return brr_str


def get_sample_type(sample_type):
    sample_type_str = ""

    if sample_type == 16:
        sample_type_str = '10_min'
    elif sample_type == 32:
        sample_type_str = '1_min'
    elif sample_type == 48:
        sample_type_str = '10_sec'
    elif sample_type == 64:
        sample_type_str = '1_sec'
    elif sample_type == 80 :
        sample_type_str = 'full_session'
    else:
        sample_type_str = 'NA'

    return sample_type_str

def get_sample_type_inmili(sample_type):
    sample_type_str = ""

    if sample_type == 16:
        sample_type_str = '600000'
    elif sample_type == 32:
        sample_type_str = '60000'
    elif sample_type == 48:
        sample_type_str = '10000'
    elif sample_type == 64:
        sample_type_str = '1000'
    elif sample_type == 80 :
        sample_type_str = '0'
    else:
        sample_type_str = '-1'

    return sample_type_str

"""
Get int values of os, browser and app
Return the str values
"""
def get_label_string(os, browser, app):
    os_str = ""
    browser_str = ""
    app_str = ""
    # 1
    if os == 1:
        os_str = 'Linux'
    elif os == 2:
        os_str = 'Windows'
    elif os == 3:
        os_str = 'OSX'
    # 100
    if browser == 1:
        browser_str = 'Chrome'
    elif browser == 2:
        browser_str = 'Firefox'
    elif browser == 3:
        browser_str = 'IExplorer'
    elif browser == 4:
        browser_str = 'Safari'
    elif browser == 5:
        browser_str = 'Non-Browser'
    # 1000
    if app == 1:
        app_str = 'Dropbox'
    elif app == 2:
        app_str = 'Facebook'
    elif app == 3:
        app_str = 'Google'
    elif app == 4:
        app_str = 'Microsoft'
    elif app == 5:
        app_str = 'Teamviewer'
    elif app == 6:
        app_str = 'Twitter'
    elif app == 7:
        app_str = 'Youtube'
    elif app == 8:
        app_str = 'Unknown'

    # if browser == 100:
    #     browser_str = 'Chrome'
    # elif browser == 200:
    #     browser_str = 'Firefox'
    # elif browser == 300:
    #     browser_str = 'IExplorer'
    # elif browser == 400:
    #     browser_str = 'Safari'
    # elif browser == 500:
    #     browser_str = 'Non-Browser'
    #
    # if app == 1000:
    #     app_str = 'Dropbox'
    # elif app == 2000:
    #     app_str = 'Facebook'
    # elif app == 3000:
    #     app_str == 'Google'
    # elif app == 4000:
    #     app_str == 'Microsoft'
    # elif app == 5000:
    #     app_str == 'Teamviewer'
    # elif app == 6000:
    #     app_str == 'Twitter'
    # elif app == 7000:
    #     app_str == 'Youtube'
    # elif app == 8000:
    #     app_str == 'Unknown'


    return os_str, browser_str, app_str

"""
Start of functions taken from pcap-feature-extractor/utils/general.py
"""

def read_pcap(filename, fields=[], display_filter="",
              timeseries=False, strict=False, dtype=None):
    """ Read PCAP file into Pandas DataFrame object.
    Uses tshark command-line tool from Wireshark.

    filename:       Name or full path of the PCAP file to read
    fields:         List of fields to include as columns
    display_filter: Additional filter to restrict frames
    strict:         Only include frames that contain all given fields
                    (Default: false)
    timeseries:     Create DatetimeIndex from frame.time_epoch
                    (Default: false)

    Syntax for fields and display_filter is specified in
    Wireshark's Display Filter Reference:

      http://www.wireshark.org/docs/dfref/
    """

    """
    pcap_path = '/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_35015_192-229-233-25_443.pcap'
    cmd = 'tshark -r %s -T fields -E occurrence=a -E aggregator=, -e frame.time_epoch -e frame.time_delta -e frame.len -e frame.cap_len -e frame.marked -e ip.src -e ip.dst -e ip.len -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum_good -e tcp.srcport -e tcp.dstport -e tcp.len -e tcp.nxtseq -e tcp.hdr_len -e tcp.flags.cwr -e tcp.flags.urg -e tcp.flags.push -e tcp.flags.syn -e tcp.window_size -e tcp.checksum -e tcp.checksum_good -e tcp.checksum_bad' % pcap_path
    table = subprocess.check_output(cmd.split())
    df = pd.read_table(StringIO(table), header=None, names=[ ... column names ... ])
    remove from cmd: -n : header=y : -R ''
    """

    if timeseries:
        fields = ["frame.time_epoch"] + fields
    fieldspec = " ".join("-e %s" % f for f in fields)
    """
    display_filters = fields if strict else []
    if display_filter:
        display_filters.append(display_filter)
    filterspec = "-R '%s'" % " and ".join(f for f in display_filters)
    """
    filterspec = ''
    # options = "-r %s -n -T fields -E header=y -E occurrence=a -E aggregator=, " % filename
    options = "-r %s -T fields -E occurrence=a -E aggregator=, " % filename
    cmd = "tshark %s %s %s" % (options, filterspec, fieldspec)
    # print '------------------'
    # print 'cmd: ' + repr(cmd)
    # print '------------------'
    #
    # proc = subprocess.Popen(cmd, shell = True,
    #                              stdout=subprocess.PIPE)
    # table = subprocess.check_output(cmd)

    # pcap_path = '/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_35015_192-229-233-25_443.pcap'
    # pcap_path = '/home/jon/workspace/pcap-feature-extractor/data/L_cyber_chrome_09-17__11_38_11/L_cyber_chrome_09-17__11_38_11.pcap.TCP_10-0-0-14_33521_212-179-154-238_443.pcap'
    # cmd = 'tshark -r %s -T fields -E occurrence=a -E aggregator=, -e frame.time_epoch -e frame.time_delta -e frame.len -e frame.cap_len -e frame.marked -e ip.src -e ip.dst -e ip.len -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum_good -e tcp.srcport -e tcp.dstport -e tcp.len -e tcp.nxtseq -e tcp.hdr_len -e tcp.flags.cwr -e tcp.flags.urg -e tcp.flags.push -e tcp.flags.syn -e tcp.window_size -e tcp.checksum -e tcp.checksum_good -e tcp.checksum_bad' % pcap_path
    # print '------------------'
    # print 'cmd: ' + repr(cmd)
    # print '------------------'
    table = subprocess.check_output(cmd.split())


    if timeseries:
        df = pd.read_table(StringIO(table),
                        index_col = "frame.time_epoch",
                        parse_dates=True,
                        date_parser=datetime.datetime.fromtimestamp,
                        dtype=dtype)
    else:
        # df = pd.read_table(StringIO(table))
        df = pd.read_table(StringIO(table), header=None, names=fields, dtype=dtype)
        # print repr(df)
    return df


def gen_label_triple(input_os, input_browser, input_application):
    """
    Taken from pcap-feature-extractor

    Labels per combination:
        os = { Linux, Windows, OSX, Unknown }
        browser = { Chrome, FireFox, IExplorer, Unknown }
        application = { Twitter, Youtube, Unknown }

        The input is non case sensitive
    """

    input_os = input_os.lower()
    input_browser = input_browser.lower()
    input_application = input_application.lower()

    label = 10000

    if input_os == 'linux':
        label = label + 1
    elif input_os == 'windows':
        label = label + 2
    elif input_os == 'osx':
        label = label + 3
    elif input_os == 'unknown':
        label = label + 4

    if input_browser == 'chrome':
        label = label + 100
    elif input_browser == 'firefox':
        label = label + 200
    elif input_browser == 'iexplorer':
        label = label + 300
    elif input_browser == 'safari':
        label = label + 400
    elif input_browser == 'unknown':
        label = label + 500

    if input_application == 'dropbox':
        label = label + 1000
    elif input_application == 'facebook':
        label = label + 2000
    elif input_application == 'google':
        label = label + 3000
    elif input_application == 'microsoft':
        label = label + 4000
    elif input_application == 'teamviewer':
        label = label + 5000
    elif input_application == 'twitter':
        label = label + 6000
    elif input_application == 'youtube':
        label = label + 7000
    else:
        label = label + 8000

    return label



def gen_sni(filename):
    """
    Generate all SNIs from specific pcap file
    """
    pcap_sni_list = []
    #
    df = read_pcap(filename=filename, fields=['ssl.handshake.extensions_server_name'] , dtype = {'ssl.handshake.extensions_server_name':'string'})
    df = df[df['ssl.handshake.extensions_server_name'].notnull()]
    for index, row in df.iterrows():

        val = str(row['ssl.handshake.extensions_server_name'])
        pcap_sni_list.append(val)

    pcap_sni_list.append('unknwon')
    return pcap_sni_list

def gen_app_name_by_sni(df, sni):
    """
    Get sni_df
    Return app_name
    """
    app_name =df.loc[df['sni'] == sni]['app_name']
    if len(app_name) == 0:
        return 'unknown'
    else:
        return app_name.iloc[0]


def read_sni_csv(sni_csv):
    """
    Read sni csv and return sni data frame
    """
    df = pd.read_csv(sni_csv,names=['sni','app_name'])
    df.fillna('unknwon')
    return df


def parse_pcap_name(pcap_name):
    """
    Parse a pcap file name and return the os + browser
    Assumes the following format:
    L_cyber_chrome_09-17__11_38_11.pcap
    where pcap_name is the full path i.e. /home/user/folder/name.pcap

    Non case sensitive
    """
    temp = pcap_name.split(os.sep)
    temp.reverse()
    tokens = temp[0].split('_')

    input_os = tokens[0].lower()
    input_browser = tokens[2].lower()

    os_str = ''
    browser_str = ''

    if input_os == 'l':
        os_str = 'Linux'
    elif input_os == 'w':
        os_str = 'Windows'
    elif input_os == 'd':
        os_str = 'OSX'
    else:
        """ TEMP """
        os_str = 'OSX'

    if input_browser == 'chrome':
        browser_str = 'Chrome'
    elif input_browser == 'ff':
        browser_str = 'Firefox'
    elif input_browser == 'firefox':
        browser_str = 'Firefox'
    elif input_browser == 'ie':
        browser_str = 'IExplorer'
    elif input_browser == 'safari':
        browser_str = 'Safari'

    return os_str, browser_str

"""
End of functions taken from pcap-feature-extractor/utils/general.py
"""
