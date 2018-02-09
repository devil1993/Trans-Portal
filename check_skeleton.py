from utilities import get_spherical_distance
import os
import numpy as np
from create_skeleton import create_skeleton_from_file_path
from settings import *
from shutil import copy
import codecs

def check_skeleton(filename,skel_folder='skeletons',usecols=(0,1)):
	print(filename)
	filecp = codecs.open(filename, 'rb') #encoding = 'cp1252'
	data = np.loadtxt(filecp,delimiter=',',usecols=usecols,skiprows=1)
	filecp.close()
	# pick out some of the data points to try matching
	fewdata = data[0::jump_seconds]
	# for p in fewdata:
	# 	print(p)
	print(len(fewdata))
	create_new = True
	to_remove = []
	if (not os.path.exists(skel_folder)):
		os.makedirs(skel_folder)
	skeletons = os.listdir(skel_folder)
	curdir = os.getcwd()
	os.chdir(skel_folder)

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
	
	if (not os.path.exists(arch)):
		os.makedirs(arch)
	if (not os.path.exists(os.path.join(curdir,'routes'))):
		os.makedirs(os.path.join(curdir,'routes'))
	
	matches = []
	for skeleton in skeletons:
		print('For Skeleton',skeleton)
		skel_data = np.loadtxt(skeleton,delimiter=',',usecols=usecols,skiprows=0)
		points = find_close_points(fewdata,skel_data)
		# for p in points:
		# 	print(p)
		# print(len(points))
		result = find_relation(data,skel_data,points)
		# POSSIBLE VALUES:
		# different
		# crossing
		# opposite_direction
		# match
		# superroute
		# can_be_extended
		print(result)
		if result == 'match':
			create_new = False
			matches.append(skeleton)
		if result == 'superroute':
			print('Removing',skeleton,'for',filename)
			to_remove.append(skeleton)
	os.chdir(curdir)
	sk = None
	parts = filename.split(os.path.sep)
	if(len(parts) == 1):
		parts = filename.split('/')
	
	if create_new:
		sk = create_skeleton_from_file_path(filename)
		if (sk == None):
			print('Skeleton','not','created')
		else:	
			print('Skeleton',sk,'created')
			# print(filename)
			os.makedirs(os.path.join(curdir,'routes',sk))
			copy(filename,os.path.join(curdir,'routes',sk,parts[-1]))
	else:
		for match in matches:
			copy(filename,os.path.join(curdir,'routes',match,parts[-1]))
	for file in to_remove:
		# Replace all trails in routes that going to be deleted into the newly created routes folder/matching folder
		# get the trails in the route that is to be deleted
		path = os.path.join(curdir,'routes')
		route_path = os.path.join(path,file)
		trails = os.listdir(route_path)
		for trail in trails:
			for match in matches:
				os.rename(os.path.join(route_path,trail),os.path.join(path,match,trail))
		os.remove(file)
		os.rmdir(route_path)
	# Move current file to archive folder
	os.rename(filename,os.path.join(arch,parts[-1]))

