from tkinter import *
from tkinter import ttk
import os
from file_merge import merge
from check_skeleton import check_skeleton
from settings import *
from firebase_connection import get_new_files
from BusStopFinder import *


def calculate():
	pass


window = Tk()

window.title("Trans-Portal : Admin panel")


mainframe = ttk.Frame(window, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

file_location = StringVar()
f_loc = ttk.Entry(mainframe, textvariable=file_location)

feet = StringVar()
meters = StringVar()

feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

feet_entry.focus()
window.bind('<Return>', calculate)



window.mainloop()

def downloadFromFirebase():
	from firebase_config import config
	get_new_files(config,file_location)
