import os
from file_merge import merge
from check_skeletons import check_skeletons
from settings import *
from firebase_connection import get_new_files

# Dump data from firebase

file_location = './file_stream/'

from firebase_config import config
get_new_files(config,file_location)


merged_file_location = './merged_file_stream/'
files = os.listdir(file_location)
curdir = os.getcwd()

ids = []
for file in files:
	id = file.split('.')[0].split('_')[-1]
	if (id not in ids):
		ids.append(id) 


# Merge related files
# Check and create skeletons

for id in ids:
	try:
		print(id)
		merge(id,file_location)
		os.rename(file_location+id+'.txt',merged_file_location+id+'.txt')
		check_skeletons(merged_file_location+id+'.txt')
	except Exception as e:
		print(e)

routes = os.listdir('routes')
for route in routes:
	# Execute the bus stop finder code
	os.system('python '+bsf_location+'/seg2.py '+bsf_location+' stops.txt')
	# Execute the feature extraction code
	os.system('python '+fa_location +'/launcher.py -i '+route+' -o ./Results/ -s '+route+'/stops.txt'+)
	pass