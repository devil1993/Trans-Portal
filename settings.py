# Minimum distance to skip in meters for skeleton creation.
skip_rate = 100
# seconds to skip while creating the estimate trail from raw trail
jump_seconds = 100
# Distance vehicle can travel away from route, used in case of identifying trails that leave a skeleton and then join again.
d1 = 1000 # meters
# Distance to measure closeness towards skeleton points
d2 = 60 # meters
# minimum length of a route
min_route_length = 8000 # meters
# Define distance and angle that can be interpolared
allowed_distance = 100 # meters 
allowed_time = 10 # seconds
allowed_angle = 15 # degrees
# Data file location
data_location = 'G:/Repos/Trans-Portal'
# BusStopFinderCodeLocation
bsf_location = '../BusStopage/Busstop/'
# Feature Extraction Code Location
fa_location = '../RoadNatureDetection/'
# archive location
archive = './archive/'