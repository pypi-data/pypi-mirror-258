
'''
	import reelity.instrument.moon.connect as moon_connect
	moon_connection = moon_connect.start ()
'''

def start ():
	mongo_client = pymongo.MongoClient ("mongodb://localhost:50001")
	return mongo_client