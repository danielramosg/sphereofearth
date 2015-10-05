# -*- coding: utf-8 -*-

# The Sphere of the Earth.
# Copyright (C) 2013 - 2015  Daniel Ramos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Author: Daniel Ramos
# daniel.ramos@imaginary.org



import sys, os
from PIL import Image
from math import *
from pyproj import Proj
from time import time

from mapping_routines import *


from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('param.ini')

src_img = params.get('Source_Image','src_img')
R0 = params.getfloat('Maps_Size','radius_of_the_globe')
resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')


try:
	ar=sys.argv[1]
except:
	print "Select 'poster' or 'program'"
	sys.exit()

if ar=="poster":
	from projections_monoscale import *
	outposter=True
	os.mkdir('./Posters')
elif ar=="program":
	from projections_multiscale import *
	outposter=False
else:
	print "Option not valid"
	sys.exit()




def print_size(PJ):
	dimx=int(PJ.width*MM2PX) 
	dimy=int(PJ.height*MM2PX)
	print "* Projection: " + PJ.name
	#print "Scale factor: ", sf
	print 'Earth radius: %.1f mm' % PJ.R
	print 'Size: %.2f x %.2f mm (%d x %d pixels at %d dpi)' % (PJ.width, PJ.height, dimx, dimy, resol)
	print ''


def make_map(PJ,grat,pdf=False):
	start=time()
	topo_map(PJ)
	gratpj = project_graticule(PJ,grat)
	merge_map_grat(PJ,gratpj,pdf)
	print "Done. Elapsed time: %.2f sec\n" % (time()-start)



tottime=time()

grat = standard_graticule()

for i in (PJ1,PJ2,PJ3,PJ4,PJ5,PJ6):	#Only PJ4 (Aziequi) and PJ5 (Gnomo) depend on the local coordinates.
	#print i.name 
	#print_size(i)
	make_map(i,grat,outposter)


print "Finished. Total elapsed time: %.2f sec\n" % (time()-tottime)



