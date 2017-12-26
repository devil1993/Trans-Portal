# sanitise_gps.py

import numpy as np

def sanitise_gps(file_name):
	data = np.loadtxt(file_name,dtype={'names':('time',),'formats':('S8',)},usecols=(2),delimiter=',',skiprows=1)
	print(data)
if __name__ == '__main__':
	import sys
	if '--file' in sys.argv:
		index = sys.argv.index('--file')
		file = sys.argv[index+1]
		print(file)
		sanitise_gps(file)
	sanitise_gps('D:\\Personal Data\\Work\\m.tech\\Project\\up_1.txt')