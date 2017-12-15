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
    conv.write_to_csv(output_filename_full_path, separator=',')
