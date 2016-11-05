# pcap-feature-extractor
A code package which transforms pcap files into ML feature vectors.


Data folder structure:

Assuming a relevant pcap directory contains a .hcl file with label details.
This allows a non strict folder hierarchy i.e.  
data/  
----any_folder_order/  
--------relevant_folder1/  
------------label_data.hcl  
------------*.pcap  
----dummy_folder_name/  
--------relevant_folder2/  
------------label_data.hcl  
------------*.pcap  

# Step by Step:

1. Verify filenames don't contain spaces
2. Verify conf.hcl is setup properly
3. Verify there exists an empty 'output' folder
4. Generate a file which lists the folders containing pcap session files - 'session_folders_filename' in conf.hcl
5. run.py
