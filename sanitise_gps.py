# sanitise_gps.py
import math
import numpy as np
from settings import *
from utilities import get_spherical_distance
import os

gps = []

def get_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dX = x2 - x1
    dY = y2 - y1
    rads = math.atan2 (-dY, dX) #wrong for finding angle/declination?
    return math.degrees (rads)

def get_time(timestring):
	# print(timestring)
	time_units = str(timestring).split(':')
	# print(int(time_units[0])*3600+int(time_units[1])*60+int(time_units[2]))
	return int(time_units[0])*3600+int(time_units[1])*60+int(time_units[2])

# def break_down(part,file_name,pos):
# 	global gps

def to_human_time(ts):
	return str(int(ts/3600))+':'+str(int((ts%3600)/60))+':'+str(ts%60)

def sanitize(data, file_name):
	gps = list(np.loadtxt(file_name,usecols=(0,1,2,3),delimiter=',',skiprows = 1))
	full_file_name = os.path.abspath(file_name)
	exact_name = full_file_name.split(os.path.sep)[-1].split('.')[0]
	arr_data = list(data)
	part = 1
	location = os.path.sep.join(full_file_name.split(os.path.sep)[0:-1])
	new_file_name =  'sanitized_'+'part_'+str(part)+'_'+exact_name+'.txt'
	full_new_file_name = os.path.join(location,new_file_name)
	break_now = False
	new_file = True
	print(full_new_file_name)
	max_speed_ratio = 1
	file = open(full_new_file_name,'w')
	for i in range(len(arr_data)-1):
		if(i%1000 == 0):
			print(i)
		time_now = get_time(arr_data[i])
		td = get_time(arr_data[i+1]) - get_time(arr_data[i])
		distance = get_spherical_distance(float(gps[i][0]),float(gps[i][1]),float(gps[i+1][0]),float(gps[i+1][1]))
		if(td==0):
			continue
		if(distance==0 and gps[i+1][2]>0):
			print(i,"GPS issue Coming up")
			if(new_file):
				continue
			break_now = True
		# if(distance> 0 and gps[i+1][2]==0):
		# 	print(i,"GPS issue Coming up")
		# 	if(new_file):
		# 		continue
		# 	break_now = True
		file.write(str(gps[i][0])+','+str(gps[i][1])+','+str(gps[i][2])+','+str(gps[i][3])+','+to_human_time(time_now)+'\n')
		new_file = False
		if(td==1 and distance<allowed_distance):
			pass
		elif (td<allowed_time):
			# try interpolation
			if distance<allowed_distance:
				# check angle
				a1 = get_angle((gps[i-1][0],gps[i-1][1]),(gps[i][0],gps[i][1]))
				a2 = get_angle((gps[i][0],gps[i][1]),(gps[i+1][0],gps[i+1][1]))
				diff_ang = abs(a1-a2)
				# print(diff_ang)
				if(diff_ang<allowed_angle):
					# Do interpolation
					if(break_now):
						break_now = False
					lats_between = np.arange(gps[i][0],gps[i+1][0],(gps[i+1][0]-gps[i][0])/td)
					longs_between = np.arange(gps[i][1],gps[i+1][1],(gps[i+1][1]-gps[i][1])/td)
					alts_diff = (gps[i+1][3]-gps[i][3])
					interpolation_length = len(lats_between)
					# print(len(lats_between),len(longs_between),alts_diff)
					print(i,'Interpolating',new_file_name,'with',interpolation_length,'data')
					for j in range(1,interpolation_length):
						file.write(str(lats_between[j])+','+str(longs_between[j])+','+str(distance/td)+','+str(gps[i][3] + alts_diff*(j)/td)+','+to_human_time(time_now+j)+'\n')
				else:
					break_now = True
			else:
				break_now = True
		else:
			break_now = True
		
		if(break_now):
			x = input()
			print('Breaking down...')
			part += 1
			file.close()
			new_file_name = 'sanitized_'+'part_'+str(part)+'_'+exact_name+'.txt'
			full_new_file_name = os.path.join(location,new_file_name)
			file = open(full_new_file_name,'w')
			break_now = False
			new_file = True
			print(full_new_file_name)
	if(part > 1):
		# indicates that the trail has not been partitioned
		# nothing to do, exit
		return False

def sanitise_gps_from_time(file_name,dtype = {'names':('time',),'formats':('S8',)}):
	data = np.loadtxt(file_name,dtype=dtype,usecols=(2),delimiter=',',skiprows=1)
	# print(data)
	return check_jumps(data, file_name)

def sanitize_gps_from_date_time(file_name, dtype = {'names':('time',),'formats':('S19',)},usecols = 4):
	data = np.genfromtxt(file_name,dtype='str',usecols=usecols,delimiter=',',skip_header =1)
	# print(data,len(data))            
	times = [str(d).split(' ')[1] for d in data]
	print(times)
	return sanitize(times, file_name)

if __name__ == '__main__':
	import sys
	if '--file' in sys.argv:
		index = sys.argv.index('--file')
		file = sys.argv[index+1]
		print(file)
		sanitise_gps(file)
	# sanitise_gps_from_time('D:\\Personal Data\\Work\\m.tech\\Project\\up_3.txt')
	sanitize_gps_from_date_time('bus_GPS_44a33497-e2a2-44d8-909e-08a082f55c97.txt')