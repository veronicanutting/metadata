# Base code
import os
import helper
import analyze

directory_path = os.getcwd()
#folder = directory_path+"/test_files"
folder = "/Users/veronicanutting/Desktop/general"

#test_file = "orwell_englandyourengland.doc"
#m = helper.preProcess(helper.readMetadata(folder+"/"+test_file))

#for k,v in m.items():
#    print(k,v)

# Extract metadata from folder
file_paths = helper.getFilePaths(folder)
file_tags,tag_freqs,tag_vals = helper.aggregateMetadata(file_paths,folder)

# Analyze metadata
num_files = len(file_tags)
analyze.generalInfo(folder,file_paths,file_tags,tag_vals)
analyze.graphTagFrequencies(tag_freqs,num_files,orderByBar=True)
analyze.findSharedTags(file_tags)
