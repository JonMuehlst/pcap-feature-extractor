from utils.general import write_data_folders_to_file
from conf import conf

if __name__ == '__main__':

    session_folders_filename = conf.session_data_folders_filename()
    input_dir = conf.input_directory()
    write_data_folders_to_file(session_folders_filename ,input_dir)
