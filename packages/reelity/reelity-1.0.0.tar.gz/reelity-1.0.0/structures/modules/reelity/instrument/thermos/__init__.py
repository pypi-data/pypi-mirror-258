

'''

'''


import json
from os.path import dirname, join, normpath
import os
import traceback


import rich
from flask import Flask, request

import reelity.instrument.thermos.routes.home.get as get_home_route
import reelity.instrument.thermos.routes.card_generator as card_generator
import reelity.instrument.thermos.routes.vue as vue_route
import reelity.instrument.thermos.routes.moves as moves_route

import reelity.instrument.thermos.utilities.generate_path_inventory as generate_path_inventory
import reelity.instrument.climate as instrument_climate
	

def build (
	records = 1
):
	climate = instrument_climate.retrieve ()

	print ("starting instrument flask service")
	rich.print_json (data = {
		"variables": {
			"frontend dist": climate ["paths"] ["frontend dist"]
		}
	})

	app = Flask (__name__)
	
	vue_dist_inventory = generate_path_inventory.beautifully (
		climate ["paths"] ["frontend dist"]
	)
	for entry in vue_dist_inventory:
		print (vue_dist_inventory [entry] ["path"])
	
	vue_route.route (app, vue_dist_inventory)
	card_generator.route (app)
	moves_route.route (app)

	@app.route ("/", methods = [ 'GET' ])
	def route_GET ():
		return get_home_route.present ()	

	@app.route ("/example", methods = [ 'GET' ])
	def route_GET_example ():
		return get_home_route.present ()

	
	
	return app;