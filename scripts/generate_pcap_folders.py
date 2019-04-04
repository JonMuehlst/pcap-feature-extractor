from utils.general import write_data_folders_to_file
from conf import conf

if __name__ == '__main__':

    sample_type = conf.sample_type()
    if sample_type == 'session':
        data_folders_filename = conf.session_data_folders_filename()
    elif sample_type == 'time_segment':
        data_folders_filename = conf.time_segment_data_folders_filename()

    input_dir = conf.input_directory()
    write_data_folders_to_file(data_folders_filename ,input_dir)
