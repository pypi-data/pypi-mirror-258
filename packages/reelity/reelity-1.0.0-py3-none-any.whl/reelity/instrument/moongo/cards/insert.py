
'''
	import reelity.instrument.moongo.cards.insert as insert_card
	moongo_connection = insert_card.start ()
'''

import pymongo
import reelity.instrument.moongo.connect as moongo_connect

def start ():
	moongo_connection = moongo_connect.start ()
	pouch = moongo_connection ["pouch"]
	cards = moongo_connection ["cards"]

	cards.insert_one ({
		"public": {
			"hexadecimal string": ""
		},
		"private": {
			"hexadecimal string": ""
		},
		"seed": {
			"hexadecimal string": ""
		}
	})

	return;