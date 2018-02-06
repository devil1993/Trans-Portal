import os
from utilities import get_spherical_distance
import numpy as np

def union(list1,list2):
	res = list1
	for i in list2:
		if not (i in res):
			res.append(i)
	return res

def get_neighbours(point,pointSet,eps):
	N = []
	for pt in pointSet:
		#if pointSet.index(point)>pointSet.index(pt):
			#continue
		#print (pt[0] - point[0]),(pt[1] - point[1])
		
		'''
		dist = math.pow(10000*(pt[1] - point[1]),2.0) + math.pow(10000*(pt[0] - point[0]),2.0)
		dist = math.sqrt(dist)
		dist_n = dist/10000
		#file.write(str(dist_n)+'\n')
		'''
		dist = get_spherical_distance(pt[0],pt[1],point[0],point[1])
		if dist<=eps:
			N.append(pt)
	return N

def findStops(folderName,tc,speed_threshold, stopRadi,stopFileName):
	files = os.listdir(folderName)
	slow_points = []
	for file in files:
		slows = []
		slowsets = []
		f = open(os.path.join(folderName,file),'r')
		lines = f.read().split('\n')
		f.close()
		pointSet = []
		for line in lines:
			components = line.split(',')
			try:
				point_x = float(components[0])
				point_y = float(components[1])
				#split time into hours, minutes and seconds
				timeunits = components[2].split(':')
				#convert the time into seconds
				point_t = ((int(timeunits[0])*60) + int(timeunits[1])) * 60 + int(timeunits[2])
				pointSet += [(point_x,point_y,point_t)]
			except Exception as e:
				# print(e)
				pass
		for i in range(len(pointSet)-1):
			d = get_spherical_distance(pointSet[i][0],pointSet[i][1],pointSet[i+1][0],pointSet[i+1][1])
			if (pointSet[i+1][2] - pointSet[i][2])==0:
				continue
			if (d/(pointSet[i+1][2] - pointSet[i][2])) <= speed_threshold:
				slows.append(pointSet[i+1])
		for i in range(len(slows)-1):
			if len(slowsets)==0:
				slowsets.append(slows[i])
			d = get_spherical_distance(slows[i][0],slows[i][1],slows[i+1][0],slows[i+1][1])
			if d<=stopRadi:
				slowsets.append(slows[i+1])
			else:
				slow_points.append(slowsets)
				slowsets = []
	# print(slow_points)
	# print(len(slow_points))
	slows = []
	centers = []
	for point in slow_points:
		# print(point)
		contribution = len(point)
		data = np.array(point)
		mean = np.mean(data[:,0:2],axis=0)
		std = np.std(data[:,0:2],axis=0)
		# print(contribution,mean)
		slows.append((contribution,mean,std))
		centers.append(mean.tolist())
		# break
	# print(len(centers))
	# centers = centers.tolist()
	pts = centers[:]

	ps = []
	for point in centers:
		if(point not in pts):
			continue
		pts.remove(point)
		#print len(pts), len(pointSet)
		N = get_neighbours(point,pts,stopRadi)	
		C = [point]
		# print(C, N)
		C = union(C,N)
		for n in N:
			pts.remove(n)
		# print(len(pts))
		while len(N)>0:
			#print "Neighbour ", neighbour
			N = []
			for c in C:
				n = get_neighbours(c,pts,stopRadi)
				N = union(N,n)
				for i in n:
					pts.remove(i)
			C = union(C,N) 
		ps.append(C)
	res = []
	for p in ps:
		if(len(p)>tc*len(files)):
			print(len(p))
			mean = np.mean(p,axis=0)
			res.append(mean)

	for r in res:
		print(r[0],',',r[1])

if __name__ == '__main__':
	findStops('G:/Repos/BusStoppage/Busstop/trails/A',0.5,0,30,'stop.txt')