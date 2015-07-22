#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from math import *
from pyproj import Proj
import types

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('param.ini')

#src_img = params.get('Source_Image','src_img')
R0 = params.getfloat('Maps_Size','radius_of_the_globe')
#resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')




class MyProj():
	def __init__(self, name, p, R, width, height):
		self.name=name
		self.p=p
		self.R=R
		self.width=width
		self.height=height
		#self.mask=mask


### Plate Carree ###
name = "platecarre"
sf = 1.
R=sf*R0

p=Proj(proj='eqc', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(pj,xy):
	return True

PJ1 = MyProj(name,p,R,width,height)
PJ1.mask = types.MethodType(mask,PJ1) 	#add a method to this instance of MyProj

### Mercator ###
name = "mercator"
sf = 1.
R=sf*R0

p=Proj(proj='merc', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,82)[1]  # Cut at 82 deg North and South   #height of the image, mm 

def mask(pj,xy):
	return (fabs(xy[0])<1/2.*pj.width and fabs(xy[1])<1/2.*pj.height)

PJ2 = MyProj(name,p,R,width,height)
PJ2.mask = types.MethodType(mask,PJ2)

### Gall-Peters ###
name = "gallpeters"
sf = 1.4142312
R=sf*R0

p=Proj(proj='cea', lat_ts = 45, ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(pj,xy):
	return True

PJ3 = MyProj(name,p,R,width,height)
PJ3.mask = types.MethodType(mask,PJ3)


### Azimuthal Equidistant ###
name = "aziequi"
sf = 1.
R=sf*R0

p = Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width = 2*pi*R  #width of the image, mm
height = width  #height of the image, mm 

def mask(pj,xy):
	return (hypot(xy[0],xy[1]) < pj.width/2.)

PJ4 = MyProj(name,p,R,width,height)
PJ4.mask = types.MethodType(mask,PJ4)

### Gnomonic ###
name = "gnomo"
sf = 1.1438848
R=sf*R0

p = Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width = 2*R*tan(70*3.14159265358979/180) # field of vision of 140 deg   #width of the image, mm
height = width  #height of the image, mm 

def mask(pj,xy):
	return ((fabs(xy[0]) < 1/2. * pj.width) and (fabs(xy[1]) < 1/2. * pj.width))

PJ5 = MyProj(name,p,R,width,height)
PJ5.mask = types.MethodType(mask,PJ5)

### Mollweide ###
name = "mollweide"
sf = 1.11077844
R=sf*R0

p=Proj(proj='moll', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]  #height of the image, mm 

def mask(pj,xy):
	return (  (xy[0])**2/(pj.width/2.)**2 + (xy[1])**2/(pj.height/2.)**2 < 1.  ) 

PJ6 = MyProj(name,p,R,width,height)
PJ6.mask = types.MethodType(mask,PJ6)



