import sys
import os
import glob

def merge(uid, folder = '.'):
	
	curdir = os.getcwd()
	os.chdir(folder)
	
	gps_strings = None
	wifi_strings = None
	marking_strings = None

	files = glob.glob('*'+uid+'*')
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

	for i in range(0,len(gps)):
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
		
		wifi_data = []
		while (k<len(wifis) and wifis[k][3]<=time):
			if (wifis[k][3] == time):
				wifi_data = wifi_data + [(wifis[k][0],wifis[k][1],int(wifis[k][2]))]
			k = k+1
		res = res + [(lat,lng,time,mark,wifi_data,info,alt)]
	
	file = open(uid+'.txt','w')
	try:
		for result in res:		
			file.write(result[0]+','+result[1]+','+result[2]+','+str(result[3])+','+str(result[5])+','+str(result[6])+','+str(result[4])+'\n')			
	except Exception as e:
		print(e)
	file.close()
	os.chdir(curdir)
	
if __name__ == '__main__':
	merge('94bb3ec4-0821-4149-831b-308a4cd6929a','./firebase_content/')