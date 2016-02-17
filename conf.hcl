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

  rename_space_underscore = true

  /*
  Fields to fetch from each packet.
  The field values are valid tshark\wireshark filters.

  Notice: Please make sure you have no duplicate fields
   */

  fields = ["frame.time_epoch", "frame.time_delta", "frame.len", "tcp.ack", "frame.cap_len", "frame.marked", "ssl.handshake.session_id_length", "ssl.handshake.comp_methods_length", "tcp.options.wscale.shift", "tcp.options.mss_val", "ip.src", "ip.dst", "ip.len", "ip.flags", "ip.flags.rb", "ip.flags.df", "ip.flags.mf", "ip.frag_offset", "ip.ttl", "ip.proto", "ip.checksum_good", "tcp.srcport", "tcp.dstport", "tcp.len", "tcp.nxtseq", "tcp.hdr_len", "tcp.flags.cwr", "tcp.flags.urg", "tcp.flags.push", "tcp.flags.syn", "tcp.flags.ack", "tcp.flags.reset" ,"tcp.window_size","tcp.checksum","tcp.checksum_good", "tcp.checksum_bad", "tcp.analysis.keep_alive", "ssl.record.version", "ssl.handshake.type", "ssl.handshake.cipher_suites_length", "ssl.handshake.extensions_server_name"]


  /*
  The desired features.
  Feature names need to be valid method names.
  (See source code - Session.py)
   */

  features = ["fSSL_session_id_len", "fSSL_num_extensions", "fSSL_num_compression_methods", "SYN_tcp_scale", "SYN_MSS", "SYN_tcp_winsize", "fcipher_suites", "fSSLv", "size_histogram", "fpeak_features", "bpeak_features", "packet_count", "min_packet_size", "max_packet_size", "mean_packet_size", "sizevar", "std_fiat", "fpackets", "bpackets", "fbytes", "bbytes", "min_fiat", "min_biat", "max_fiat", "max_biat", "std_biat", "mean_fiat", "mean_biat", "min_fpkt", "min_bpkt", "max_fpkt", "max_bpkt", "std_fpkt", "std_bpkt", "mean_fpkt", "mean_bpkt", "mean_fttl", "num_keep_alive"]


  /*
  Data directory - full path.
  */

  data = "/home/jony/Infomedia/pcap-feature-extractor/real_data"

  /*
  The output file name - full path.
  */

  output = "/home/jony/Infomedia/pcap-feature-extractor/real_data/samples_17.2.16.csv"

  /*
  sni_csv full path
  */

  sni_csv = "/home/jony/Infomedia/pcap-feature-extractor/sni.csv"

}
