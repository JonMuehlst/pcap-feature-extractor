
"""
Temporarily holding for reference
"""

output_filename='Dont_Have_OS_Or_Browser_At_Folder_Name.csv',
data_folders = gen_data_folders(PARENT_DIRECTORY)
only_pcap_files = gen_pcap_filenames(data_folders)
if len(only_pcap_files) > 0:
    os = parse_folder_name(data_folders)
    browser = parse_folder_name_for_browser(data_folders)
    if (os != 'Unknown' and browser != 'Unknown')
        discover_application (data_folders)
        #rename_space_under_input == 'y':
        #rename_space_under = True
    elif write_to_csv(ROOT_DIRECTORY + '/' + output_filename, separator='\t')

def discover_application (data_folders)
    twitter_sni_list = ['twitter.com' , 'twimg.com' , 'redirector.gvt1.com' , 'google-analytics.com' , 'r1---sn-cx1x9-ua8z.gvt1.com' , 'stats.g.doubleclick.net' , 'google.com' , 'google.co.il' , 'analytics.twitter.com' , 'cm.g.doubleclick.net' , 'pbs.twimg.com' , 'ton.twimg.com']
    df = read_pcap(pcap_path, fields=['frame.time_epoch','ssl.handshake.extensions_server_name'])
    sni = df[df['ssl.handshake.extensions_server_name']]
#    if sni in twitter_sni_list:
    if sni in twitter_sni_list
        #ssl.handshake.extensions_server_name == "pbs.twimg.com"
