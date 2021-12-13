import matplotlib.pyplot as plt

# Print out general information about metadata found
def generalInfo(folder,file_paths,file_attrs,attr_vals,verbose=False):
    print(f"Directory: {folder}")
    print(f"Number of file paths: {len(file_paths)}")
    print(f"Number of files: {len(file_attrs.keys())}")
    print(f"Number of kinds of files: {len(attr_vals['kMDItemKind'])}")
    print(f"File kinds: {attr_vals['kMDItemKind']}")
    print(f"Number of distinct user ids: {len(attr_vals['kMDItemFSOwnerUserID'])}")
    print(f"User ids: {attr_vals['kMDItemFSOwnerUserID']}")
    print(f"Number of distinct attributes: {len(attr_vals.keys())}")
    if verbose:
        print("Distinct attributes:")
        for t in attr_vals.keys():
            print(t)
            print(attr_vals[t])
            print()

# From attribute counts, output frequency graph
def graphAttributeFrequencies(attr_freqs,num_files,color,orderByBar=False):
    if orderByBar:
        names,values=[],[]
        for k in sorted(attr_freqs, key=attr_freqs.get):
            names.append(k),values.append(attr_freqs[k])
    else:
        names = sorted(list(attr_freqs.keys()))
        values = [attr_freqs[k] for k in names]
    plt.bar(range(len(attr_freqs)), values,color=color)

    if len(names)<=10:
        plt.xticks(range(len(attr_freqs)), names, rotation=90)
    else:
        plt.xticks(range(len(attr_freqs)), names, rotation=90,size=2)
    plt.ylabel("Attribute Counts")
    plt.xlabel("Attributes")
    plt.title(f"Metadata Attributes Frequencies\n{len(names)} Attributes from {num_files} Files in Single Directory")
    plt.tight_layout()
    plt.savefig('freqs.png')

# Find which attributes are shared amongst all the files analyzed
def findSharedAttributes(file_attrs):
    num_files = len(file_attrs)

    # Find attrs shared among all files
    all_attrs = [set(file_attrs[file].keys()) for file in file_attrs.keys()]
    shared_attrs = set.intersection(*all_attrs)
    print(f"{num_files} files share {len(shared_attrs)} attrs.")
    print(f"Shared attributes: {shared_attrs}")
    return shared_attrs

# Print all the attributes corresponding to differnt file kinds
def printAttributesByKind(file_attrs):
    attrs_by_kind = {}
    for f in file_attrs.keys():
        f_type = file_attrs[f]['kMDItemKind'][0]
        if f_type not in attrs_by_kind.keys():
            attrs_by_kind[f_type] = [len(file_attrs[f])]
        else:
            attrs_by_kind[f_type].append(len(file_attrs[f]))

    for k,v in attrs_by_kind.items():
        print(f"{len(v)} file(s) found of type {k}")
        print(f"Attribute counts: {v}")
        print(f"Min: {min(v)}, Max: {max(v)}, Avg: {sum(v)/len(v)}")
        print()
