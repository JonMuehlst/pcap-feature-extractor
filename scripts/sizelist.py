
import math,os


out="name.txt"
root="";

def numberOfPackets(pcap_path):
    statinfo = os.stat(pcap_path)
    return statinfo.st_size


def list_all_pcaps(root):
    pcaps=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            pcaps.append(os.path.join(path, name))
    return pcaps


with open(out,'w') as w:
    for pcap in list_all_pcaps(root):
        w.write(str(numberOfPackets(pcap))+",")
