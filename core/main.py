from core.Converter import Converter
from utils.general import space_to_underscore

"""
Convert all relevant pcap files in the given ROOT_DIRECTORY with the given feature_list and save the results to the output_filename
"""
def work(
    ROOT_DIRECTORY,
    output_filename='samples.csv',
    rename_space_underscore=True,
    feature_list=['packet_count', 'mean_packet_size', 'sizevar', 'std_fiat', 'std_biat', 'fpackets', 'bpackets', 'fbytes', 'bbytes', 'min_fiat', 'min_biat', 'max_fiat', 'max_biat', 'std_fiat', 'std_biat', 'mean_fiat', 'mean_biat', 'min_fpkt', 'min_bpkt', 'max_fpkt', 'max_bpkt', 'std_fpkt', 'std_bpkt', 'mean_fpkt', 'mean_bpkt', 'mean_fttl'],
    fields_list=[]):

    if rename_space_underscore:
        space_to_underscore(ROOT_DIRECTORY)

    features = feature_list
    conv = Converter(ROOT_DIRECTORY, feature_list, fields_list)
    conv.activate()
    conv.write_to_csv(ROOT_DIRECTORY + '/' + output_filename, separator='\t')


"""
IMPLEMENT
UI - For end users who dont want to write code
"""
def start_here():
    print "Assuming config file is up-to-date"
    print '---'
    print "Enter data root directory: "
    ROOT_DIR = raw_input()
    print "Enter output filename: "
    out_file = raw_input()
    print "The system does not cope with spaces in folder / file names."
    print "Replace spaces with underscores in given directory?"
    print "Type y / n"
    rename_space_under_input = raw_input()

    if rename_space_under_input == 'y':
        rename_space_under = True
    elif rename_space_under_input == 'n':
        rename_space_under = False

    """
    Read feature_list from config file
    """
    work(ROOT_DIRECTORY=ROOT_DIR, output_filename=out_file, rename_space_underscore=rename_space_under)
