import subprocess,os,shutil,time

#
# first convert all pcapng to pcap with
#  find . -type f -name '*.pcapng' -print0 | while IFS= read -r -d '' f; do editcap -F libpcap "$f" "${f%.pcapng}.pcap"; done
#
input_folder="/mnt/InfomediaMobie/mobile_captures"
output_folder="/mnt/InfomediaMobie/mobie_captures_sessions"
errors=[]

for folder, subs, files in os.walk(input_folder):
    dst_folder=folder.replace(input_folder,output_folder)
    if (os.path.exists(dst_folder)):
        shutil.rmtree(dst_folder, ignore_errors=True)
    os.mkdir(dst_folder,0755)
    for s in subs:
            os.mkdir(os.path.join(dst_folder,s),0755)
    for filename in files:
        if filename.endswith(".pcap"):
            if " " in filename:
                os.rename(os.path.join(folder,filename),os.path.join(folder,filename.replace(" ","_")))
                filename=filename.replace(" ","_")
            path=os.path.join(folder,filename)
            pathto=os.path.join(dst_folder,filename)
            os.mkdir(pathto,0755)
            print ("************spliting "+str(path)+"********************")
            commed="mono SplitCap.exe -r "+str(path)+" -s session -o "+str(pathto)
            p=subprocess.Popen(commed.split(" "), stdout=subprocess.PIPE)
            p.wait()
            code=p.returncode
            if (code!=0):
                errors.append(commed)
    for e in errors:
        print(str(e))