def find_relation(data_points,skel,close_pairs=None):
	if close_pairs == None:
		close_pairs = find_close_points(data_points[0::jump_seconds],skel)
	close_pairs = np.array(close_pairs)

	if(len(close_pairs)<1):
		return 'different'

	if(len(close_pairs) == 1):
		return 'crossing'
	
	# check direction first:
	first_close_data = close_pairs[0][1]
	first_close_skel = close_pairs[0][0]

	last_close_data = close_pairs[-1][1]
	last_close_skel = close_pairs[-1][0]

	# print(first_close_data,first_close_skel,last_close_data,last_close_skel)

	first_skel_index = np.where(np.all(skel==first_close_skel,axis=1))[0][0]
	last_skel_index = np.where(np.all(skel==last_close_skel,axis=1))[0][0]

	# print(first_skel_index,last_skel_index)
	
	first_data_index = np.where(np.all(data_points==first_close_data,axis=1))[0][0]
	last_data_index = np.where(np.all(data_points==last_close_data,axis=1))[0][0]

	# print(first_data_index,last_data_index)

	# Find direction
	if (first_skel_index<last_skel_index):
		dir_skel = True
	else:
		dir_skel = False

	if first_data_index<last_data_index:
		dir_data = True
	else:
		dir_data = False
		
	if dir_data == dir_skel:
		pass
	else:
		return 'opposite_direction'

	# Find same route or not
	# Either non leaving full middle
	# Or late matching non leaving end
	# Or start non leaving early end
	

	# skel_indexes = []
	# if dir_skel:
	# 	skel_indexes = range(first_skel_index,last_skel_index+1)
	# else:
	# 	skel_indexes = range(first_skel_index,last_skel_index-1,-1)

	close_skels = close_pairs[:,0]
	different_route = False
	for i in range(len(close_skels)-1):
		this_bone_index = np.where(np.all(skel==close_skels[i],axis=1))[0][0]
		next_bone_index = np.where(np.all(skel==close_skels[i+1],axis=1))[0][0]
		# print(this_bone_index,next_bone_index)

		if abs(this_bone_index - next_bone_index)>1:
			# if skipp is over 2 KM, simply consider a different route:
			if abs(this_bone_index - next_bone_index)>20:	
				# print('different route')
				different_route = True
				break
			# look for missing bones
			# Find the position in data file, look upto 1 KM if any of the skipped part does not arrive,
			# its a different route, but to be sure some more checking to be perormed
			nearest_data = close_pairs[i,1]
			next_match_data = close_pairs[i+1,1]
			# find the actual place in the data file
			index_of_last_found = np.where(np.all(data_points==nearest_data,axis=1))[0][-1]
			index_of_next_found = np.where(np.all(data_points==next_match_data,axis=1))[0][0]
			# print(index_of_last_found,index_of_next_found)
			
			found = this_bone_index
			d = 0
			for j in range(index_of_last_found,index_of_next_found-1):
				d += get_spherical_distance(data_points[j][0],data_points[j][1],data_points[j+1][0],data_points[j+1][1])
				
				# check if any of the skipped points come up
				target = found + 4
				if target > len(skel)-1:
					target = len(skel)-1
				for skipped_points in range(found+1,target):
					distance = get_spherical_distance(data_points[j][0],data_points[j][1],skel[skipped_points][0],skel[skipped_points][1])
					if distance<=d2:
						found = skipped_points
						d = 0
				if(d>d1) or found == next_bone_index-1:
					break
			if not (found+1 == next_bone_index):
				different_route = True
				# print('different route1')
				break 
	if not different_route:
		# decide a part or full
		# print(first_skel_index,last_skel_index,first_data_index,last_data_index)
		
		# Check how far the trail start and finish points are from the nearest skeleton point
		d = 0
		far_start = False
		far_end = False
		target = first_skel_index -1
		if(not first_data_index == 0):
			print('Non matching start')
			for i in range(first_data_index,0,-1):
				if target >= 0:
					dist_prev_skel = get_spherical_distance(data_points[i][0],data_points[i][1],skel[target][0],skel[target][1])
					if dist_prev_skel < d2:
						first_skel_index = target
						if target > 0:
							target -= 1
						d = 0
						continue
				d += get_spherical_distance(data_points[i][0],data_points[i][1],data_points[i-1][0],data_points[i-1][1])
				if d>d1:
					far_start = True
					break

		print('Start',d)
		d = 0
		target = last_skel_index + 1
		if(last_data_index < len(data_points)-1):
			print('Non matching finish')
			for i in range(last_data_index,len(data_points)-1):
				if target < len(skel):
					dist_next_skel = get_spherical_distance(data_points[i][0],data_points[i][1],skel[target][0],skel[target][1])
					if dist_next_skel < d2:
						last_skel_index = target
						if target < len(skel)-1:
							target += 1
						d = 0
						continue
				d += get_spherical_distance(data_points[i][0],data_points[i][1],data_points[i+1][0],data_points[i+1][1])
				if d>d1:
					far_end = True
					break
		print('End',d)
		
		# if none of the points are far from the nearest skeleton point, then the trail is definately a subroute of the skeleton

		if(not (far_end or far_start)):
			return 'match'
		else:
			# else we must check wheather it is a overlapping and different route...
			# in that case, the first and/or last close skeleton points should not be the begining and ending 
			# point of the skeleton, that case, its a direct different route.
			
			# print(first_skel_index,last_skel_index)
			if(first_skel_index > 0 and last_skel_index < len(skel) -1):
				return 'different'
			# else, must check if the trail extends starting point of skeleton or the ending point of  the skeleton
			if(first_skel_index == 0 and last_skel_index == len(skel) - 1):
				# extending the route
				return 'superroute'
			else:
				return 'can_be_extended'	
	# Else not same route
	else:
		return 'different'

def find_close_points(data,skeleton):
	# print(data)
	points = []
	for d in data:
		matched = False
		for s in skeleton:
			if get_spherical_distance(d[0],d[1],s[0],s[1])<d2:
				points.append([s,d])
				matched= True
				break
		# if not matched:
		# 	print('Not matched',d)
	return points

if __name__ == '__main__':
	# check_skeleton('up_3.txt')
	import sys
	if '--folder' in sys.argv:
		index = sys.argv.index('--folder')
		folder = sys.argv[index+1]
		if folder.startswith('~/'):
			folder = folder[2:]
			# folder = os.path.join(data_location,folder_name)
			os.chdir(data_location)
		for file in os.listdir(folder):
			print(file)
			check_skeleton(os.path.join(folder,file))
	if '--file' in sys.argv:
		index = sys.argv.index('--file')
		file = sys.argv[index+1]
		print(file)
		check_skeleton(file)
	# print(os.listdir(data_location))