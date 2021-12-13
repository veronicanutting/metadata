import subprocess

# Get all file paths within given directory
def getFilePaths(folder):
    proc = subprocess.Popen(["ls",folder], stdout=subprocess.PIPE, universal_newlines=True)
    try:
        file_paths, stderr_data = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill() # kill child process
        file_paths, stderr_data = proc.communicate()
    return file_paths.splitlines()

# Read in a file's metadata
def readMetadata(file_path):
    proc = subprocess.Popen(["mdls",file_path], stdout=subprocess.PIPE, universal_newlines=True)
    try:
        file_metadata, stderr_data = proc.communicate(timeout=15)
    except TimeoutExpired:
        proc.kill() # kill child process
        file_metadata, stderr_data = proc.communicate()
    return file_metadata.splitlines()

# Preprocess a file's metadata
def preProcess(file_metadata):
    meta = {}
    prev_key = ''
    multiLineAttribute = False
    for line in file_metadata:
        if line.strip()==')': # end of multiline attribute
            multiLineAttribute = False
        elif multiLineAttribute: # line contains single value associated with attr
            meta[prev_key].append(line.strip())

        else: # line contains 2 parts, attr and value or attr and '('
            line = line.split("=",1) # split only at first '='
            attr_name = line[0].strip()
            attr_value = line[1].strip()
            meta[attr_name]=[]

            if attr_value=='(':
                multiLineAttribute = True
            else:
                if attr_value not in ['(null)','""']:
                    meta[attr_name].append(attr_value)
            prev_key = attr_name
    return meta

# Aggregate information about all the metadata in a folder
def aggregateMetadata(file_paths,folder):
    file_attrs = {} # aggregate by file path
    attr_freqs = {} # aggregate by attribute
    attr_vals = {}
    for path in file_paths:
        stdout_data = readMetadata(folder+"/"+path)
        meta_dict = preProcess(stdout_data)
        file_attrs[path] = meta_dict
        for attr,v in meta_dict.items():
            if attr in attr_freqs.keys():
                attr_freqs[attr]+=1
                attr_vals[attr].add(tuple(v))
            else:
                attr_freqs[attr]=1
                attr_vals[attr]=set(tuple(v))

    return file_attrs,attr_freqs,attr_vals
