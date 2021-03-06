import pyrebase
import os
from settings import *

def get_new_files(config,storagepath='file_stream',dbpath="files"):
	downloaded_files = []
	firebase = pyrebase.initialize_app(config)
	if not storagepath.endswith('/'):
		storagepath += '/'
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
			try:
				l = f.val()
				key = f.key()
				print(l)
				storage.child(l).download(storagepath+l)
				db.child(dbpath).child(key).remove()
				storage.delete(l)
				downloaded_files.append(l)
			except Exception as e:
				print(e)
	except Exception as e:
		print(e)
		pass
	return downloaded_files

if __name__ == '__main__':
	from firebase_config import config
	get_new_files(config)