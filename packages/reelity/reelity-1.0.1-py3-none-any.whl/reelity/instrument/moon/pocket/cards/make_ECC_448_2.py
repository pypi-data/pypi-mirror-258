
'''
	import reelity.instrument.moon.cards.make_ECC_448_2 as make_ECC_448_2
	moon_connection = make_ECC_448_2.start (
		name = "",
		seed = ""
	)
'''

import pymongo

import reelity.instrument.moon.connect as moon_connect
import reelity.modules.EEC_448_2.keys as EEC_448_2_key_creator	

def start (
	name = "",
	seed = ""
):
	moon_connection = moon_connect.start ()
	cards = moon_connection ["pocket"] ["cards"]
	
	keys = EEC_448_2_key_creator.create (
		seed = seed
	)
	
	cards.insert_one ({
		"name": name,
		"format": "ECC_448_2",
		"public": {
			"hexadecimal string": keys ["public"] ["hexadecimal string"]
		},
		"private": {
			"hexadecimal string": keys ["private"] ["hexadecimal string"]
		},
		"seed": {
			"hexadecimal string": seed
		}
	})

	return;