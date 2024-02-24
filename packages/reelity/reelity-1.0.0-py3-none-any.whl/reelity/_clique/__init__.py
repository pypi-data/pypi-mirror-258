




#from reelity._clique.group import clique as clique_group

#import reelity.instrument.awareness_sockets.clique_group as clique_group
#from reelity.instrument.clique_tracks import clique as instrument_clique_tracks
#from reelity.instrument.clique_socket import clique as instrument_clique_socket


def intro ():

	import click
	@click.group ()
	def group ():
		pass

	import click
	@click.command ("tutorial")
	def sphene_command ():	
		import pathlib
		from os.path import dirname, join, normpath
		this_directory = str (pathlib.Path (__file__).parent.resolve ())
		module_directory = str (normpath (join (this_directory, "..")));

		import carbonado
		carbonado.start ({			
			#
			#	This is the node from which the traversal occur.
			#
			"directory": module_directory,
			
			#
			#	This path is removed from the absolute path of share files found.
			#
			"relative path": module_directory
		})
		
		import time
		while True:
			time.sleep (1000)

	group.add_command (sphene_command)
	
	
	#group.add_command (clique_group.add ())
	
	
	#group.add_command (vibes_clique ())
	
	
	return group;




#
