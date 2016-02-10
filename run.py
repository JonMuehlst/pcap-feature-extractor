 #!/usr/bin/env python

import sys
from core.main import work, start_here
from utils.hcl_helpers import parse_conf

if __name__ == '__main__':

    fields, features, input_directory, output_filename = parse_conf()
    work(input_directory,
    output_filename=output_filename,
    rename_space_underscore=True,
    feature_list=features,
    fields_list=fields)
