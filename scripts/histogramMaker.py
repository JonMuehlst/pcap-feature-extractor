

import numpy as np
import math,os
from matplotlib import pyplot as plt

out_v=[("\\Users\\erlichsefi\\Dropbox\\Workspaces\\Atom\\Simulator\\pcap-feature-extractor\\doc\\histograms\\full_session.txt","full_session"),
("\\Users\\erlichsefi\\Dropbox\\Workspaces\\Atom\\Simulator\\pcap-feature-extractor\\doc\\histograms\\10_min_histo.txt","10 mintues")
,("\\Users\\erlichsefi\\Dropbox\\Workspaces\\Atom\\Simulator\\pcap-feature-extractor\\doc\\histograms\\1_min_histo.txt","1 minute")
,("\\Users\\erlichsefi\\Dropbox\\Workspaces\\Atom\\Simulator\\pcap-feature-extractor\\doc\\histograms\\10_sec_histo.txt","10 sec")
,("\\Users\\erlichsefi\\Dropbox\\Workspaces\\Atom\\Simulator\\pcap-feature-extractor\\doc\\histograms\\1_sec_histo.txt","1 sec")]

out_v=[
("\\Users\\erlichsefi\\Dropbox\\Workspaces\\Atom\\Simulator\\pcap-feature-extractor\\doc\\histograms\\Number_od_packets_in_1_sec_session.txt","Number of packets in 1 sec session")
]
root="/"

def numberOfPackets(pcap_path):
    statinfo = os.stat(pcap_path)
    return statinfo.st_size


def list_all_pcaps(root):
    pcaps=[]
    for path, subdirs, files in os.walk(root):
        for name in files:
            pcaps.append(os.path.join(path, name))
    return pcaps



# with open(out,'w') as w:
#     for pcap in list_all_pcaps(root):
#         w.write(str(numberOfPackets(pcap))+",")

# draw it
total=[]
i=0
reomved=[]
names=[]
maxs=[]
counts=[]
sums=[]
for out,name in out_v:
    lengths=[]
    c=0
    m=0
    s=0
    i=0
    with open(out,'r') as r:
        for val in r.readline().split(","):
            if val not in '':
                intt=int(val)
                m=max(m,intt)
                c=c+1
                s=s+intt
                if intt < 40000:
                    lengths.append(intt)
                else:
                    i=i+1
    reomved.append(i)
    total.append(lengths)
    names.append(name)
    maxs.append(m)
    counts.append(c)
    sums.append(s)


for arr,rev,name,m,c,s in zip(total,reomved,names,maxs,counts,sums):
    # lengths = np.asarray(lengths)
    bins = np.linspace(math.ceil(min(arr)),
                       math.floor(max(arr)),
                      20) # fixed number of bins

    plt.xlim([min(arr)-5, max(arr)+5])
    plt.hist(arr, bins=bins, alpha=0.5)
    plt.title(str(name))
    plt.xlabel('variable X (20 evenly spaced bins) , droped= '+str(rev))
    plt.ylabel('count')
    plt.show()

    print("For "+str(name))
    print("sum= "+str(s))
    print("max= "+str(m))
    print("avg= "+str(s/c))
    print("count= "+str(c))
