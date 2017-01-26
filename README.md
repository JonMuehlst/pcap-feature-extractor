# pcap-feature-extractor

A code package which transforms pcap files into ML feature vectors.

## Dependencies

See dependencies.txt

## Data folder structure

data/  
  --- any_folder_order/  
    ------ OS_dontcare_Browser/  
      ------------------ pcap_files.pcap  
etc...

Note: In case of session pcaps the folder name must follow the  
OS_dontcare_Browser structure.

Legal OS, Browser strings:

'l' - Linux  
'w' - Windows  
'd' - OSX  

'chrome' - Chrome  
'ff' - FireFox  
'firefox' - Firefox  
'ie' - Internet Explorer  
'safari' - Safari  


# Step by Step:

* Verify filenames don't contain spaces
* Enter / verify settings in conf.hcl
  * Especially:
    * sample_type
    * label_type
    * features - according to sample type
    * data - root data folder
    * output - the output csv full path (should be located in the output folder)
    * sni_csv - in case of triple label type make sure the sni.csv file exists.
                The file has two columns: sni, app_name (without headers).
                generate_sni_list.py can be used to generate all the sni's
                from the data but the app names have to be entered manually.
    * time_segment / session_folders_filename - all folders containing pcap
                                                files under "data" will be
                                                listed here
    * label_df_path - label data for each pcap file
* Verify there exists an empty 'output' folder in the root of run.py
* Verify that the time_segment / session_folders_filename is configured
* Run generate_pcap_folders.py if necessary

* run.py


# Additional files:

Note other md files for installation instructions and work flow recommendations.  

cleanup_pyc_files.py removes pyc files.  
