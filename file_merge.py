import sys
import os
import glob
from settings import *

def merge(uid, folder = '.'):
	curdir = os.getcwd()
	print(curdir,folder)
	os.chdir(folder)
	print('HI')
	gps_strings = []
	wifi_strings = []
	marking_strings = []

	# print(curdir)
	# input()

	archive_folder = archive
	if archive_folder.startswith('..'):
		print('Archive folder should not start with ..\n')
	elif archive_folder.startswith('.'):
		archive_folder = archive_folder[2:]
		arch = os.path.join(curdir,archive_folder)
	elif archive_folder.startswith('/'):
		arch = archive_folder
	else:
		arch = os.path.join(curdir,archive_folder)
	
	# print(arch)
	# input()

	if (not os.path.exists(arch)):
		os.makedirs(arch)

	# print("Folder created")
	# input()
	
	files = glob.glob('*'+uid+'*')
	print(files	)
	for file in files:
		if (file.find('gps') >= 0 or file.find('GPS')>= 0):
			_file = open(file,'r')
			gps_strings = _file.read().split('\n')
			_file.close()
		if (file.find('wifi') >= 0 or file.find('WIFI') >= 0):
			_file = open(file,'r')
			wifi_strings = _file.read().split('\n')
			_file.close()
		if (file.find('marking')>= 0 or file.find('MARKING')>= 0):
			_file = open(file,'r')
			marking_strings = _file.read().split('\n')
			_file.close()
	gps = []
	marking = []
	wifis = []

	for gps_string in gps_strings:
		try:
			components = gps_string.split(',')
			gps = gps + [(components[0], components[1],components[4].split(' ')[1],components[2],components[3])]
		except Exception as e:
			print(e)
	for rating in marking_strings:
		try:
			components = rating.split(',')
			marking = marking + [(components[0], components[1].split(' ')[1])]
		except Exception as e:
			print(e)

	for wifi_string in wifi_strings:
		try:
			components = wifi_string.split(',')
			wifis = wifis + [(components[0], components[1], components[2], components[3].split(' ')[1])]
		except Exception as e:
			print(e)

	j=0
	k=0
	res = []

	# print(len(gps_strings))

	for i in range(0,len(gps)):
		# if i%500 == 0:
			# x = input()
		lat = gps[i][0]
		lng = gps[i][1]
		time = gps[i][2]
		info = gps[i][3]
		alt = gps[i][4]

		mark = -1
		while (j<len(marking) and marking[j][1]<=time):
			if(marking[j][1]==time):
				mark = marking[j][0]
			j = j+1
		
		# print(i,len(marking),j)

		wifi_data = []
		while (k<len(wifis) and wifis[k][3]<=time):
			if (wifis[k][3] == time):
				wifi_data = wifi_data + [(wifis[k][0],wifis[k][1],int(wifis[k][2]))]
			k = k+1
		res = res + [(lat,lng,time,mark,wifi_data,info,alt)]
	

	file = open(uid+'.txt','w')
	# print(res)
	try:
		for result in res:		
			file.write(result[0]+','+result[1]+','+result[2]+','+str(result[3])+','+str(result[5])+','+str(result[6])+','+str(result[4])+'\n')			
	except Exception as e:
		print(e)
	file.close()

	# print("File created, going to replace the individual files.")
	# input()
	
	for file in files:
		# print(file)
		os.rename(file,os.path.join(arch,file))

	os.chdir(curdir)
	
if __name__ == '__main__':
	merge('44a33497-e2a2-44d8-909e-08a082f55c97','./file_stream/')