import os
import helper
import analyze

directory_path = os.getcwd()

folder = directory_path+"/test_files"
#folder = "/Users/veronicanutting/Desktop/general"

# Extract metadata attributes from folder
file_paths = helper.getFilePaths(folder)
file_attrs,attr_freqs,attr_vals = helper.aggregateMetadata(file_paths,folder)

# Analyze metadata
analyze.generalInfo(folder,file_paths,file_attrs,attr_vals,verbose=False)
analyze.graphAttributeFrequencies(attr_freqs,num_files=len(file_attrs),color='blue',orderByBar=True)
analyze.printAttributesByKind(file_attrs)
shared_attrs = analyze.findSharedAttributes(file_attrs)
