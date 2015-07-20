#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
from math import *
from pyproj import Proj
from time import time

from mapping_routines import *

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('../param.ini')

src_img = params.get('Source_Image','src_img')
R0 = params.getfloat('Maps_Size','radius_of_the_globe')
resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')



MM2PX=resol/25.4  # pixels/mm  # 1 inch = 25.4 mm
PX2MM=1./MM2PX

def print_sizes():
	dimx=int(width*MM2PX) 
	dimy=int(height*MM2PX)
	print "Projection: " + name
	print "Scale factor: ", sf
	print 'Size: %.2f x %.2f mm (%d x %d pixels at %d dpi)' % (width, height, dimx, dimy, resol)
	print ''

def make_maps():
	start=time()
	topo_map(p,width,height,mask,name)
	gratpj = project_graticule(p,grat,mask)
	merge_map_grat(name,gratpj)
	print "Done. Elapsed time: %.2f sec\n" % (time()-start)


tottime=time()

grat = standard_graticule()


### Plate Carree ###
name = "platecarre"
sf = 1.
R=sf*R0

p=Proj(proj='eqc', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(xy):
	return True

#print_sizes()
make_maps()

### Mercator ###
name = "mercator"
sf = 1.
R=sf*R0

p=Proj(proj='merc', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,82)[1]  # Cut at 82 deg North and South   #height of the image, mm 

def mask(xy):
	return (fabs(xy[0])<1/2.*width and fabs(xy[1])<1/2.*height)

#print_sizes()
make_maps()

### Gall-Peters ###
name = "gallpeters"
sf=1. #sf = 1.4142312
R=sf*R0

p=Proj(proj='cea', lat_ts = 45, ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(xy):
	return True

#print_sizes()
make_maps()

### Azimuthal Equidistant ###
name = "aziequi"
sf = 1.
R=sf*R0

p = Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width = 2*pi*R  #width of the image, mm
height = width  #height of the image, mm 

def mask(xy):
	return (hypot(xy[0],xy[1]) < width/2.)

#print_sizes()
make_maps()

### Gnomonic ###
name = "gnomo"
sf=1. #sf = 1.1438848
R=sf*R0

p = Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width = 2*R*tan(70*3.14159265358979/180) # field of vision of 140 deg   #width of the image, mm
height = width  #height of the image, mm 

def mask(xy):
	return (fabs(xy[0])<1/2.*width and fabs(xy[1])<1/2.*width)

#print_sizes()
make_maps()

### Mollweide ###
name = "mollweide"
sf=1. #sf = 1.11077844
R=sf*R0

p=Proj(proj='moll', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]  #height of the image, mm 

def mask(xy):
	return (  (xy[0])**2/(width/2.)**2 + (xy[1])**2/(height/2.)**2 < 1.  ) 

#print_sizes()
make_maps()


print "Finished. Total elapsed time: %.2f sec\n" % (time()-tottime)



