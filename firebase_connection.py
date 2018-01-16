import pyrebase
import os
from settings import *

def get_new_files(config,storagepath='file_stream',dbpath="files"):
	firebase = pyrebase.initialize_app(config)

	db = firebase.database()
	storage = firebase.storage()

	if (storagepath.startswith('~/')):
		storagepath = storagepath[2:]
		os.chdir(data_location)
	if( not os.path.exists(storagepath)):
		os.makedirs(storagepath)

	try:
		files = db.child(dbpath).get()
		l = []
		for f in files.each():
			l = f.val()
			storage.child(l).download(storagepath+'/'+l)
	except Exception as e:
		print(e)
		pass

if __name__ == '__main__':
	from firebase_config import config
	get_new_files(config)