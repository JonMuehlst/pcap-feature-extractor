/*
Syntax

Single line comments start with # or //
Multi-line comments are wrapped in /* and */
Values are assigned with the syntax key = value (whitespace doesn’t matter). The value can be any primitive: a string, number, boolean, object, or list.
Strings are double-quoted and can contain any UTF-8 characters. Example: "Hello, World"
Numbers are assumed to be base 10. If you prefix a number with 0x, it is treated as a hexadecimal. If it is prefixed with 0, it is treated as an octal. Numbers can be in scientific notation: “1e10”.
Boolean values: true, false, on, off, yes, no.
Arrays can be made by wrapping it in []. Example: ["foo", "bar", 42]. Arrays can contain primitives and other arrays, but cannot contain objects. Objects must use the block syntax shown below.
Objects and nested objects are created using the structure shown below:

variable "ami" {
    description = "the AMI to use"
}
*/



conf {

  /*
  Preprocessing - Rename all spaces in data filenames, directories to underscores?
  */

  rename_space_underscore = false

  /*
  Fields to fetch from each packet.
  The field values are valid tshark\wireshark filters.

  Notice: Please make sure you have no duplicate fields

   */

 fields = ["frame.time_epoch", "frame.time_delta", "frame.len", "tcp.ack", "frame.cap_len", "frame.marked", "ssl.handshake.session_id_length", "ssl.handshake.comp_methods_length", "tcp.options.wscale.shift", "tcp.options.mss_val", "ip.src", "ip.dst", "ip.len", "ip.flags", "ip.flags.rb", "ip.flags.df", "ip.flags.mf", "ip.frag_offset", "ip.ttl", "ip.proto", "ip.checksum_good", "tcp.srcport", "tcp.dstport", "udp.srcport", "udp.dstport", "tcp.len", "tcp.nxtseq", "tcp.hdr_len", "tcp.flags.cwr", "tcp.flags.urg", "tcp.flags.push", "tcp.flags.syn", "tcp.flags.ack", "tcp.flags.reset" ,"tcp.window_size","tcp.checksum","tcp.checksum_good", "tcp.checksum_bad", "tcp.analysis.keep_alive", "ssl.record.version", "ssl.handshake.type", "ssl.handshake.cipher_suites_length", "ssl.handshake.extensions_server_name"]

  /*
  The desired features.
  Feature names need to be valid method names.
  (See source code - Session.py / TimeSegment.py)

  For session statistics:
  features = ["duration", "fpackets", "bpackets", "fbytes", "bbytes"]

  For ID:
  features = ["time_plus_ip_port_tuple"]

  For sessions:
  features = ["fSSL_session_id_len", "fSSL_num_extensions", "fSSL_num_compression_methods", "SYN_tcp_scale", "SYN_MSS", "SYN_tcp_winsize", "fcipher_suites", "fSSLv", "size_histogram", "fpeak_features", "bpeak_features", "packet_count", "min_packet_size", "max_packet_size", "mean_packet_size", "sizevar", "std_fiat", "fpackets", "bpackets", "fbytes", "bbytes", "min_fiat", "min_biat", "max_fiat", "max_biat", "std_biat", "mean_fiat", "mean_biat", "min_fpkt", "min_bpkt", "max_fpkt", "max_bpkt", "std_fpkt", "std_bpkt", "mean_fpkt", "mean_bpkt", "mean_fttl", "num_keep_alive"]

  For time segments:
  features = ["size_histogram", "peak_features", "packet_count", "min_packet_size", "max_packet_size", "mean_packet_size", "sizevar", "std_time_delta", "min_time_delta", "max_time_delta", "mean_time_delta"]

  For traffic type time segments:
  features = ["size_histogram", "packet_count", "min_packet_size", "max_packet_size", "mean_packet_size", "sizevar", "std_time_delta", "min_time_delta", "max_time_delta", "mean_time_delta"]

  For traffic type:
  */

  features = ["size_histogram", "packet_count", "min_packet_size", "max_packet_size", "mean_packet_size", "sizevar", "std_fiat", "fpackets", "bpackets", "fbytes", "bbytes", "min_fiat", "min_biat", "max_fiat", "max_biat", "std_biat", "mean_fiat", "mean_biat", "min_fpkt", "min_bpkt", "max_fpkt", "max_bpkt", "std_fpkt", "std_bpkt", "mean_fpkt", "mean_bpkt", "mean_fttl"]

  /*
  Data directory - full path.


  data = "/home/jon/wip/mobile_actions/data"
  data = "/media/jon/ge60_data1/infomedia_data/mobile_actions_flash_networks/output"
  data = "/media/jon/ge60_data1/infomedia_data/filtered_raw_dataset_temu2016_first_1_sec"

  data = "/media/jon/ge60_data1/infomedia/action_data/subset"
  data = "/media/jon/ge60_data1/infomedia_data/cipher_sessions"
  data = "/media/jon/A40E85720E853E74/captures_2017_sessions_subset_2"
  data = "/media/jon/A40E85720E853E74/cipher_sessions_subset"
  data = "/media/jon/A40E85720E853E74/captures_2016_subset_sessions"
  data = "/media/jon/A40E85720E853E74/cipher_sessions_2016"
  data = "/media/jon/A40E85720E853E74/captures_2017_sessions"
  data = "/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016"
  */

  data = "/media/jon/ge60_data1/android_pcaps/sessions_90k-30m_4G"

  /*

  Temp data folder.

  */

  temp_folder = "/media/jon/ge60_data1/temp"

  /*
  The output file name - full path.
  */

  output = "/home/jon/workspace/pcap-feature-extractor/output/infomedia_traffictype_4G_only_id_label_3.12.17.csv"

  /*
  sni_csv full path
  */

  sni_csv = "/home/jon/workspace/pcap-feature-extractor/sni.csv"

  /*
  This file contains folders for session pcaps

  Notice - Can be generated by running generate_pcap_folders

  Notice - If one session pcap is contained in a folder it is added to the list.
           Do not mix session pcaps with non-session pcaps
  */

  session_folders_filename = "/home/jon/workspace/pcap-feature-extractor/data/tt_sessions_folders_temu.csv"

  /*
  This file contains folders for time segment pcaps

  Notice - Can be generated by running generate_pcap_folders

  time_segment_folders_filename = "/media/jon/ge60_data1/infomedia/action_data/subset/time_segment_folders.csv"
  time_segment_folders_filename = "/home/jon/wip/mobile_actions/data/time_segment_folders_mobile.csv"
  time_segment_folders_filename = "/media/jon/ge60_data1/infomedia/action_data/subset/time_segment_folders.csv"
  */

  time_segment_folders_filename = "/home/jon/workspace/pcap-feature-extractor/data/tt_timeframe_folders.csv"

  /*
    "triple" - Desktop: (OS, Browser, App) - tuple
    "action" - Desktop actions
    "mobile_action" - Mobile actions
    "traffic_type"
  */
  label_type = "traffic_type"

  /*
    "session" - pcaps are split to sessions by SplitCap
    "time_segment" - pcaps are split to time segments by SplitCap
    "traffic_type" - SplitCap sessions which may contain UDP traffic
  */
  sample_type = "traffic_type"

  /*
  Full path to the label database: pcap_id, info_i
  e.g.

  id,os,browser,action_type
  123,windows,chrome,text

  (keys are column names)
  mobile action format:
  {'id': 123, 'label': '1'}

  twitter action format:
  {'action': 'silence', 'side': 'follower', 'os': 'L', 'id': 412006, 'browser': 'firefox'}
  label_df_path = "/media/jon/ge60_data1/infomedia/action_data/time_segments/labels.csv"
  label_df_path = "/home/jon/wip/mobile_actions/labels.csv"
  label_df_path = "/media/jon/ge60_data1/infomedia_data/mobile_actions_flash_networks/output/labels.csv"
  label_df_path = "/media/jon/ge60_data1/infomedia/action_data/time_segments/subset.csv"
  */

  label_df_path = "/media/jon/ge60_data1/android_pcaps/sessions_90k-30m/all_ids.csv"

  /*
  pcap id database path

  id_table_path = "/media/jon/ge60_data1/Dropbox/infomedia_data/filtered_raw_dataset_temu2016/all_ids.csv"
  */

  id_table_path = "/media/jon/ge60_data1/android_pcaps/sessions_90k-30m/all_ids.csv"
}
