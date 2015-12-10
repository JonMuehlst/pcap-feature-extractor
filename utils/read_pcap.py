from steelscript.wireshark.core.pcap import PcapFile

""" 
Rename and reorder file
"""

"""
pdf = pcap.query(['frame.time_epoch', 'ip.src', 'ip.dst', 'ip.len', 'ip.proto'], 
                starttime = pcap.starttime, 
                duration='1min',
                as_dataframe=True)
"""

def gen_data_frame(path_str):
	pcap = PcapFile(path_str)
	pcap.info()

	pdf = pcap.query([
	'frame.time_epoch',
	'frame.time_delta',
	#'frame.pkt_len', 
	'frame.len',
	'frame.cap_len',
	'frame.marked',
	'ip.src', 
	'ip.dst',
	'ip.len',
	'ip.flags',
	'ip.flags.rb',
	'ip.flags.df',
	'ip.flags.mf',
	'ip.frag_offset',
	'ip.ttl', 
	'ip.proto',
	'ip.checksum_good',
	'tcp.srcport',
	'tcp.dstport',
	'tcp.len', 
	'tcp.nxtseq', 
	'tcp.hdr_len',
	'tcp.flags.cwr',
	'tcp.flags.urg',
	'tcp.flags.push',
	'tcp.flags.syn',
	'tcp.window_size',
	'tcp.checksum',
	'tcp.checksum_good',
	'tcp.checksum_bad',
	#'udp.length',
	#'udp.checksum_coverage',
	#'udp.checksum',
	#'udp.checksum_good',
	#'udp.checksum_bad' 
	],as_dataframe=True)

	return pdf

def gen_flows(pcap):
	ip_src = pcap['ip.src'].iloc[0]
	ip_dst = pcap['ip.dst'].iloc[0]
	return pcap[pcap['ip.src']==ip_src], pcap[pcap['ip.src']==ip_dst]
