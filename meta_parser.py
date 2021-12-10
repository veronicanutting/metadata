# Base code
import subprocess
import os
import matplotlib.pyplot as plt

directory_path = os.getcwd()
folder = directory_path+"/test_files"

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
    p_counts = {}
    p_vals = {}
    for path in file_paths:
        stdout_data = readMetadata(folder+"/"+path)
        meta_dict = preProcess(stdout_data)
        for k,v in meta_dict.items():
            if k in p_counts.keys():
                p_counts[k]+=1
                p_vals[k].append(v)
            else:
                p_counts[k]=1
                p_vals[k]=[v]
    return p_counts,p_vals

# Get stats for all test files in folder
file_paths = getFilePaths(folder)
p_counts,p_vals = getStats(file_paths,folder)

# Output as graph
names = sorted(list(p_counts.keys()))
values = [p_counts[k] for k in names]
plt.bar(range(len(p_counts)), values)#, tick_label=names)
plt.xticks(range(len(p_counts)), names, rotation=90)
plt.ylabel("Frequencies")
plt.title(f"Metadata Tag Frequencies\n{len(names)} Tags from {len(file_paths)} Files")
plt.tight_layout()
plt.savefig('stats.png')
