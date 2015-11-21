#!/usr/env python

import ConfigParser
import sys, os


param_preamble = """
###############################################
#Configuration file for The Sphere of the Earth
#----------------------------------------------
#
# * Source image for the maps. You can use the get_source script to download from NASA website.
#	
# src_img 		Image file containing the topographic data of the Earth.
#
#
# * These options determine the final size of the images.
#
# radius_of_the_globe	The radius of your model of the Earth (in mm).
# resolution		The resolution in dots per inch (dpi).
#
#
# * Some projections use a center location (azimuthal equidistant, gnomonic). You can choose the center.
#
#location_name		Name of the city or location.
#longitude		Longitude of the city.
#latitude		Latitude of the city.
#
#Example:
#location_name = Barcelona
#longitude = 2.170035 
#latitude = 41.386996
#
###############################################
\n\n"""





def menu_location():
	params = ConfigParser.RawConfigParser(allow_no_value = True)
	params.read(r'param.ini')
	name = params.get('Center_of_projections','loc_name')
	lon =  params.getfloat('Center_of_projections','longitude')
	lat =  params.getfloat('Center_of_projections','latitude')

	print """
## Center location for The Sphere of the Earth ##

The program The Sphere of the Earth contains six maps. Two of these maps (Azimuthal equidistant, Gnomonic) are centered on an arbitrary location. You can use for instance Google Maps to find your coordinates (right click, "What's here?")
"""

	print "The current center location is \n%s (lat: %f, lon: %f)\n" % (name, lat, lon)

	if raw_input("Do you want to change the center location?(y/n) --> ")!='y':
		print "Operation cancelled."
		return 1

	print "Set your local Latitude and Longitude. Use degrees with decimal places (point as separator)."

	try:
		lat =  float(raw_input("Latitude (between -90 and 90) --> "))
		assert -90 <= lat and lat <= 90
	except:
		print "Invalid latitude. Operation cancelled."
		return 1

	try:
		lon = float(raw_input("Longitude (between -180 and 180) --> "))
		assert -180 <= lon and lon <= 180
	except:
		print "Invalid longitude. Operation cancelled."
		return 1

	name = raw_input("Name of the city/location (optional) --> ")


	if raw_input("Save the location?(y/n) --> ")!='y':
		print "Operation cancelled."
		return 1

	params.set('Center_of_projections', 'longitude', lon)
	params.set('Center_of_projections', 'latitude', lat)
	params.set('Center_of_projections', 'loc_name', name)

	configfile = open(r'param.ini', 'wb')
	configfile.write(param_preamble)
	params.write(configfile)
	configfile.close()
	print "Location saved. \n"

	if raw_input("Do you want to generate the two localized maps for the current location?(y/n) --> ")!='y':
		print "Maps not created. Finished."
		return 0

	#os.system('python create_images.py program')

	from projections_multiscale import PJ1,PJ2,PJ3,PJ4,PJ5,PJ6	

	for i in (PJ4,PJ5):	#Only PJ4 (Aziequi) and PJ5 (Gnomo) depend on the local coordinates.
		make_map(i,grat)

	print "Maps generated for your location. Finished."
	return 0

def menu_all_maps():
	print """
## Generate the maps for the program ##

This will generate all six maps for the program.
"""
	params = ConfigParser.SafeConfigParser()
	params.read(r'param.ini')
	name = params.get('Center_of_projections','loc_name')
	lon =  params.getfloat('Center_of_projections','longitude')
	lat =  params.getfloat('Center_of_projections','latitude')

	print "The current center location is \n%s (lat: %f, lon: %f)\n" % (name, lat, lon)

	if raw_input("Continue?(y/n) --> ")!='y':
		print "Operation cancelled."
		return 1

	from projections_multiscale import PJ1,PJ2,PJ3,PJ4,PJ5,PJ6	

	tottime=time()

	for i in (PJ1,PJ2,PJ3,PJ4,PJ5,PJ6):
		make_map(i,grat)

	print "Finished. Total elapsed time: %.2f sec\n" % (time()-tottime)
	return 0


## MAIN SCRIPT ##


menu_txt = """
Choose an option:
1. Configure the center location.
2. Generate all the maps for the program (required at least once).
3. Exit
"""
# Add more options?
# n. Generate pdf posters.
# n. Restore param.ini

print """
######################################
## Setup of The Sphere of the Earth ##
######################################

This script will help you to configure the program The Sphere of the Earth, including the center location and re-generating the maps. You can also configure further parameters by editing the file param.ini.
WARNING: this script will overwrite any changes made manually to param.ini.
"""
#print "The current center location is: \n%s (lat: %f, lon: %f)" % (name, lat, lon)


print "Checking dependencies..."
try:
	import numpy, pyproj, PyQt4, matplotlib.pyplot, PIL
	print "Done."
except ImportError:
	print "There are missing dependencies."
	import platform
	if platform.linux_distribution()[0] == 'Ubuntu':
		if raw_input("Install the software dependencies automatically?(y/n) --> ") =='y':
			os.system("sudo apt-get install python python-numpy python-pyproj python-qt4 python-scitools python-pil")
		else:
			print "Dependencies not installed."
			sys.exit()
	else:
		print "You need to install manually the following modules: numpy, pyproj, PyQt4, scitools, PIL."
		sys.exit()


print "Checking topographic data..."

params = ConfigParser.SafeConfigParser()
params.read(r'param.ini')
src_img = params.get('Source_Image','src_img')
if not os.path.isfile(src_img):
	print "Topographic data not found."
	if raw_input("Download the topographic image from NASA website?(y/n) --> ") =='y':
		print "Downloading..."
		import urllib2
		pg = urllib2.urlopen("http://eoimages.gsfc.nasa.gov/images/imagerecords/57000/57752/land_shallow_topo_8192.tif")
		f = open('land_shallow_topo_8192.tif','w')
		f.write(pg.read())
		f.close()
		print "Done."
	else:
		print "Download or create a base map and configure your settings in param.ini."
		sys.exit()
else:
	print "Done."

from mapping_routines import *

grat = standard_graticule()
print "Done."

while 1:
	try:
		opt = int(raw_input(menu_txt + "--> "))
	except:
		opt = 0

	if opt == 1:
		menu_location()
	elif opt == 2:
		menu_all_maps()
	elif opt == 3:
		print "Exit from the configuration script. Good bye. \n"
		sys.exit()
	else:
		print "Invalid option."



