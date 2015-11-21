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


params = ConfigParser.RawConfigParser(allow_no_value = True)
params.read(r'param.ini')
name = params.get('Center_of_projections','loc_name')
lon =  params.getfloat('Center_of_projections','longitude')
lat =  params.getfloat('Center_of_projections','latitude')


print """
#################################################
## Center location for The Sphere of the Earth ##
#################################################

The program The Sphere of the Earth contains six maps. 
Two of these maps (Azimuthal equidistant, Gnomonic) are centered on an arbitrary location. 
This script sets the center location.
You can use for instance Google Maps to find your coordinates (right click, "What's here?")

You can configure further parameters by editing the file param.ini.
WARNING: this script will overwrite any changes made manually to param.ini.
"""

print "The current location is %s (lat: %f, lon: %f)" % (name, lat, lon)

if raw_input("Continue?(y/n) --> ")!='y':
	print "Operation cancelled."
	sys.exit()

print "Set your local Latitude and Longitude. Use degrees with decimal places (point as separator)."

try:
	lat =  float(raw_input("Latitude (between -90 and 90) --> "))
	assert -90 <= lat and lat <= 90
except:
	print "Invalid latitude. Operation cancelled."
	sys.exit()

try:
	lon = float(raw_input("Longitude (between -180 and 180) --> "))
	assert -180 <= lon and lon <= 180
except:
	print "Invalid longitude. Operation cancelled."
	sys.exit()

name = raw_input("Name of the city/location (optional) --> ")


if raw_input("Save the location?(y/n) --> ")!='y':
	print "Operation cancelled."
	sys.exit()

params.set('Center_of_projections', 'longitude', lon)
params.set('Center_of_projections', 'latitude', lat)
params.set('Center_of_projections', 'loc_name', name)

configfile = open(r'param.ini', 'wb')
configfile.write(param_preamble)
params.write(configfile)
configfile.close()
print "Location saved. \n"

if raw_input("Do you want to generate the maps for the current location?(y/n) --> ")!='y':
	print "Maps not created. Finished."
	sys.exit()


#os.system('python create_images.py program')
from mapping_routines import *
from projections_multiscale import *

params=SafeConfigParser()
params.read('param.ini')

src_img = params.get('Source_Image','src_img')
R0 = params.getfloat('Maps_Size','radius_of_the_globe')
resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')

def make_map(PJ):
	start=time()
	topo_map(PJ)
	gratpj = project_graticule(PJ,grat)
	merge_map_grat(PJ,gratpj,False)
	print "Done. Elapsed time: %.2f sec\n" % (time()-start)

grat = standard_graticule()

for i in (PJ4,PJ5):	#Only PJ4 (Aziequi) and PJ5 (Gnomo) depend on the local coordinates.
	make_map(i)

print "Maps generated for your location. Finished."




