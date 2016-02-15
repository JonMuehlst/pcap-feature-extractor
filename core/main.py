from core.Converter import Converter
from utils.general import space_to_underscore
from conf import conf

"""
Convert all relevant pcap files in the given ROOT_DIRECTORY with the given feature_list and save the results to the output_filename
"""
def work():

    rename_flag = conf.space_to_underscore()
    ROOT_DIRECTORY = conf.input_directory()

    if rename_flag:
        space_to_underscore(ROOT_DIRECTORY)

    output_filename_full_path = conf.output_filename()

    conv = Converter()
    conv.activate()
    conv.write_to_csv(output_filename_full_path, separator='\t')


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
