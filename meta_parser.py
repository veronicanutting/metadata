# Base code
import subprocess
import os
import matplotlib.pyplot as plt

directory_path = os.getcwd()
folder = directory_path+"/test_files"
#folder = "/Users/veronicanutting/Desktop/general"

# Get all file paths within given directory
def getFilePaths(folder):
    proc = subprocess.Popen(["ls",folder], stdout=subprocess.PIPE, universal_newlines=True)
    try:
        stdout_data, stderr_data = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill() # kill child process
        stdout_data, stderr_data = proc.communicate()
    return stdout_data.splitlines()

# Read in metadata
def readMetadata(file_path):
    proc = subprocess.Popen(["mdls",file_path], stdout=subprocess.PIPE, universal_newlines=True)
    try:
        stdout_data, stderr_data = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill() # kill child process
        stdout_data, stderr_data = proc.communicate()
    return stdout_data.splitlines()

# Preprocess metadata
def preProcess(stdout_data):
    meta = {}
    prev_key = ''
    for line in stdout_data:
        l = line.split("=",1)
        curr_left = l[0].strip()
        if len(l)==2:
            curr_right = l[1].strip()
            meta[curr_left]=[]
            if curr_right!='(':
                meta[curr_left].append(curr_right)
            prev_key = curr_left
        else:
            if curr_left!=')' and prev_key:
                meta[prev_key].append(curr_left)
    return meta

# Aggregate counts for metadata tags
def getStats(file_paths,folder):
    t_counts = {}
    t_vals = {}
    file_tags = {}
    for path in file_paths:
        file_tags[path] = [0,[]]
        stdout_data = readMetadata(folder+"/"+path)
        meta_dict = preProcess(stdout_data)
        for k,v in meta_dict.items():
            if k in t_counts.keys():
                t_counts[k]+=1
                t_vals[k].append(v)
            else:
                t_counts[k]=1
                t_vals[k]=[v]
        file_tags[path][0]=t_counts[k]
        file_tags[path][1]=set(t_counts.keys())
    return t_counts,t_vals,file_tags

# From tag counts, output frequency graph
def tagFrequencies(t_counts,file_paths,orderByBar=False):
    if orderByBar:
        names,values=[],[]
        for k in sorted(t_counts, key=t_counts.get):
            names.append(k),values.append(t_counts[k])
    else:
        names = sorted(list(t_counts.keys()))
        values = [t_counts[k] for k in names]
    plt.bar(range(len(t_counts)), values)#, tick_label=names)

    if len(names)<=10:
        plt.xticks(range(len(t_counts)), names, rotation=90)
    plt.ylabel("Tag Counts")
    plt.title(f"Metadata Tag Frequencies\n{len(names)} Tags from {len(file_paths)} Files")
    plt.tight_layout()
    plt.savefig('freqs.png')

# Get other tag stats
def findSharedTags(file_tags):
    num_files = len(file_tags)

    # Find tags shared among all files
    all_tags = [file[1] for file in file_tags.values()]
    shared_tags = set.intersection(*all_tags)
    print(f"{num_files} files share {len(shared_tags)} tags.")
    print(shared_tags)

def generalStats(t_vals):
    print(t_vals.keys())
    print(t_vals['kMDItemKind'])
    #print(f"{len(t_vals["kMDItemKind"])} types of files.")
    #print(t_vals["kMDItemKind"])

    #print(f"User id")
    #print(unique(t_vals["kMDItemFSOwnerUserID"]))

# Get stats for all test files in folder
file_paths = getFilePaths(folder)
t_counts,t_vals,file_tags = getStats(file_paths,folder)

#tagFrequencies(t_counts,file_paths,orderByBar=True)
findSharedTags(file_tags)
#generalStats(t_vals)
