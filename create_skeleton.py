from utilities import get_spherical_distance
import uuid
import os
import numpy as np
from settings import *

def create_skeleton(gps,skel_folder='skeletons'):
	d = 0
	trail_length = 0
	id = uuid.uuid4()
	path = os.path.join(skel_folder,str(id))
	print(path)
	skel_file = open(path,'w')
	n = len(gps)
	for i in range(n-1):
		step = get_spherical_distance(gps[i][0],gps[i][1],gps[i+1][0],gps[i+1][1])
		d += step
		trail_length += step
		if (d>skip_rate):
			skel_file.write("{},{}\n".format(gps[i+1][0],gps[i+1][1]))
			d=0
	skel_file.close()
	routes_folder = os.path.join(data_location,'routes')
	# if(not os.path.exists(routes_folder)):
	os.makedirs(os.path.join(routes_folder,str(id))) 
	if trail_length < min_route_length:
		os.remove(path)
		return None
	return str(id)

def create_skeleton_from_file_path(file_path,usecols = (0,1),folder='skeletons'):
	file = open(file_path,'rb')
	gps = np.loadtxt(file,delimiter=',',usecols=usecols,skiprows=1)
	return create_skeleton(gps,folder)
if __name__ == '__main__':
	create_skeleton_from_file_path('up_1.txt')