import subprocess,os,shutil,time,csv,shutil

#
# first convert all pcapng to pcap with
#  find . -type f -name '*.pcapng' -print0 | while IFS= read -r -d '' f; do editcap -F libpcap "$f" "${f%.pcapng}.pcap"; done
#
input_folder="/mnt/InfomediaMobie/mobie_captures_sessions_action/ariel_students"
output_folder="/mnt/InfomediaMobie/mobie_captures_sessions_action/ariel_students_by_csv"
errors=[]

def run(path,start,end,label,new_dst_folder):
    pathto=os.path.join(new_dst_folder,path.split("/")[-1])
    pathto=pathto+"_start_"+start.replace(" ","_").replace(":","_").replace("-","_")+"label_"+label+".pcap"
    print("path= "+path+"\n from= "+start+"\n pathto= "+pathto+"\n")
    start_q=start
    end_q=end
    if end is None:
        commed=["editcap" ,"-A",str(start_q),str(path),str(pathto)]
    else:
        commed=["editcap",  "-A",str(start_q),"-B",str(end_q),str(path),str(pathto)]
    #print(commed)
    p=subprocess.Popen(commed, stdout=subprocess.PIPE)
    p.wait()
    code=p.returncode
    if (code!=0):
        errors.append(commed)
        exit(1)

def timeAndlabel(csv_files):
    #print(str(csv_files))
    time=[]
    for csv_file in csv_files:
        vals=[]
        f = open(csv_file, 'rb')
        reader = csv.reader(f)
        for row in reader:
            vals.append((row[0].replace("-"," ").replace(".","-"),row[2].replace(" ","_")))
        time.extend(vals[1:])
    return time

def makeSureFolder(dst_folder,label):
    pathto=os.path.join(dst_folder,label)
    if not(os.path.exists(pathto)):
        os.mkdir(pathto,0755)
    return pathto

def work(csv_files,pcap_file,dst_folder):
    timeAndlabels=timeAndlabel(csv_files);
    for i in range(len(timeAndlabels)-1):
        start = timeAndlabels[i][0]
        end= timeAndlabels[i+1][0]
        label= timeAndlabels[i][1]
        new_dst_folder=makeSureFolder(dst_folder,label)
        run(pcap_file,start,end,label,new_dst_folder)
    start = timeAndlabels[len(timeAndlabels)-1][0]
    label= timeAndlabels[len(timeAndlabels)-1][1]
    new_dst_folder=makeSureFolder(dst_folder,label)
    run(pcap_file,start,None,label,new_dst_folder)


def listAllFolderContainPcap(input_folder):
    #print(input_folder)
    res=[]
    found=False
    for file in os.listdir(input_folder):
            full=os.path.join(input_folder,file)
            #print("  "+full)
            if os.path.isdir(full):
                depths=listAllFolderContainPcap(full)
                res.extend(depths)
            else:
                if not(found) and file.endswith(".pcap"):
                    res.append(input_folder)
                    print("found -> "+file+"-> "+input_folder)
                    found=True

    return res

input_folders=listAllFolderContainPcap(input_folder)
for folder in input_folders:
    print("cutting folder= "+folder+"\n")
    pcap_file=None
    csv_files=[]
    for filename in os.listdir(folder):
        if filename.endswith(".pcap"):
            pcap_file=filename
        elif filename.endswith(".csv"):
            csv_files.append(os.path.join(folder,filename))
    csv_files.sort()
    #print("55555 "+pcap_file)
    work(csv_files,os.path.join(folder,pcap_file),output_folder)
for e in errors:
    print(str(e))
