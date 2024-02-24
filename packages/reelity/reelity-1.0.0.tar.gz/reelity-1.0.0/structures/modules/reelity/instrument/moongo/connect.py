
'''
	import reelity.instrument.moongo.connect as moongo_connect
	moongo_connection = moongo_connect.start ()
'''

def start ():
	mongo_client = pymongo.MongoClient ("mongodb://localhost:50001")
	return mongo_client