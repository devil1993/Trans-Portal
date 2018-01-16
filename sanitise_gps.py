# sanitise_gps.py
import math
import numpy as np
from settings import *
from utilities import get_spherical_distance

gps = []

def get_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dX = x2 - x1
    dY = y2 - y1
    rads = math.atan2 (-dY, dX) #wrong for finding angle/declination?
    return math.degrees (rads)

def get_time(timestring):
	time_units = str(timestring).split(':')
	return int(time_units[0])*3600+int(time_units[1])*60+int(time_units[2])

def break_down(part,file_name,pos):
	global gps


def check_jumps(data, file_name):
	global gps
	arr_data = list(data)
	part = 1
	interpolated = False
	file = open(file_name + '_part_' + str(part),'w')
	for i in range(len(arr_data)-1):
		td = get_time(arr_data[i+1] - get_time(arr_data[i]))
		if (td==1):
			continue
		elif(td >1 and td<allowed_time):
			# try interpolation
			if (len(gps)==0):
				gps = list(np.loadtxt(file_name,usecols=(0,1),delimiter=',',skiprows = 1))
			distance = get_spherical_distance(float(gps[i][0]),float(gps[i][1]),float(gps[i+1][0]),float(gps[i+1][1]))
			if distance<allowed_distance:
				# check angle
				a1 = get_angle(gps[i][0],gps[i][1])
				a2 = get_angle(gps[i+1][0],gps[i+1][1])
				diff_ang = abs(a1-a2)
				if(diff_ang<allowed_angle):
					# Do interpolation
					if not interpolated:
						interpolated = True
					lats_between = np.arange(gps[i][0],gps[i+1][0],(gps[i+1][0]-gps[i][0])/td)
					longs_between = np.arange(gps[i][1],gps[i+1][1],(gps[i+1][1]-gps[i][1])/td)
					gps = list(gps[:i]) + list(np.transpose(np.array([lats_between,longs_between]))) + list(gps[i:])
				else:
					break_down(part, file_name, i)
					part += 1
			else:
				break_down(part)
				part += 1
		else:
			break_down(part)
			part += 1
	if(part > 1):
		# indicates that the trail has not been partitioned
		# nothing to do, exit
		return False

def sanitise_gps_from_time(file_name,dtype = {'names':('time',),'formats':('S8',)}):
	data = np.loadtxt(file_name,dtype=dtype,usecols=(2),delimiter=',',skiprows=1)
	# print(data)
	return check_jumps(data, file_name)

def sanitize_gps_from_date_time(file_name, dtype = {'names':('time',),'formats':('S19',)},usecols = 4):
	data = np.loadtxt(file_name,dtype=dtype,usecols=usecols,delimiter=',',skiprows=1)
	# print(data)
	times = [str(d).split(' ')[1] for d in data]
	# print(times)
	return check_jumps(times, file_name)

if __name__ == '__main__':
	import sys
	if '--file' in sys.argv:
		index = sys.argv.index('--file')
		file = sys.argv[index+1]
		print(file)
		sanitise_gps(file)
	# sanitise_gps_from_time('D:\\Personal Data\\Work\\m.tech\\Project\\up_3.txt')
	sanitize_gps_from_date_time('B.txt')