import os
from file_merge import merge
from shu
file_location = './file_stream/'
files = os.listdir(file_location)
curdir = os.getcwd()

ids = []
for file in files:
	id = file.split('.')[0].split('_')[-1]
	if (id not in ids):
		ids.append(id) 

os.chdir(file_location)
for id in ids:
	merge(id)


print(ids)