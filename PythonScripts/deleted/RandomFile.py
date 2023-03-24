#------------------------------------------------------------------------
import N10X
import random
import time

#------------------------------------------------------------------------
def FilterOut(file):
	return \
		file.lower().find("externallibs") != -1 or \
		file.lower().find("puredevreg") != -1 or \
		(file.lower().find(".cpp") == -1 and file.lower().find(".h") == -1)
		
#------------------------------------------------------------------------
def RandomFile():
	all_files = N10X.Editor.GetWorkspaceFiles()
	filtered_files = []
	for file in all_files:
		if not FilterOut(file):
			filtered_files.append(file)

	random.seed(time.time())
	index = random.randint(0, len(filtered_files) - 1)
	file = filtered_files[index]
	print("opening file: " + file)
	N10X.Editor.OpenFile(file)

