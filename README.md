# Trans-Portal
Designing a intelligent transport system from mobile sensor logs

Steps and description:

 - Step 0:
 	Sanitize input files:
 	> TODO: First look for the travel modes, for this case, only bus trails to be taken. For trails of personalised vehicles, algorithmd like TrajDBSCAN might be useful. Go through the GPS log and check wheather the points have jumps in between. If the jump is small and does not change direction more than a certain angle, interpolate points in between them. If not create a seperate file for the bothw ends of the jump observed in the log. If the trail is very short(less than 15 mins / 8km maybe) they are probably not full trails but parts of trails. A slightly different approach is to be taken, not to create trail skeletons from these trails. Keep those in different folders perhaps.

 - Step 1:
 	Detect routes.
 	Code file: check_skeleton.py
 	Takes a file or folder as input and checks that file or all files in the folder.
 	If the current file is similar to any of the existing skeleton files, it returns the information or creates a new skeleton file out of the trail.
 	Methodology:
 		First some points are chosen at regular time gaps from the given trail to perform a rough estimation. Points are chosen one per 100(considering the log is taken in 1 second interval). Set of chosen points are compared with the existing skeletons to see how many points lie within 50 meters of the skeleton points. If no points are found, its a different route. If only one point found, it is a different route that intersects the current skeleton. If a set of points found, they are checked in detail whether they are nearby all along or not. In case there is a large distance between two consecutive close points, it is probably taking a different road to reach the same destination. Otherwise the trail is likely to be the same route.

 - Step 2:
 	Create a 'skeleton' of routes.
 	Code file: create_skeleton.py
 	Creates a skeleton of a given GPS trails. A skeleton is a trace of GPS points with a minimum gap of 100 meters.

 	> TODO: keep track of a minimum distance of a trail to avoid creation of small insignificant routes.