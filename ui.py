from tkinter import *
from tkinter import ttk
import os
from file_merge import merge
from check_skeleton import check_skeleton
from settings import *
from firebase_connection import get_new_files
from BusStopFinder import *
from tkinter.messagebox import showinfo


def downloadFromFirebase(f_loc):
	file_loc = f_loc.get()
	# showinfo('Window',file_loc)
	from firebase_config import config
	dwnld= get_new_files(config,file_loc)
	# dwnld = ['a','s','d','f']
	global msg1
	msg.set(str(len(dwnld)) + ' files downloaded in: ' + file_loc)
	files = ''
	for f in dwnld:
		files += f + '\n'
	showinfo('Window',files)

def mergeFiles(file_loc,file_location):
	merged_file_location = file_loc.get()
	files = os.listdir(file_location)
	curdir = os.getcwd()

	ids = []
	for file in files:
		identifiers = file.split('.')[0].split('_')
		id = identifiers[-1]
		if (id not in ids) and (('bus' in identifiers) or ('BUS' in identifiers)):
			ids.append(id) 
	global msg2
	msg2.set('List of IDs merging'+str(ids))

	# Merge related files
	# Check and create skeletons

	for id in ids:
		try:
			print(id)
			merge(id,file_location)
			os.rename(file_location+id+'.txt',merged_file_location+id+'.txt')
		except Exception as e:
			showinfo('Window','Exception in merging and archiving '+str(id)+'\n'+str(e))

def routeAnalysis(merged_file_location):
	try:
		trails = os.listdir(merged_file_location)
		for id in trails:
			try:
				check_skeleton(merged_file_location+id)
			except Exception as e:
				showinfo('Window','Exception in route analysis of '+str(id)+'\n'+str(e))
	except Exception as e:
		showinfo('Window','Exception in route analysis.\n'+str(e))


window = Tk()

window.title("Trans-Portal : Admin panel")


mainframe = ttk.Frame(window, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# ===================================================================File Download Section=============================================================
msg1 = StringVar()
file_location = StringVar()
f_loc = ttk.Entry(mainframe, textvariable=file_location)
f_loc.grid(column=1, row=1, sticky=(W, E))

ttk.Button(mainframe, text="Get files from Firebase", command=lambda:downloadFromFirebase(file_location)).grid(column=1, row=2, sticky=W)

label = ttk.Label(mainframe, textvariable = msg1)
label.grid(column=3, row=1, sticky=W)

file_location.set('./file_stream/')

# ===================================================================File Merge Section=============================================================
msg2 = StringVar()
merged_file_location = StringVar()
f_loc1 = ttk.Entry(mainframe, textvariable=merged_file_location)
f_loc1.grid(column=1, row=4, sticky=(W, E))

ttk.Button(mainframe, text="Merge sensor data of bus", command=lambda:mergeFiles(merged_file_location,file_location.get())).grid(column=1, row=5, sticky=W)

label = ttk.Label(mainframe, textvariable = msg2)
label.grid(column=3, row=4, sticky=W)

merged_file_location.set('./merged_file_stream/')


# ===================================================================Skeleton Checking and Creation==================================================

msg3 = StringVar()

ttk.Button(mainframe, text="Perform Route Analysis", command=lambda:routeAnalysis(merged_file_location.get())).grid(column=1, row=7, sticky=W)

label = ttk.Label(mainframe, textvariable = msg3)
label.grid(column=1, row=6, sticky=W)

# merged_file_location.set('./merged_file_stream/')



# feet = StringVar()
# meters = StringVar()

# feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
# feet_entry.grid(column=2, row=1, sticky=(W, E))

# ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
# ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
# ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
# ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# feet_entry.focus()
# window.bind('<Return>', calculate)



window.mainloop()
