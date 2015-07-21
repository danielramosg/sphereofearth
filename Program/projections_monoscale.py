#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from math import *
from pyproj import Proj


from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('param.ini')

#src_img = params.get('Source_Image','src_img')
R0 = params.getfloat('Maps_Size','radius_of_the_globe')
#resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')




class MyProj():
	def __init__(self, name, p, R, width, height, mask):
		self.name=name
		self.p=p
		self.R=R
		self.width=width
		self.height=height
		self.mask=mask


### Plate Carree ###
name = "platecarre"
sf = 1.
R=sf*R0

p1=Proj(proj='eqc', ellps='sphere', a=R, b=R)

width1 = 2*p1(180,0)[0]   #width of the image, mm
height1 = 2*p1(0,90)[1]   #height of the image, mm 

def mask1(xy):
	return True

PJ1 = MyProj(name,p1,R,width1,height1,mask1)


### Mercator ###
name = "mercator"
sf = 1.
R=sf*R0

p2=Proj(proj='merc', ellps='sphere', a=R, b=R)

width2 = 2*p2(180,0)[0]   #width of the image, mm
height2 = 2*p2(0,82)[1]  # Cut at 82 deg North and South   #height of the image, mm 

def mask2(xy):
	return (fabs(xy[0])<1/2.*width2 and fabs(xy[1])<1/2.*height2)

PJ2 = MyProj(name,p2,R,width2,height2,mask2)


### Gall-Peters ###
name = "gallpeters"
sf = 1. #1.4142312
R=sf*R0

p3=Proj(proj='cea', lat_ts = 45, ellps='sphere', a=R, b=R)

width3 = 2*p3(180,0)[0]   #width of the image, mm
height3 = 2*p3(0,90)[1]   #height of the image, mm 

def mask3(xy):
	return True

PJ3 = MyProj(name,p3,R,width3,height3,mask3)


### Azimuthal Equidistant ###
name = "aziequi"
sf = 1.
R=sf*R0

p4 = Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width4 = 2*pi*R  #width of the image, mm
height4 = width4  #height of the image, mm 

def mask4(xy):
	return (hypot(xy[0],xy[1]) < width4/2.)

PJ4 = MyProj(name,p4,R,width4,height4,mask4)


### Gnomonic ###
name = "gnomo"
sf = 1. #1.1438848
R=sf*R0

p5 = Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width5 = 2*R*tan(70*3.14159265358979/180) # field of vision of 140 deg   #width of the image, mm
height5 = width5  #height of the image, mm 

def mask5(xy):
	return (fabs(xy[0])<1/2.*width5 and fabs(xy[1])<1/2.*width5)

PJ5 = MyProj(name,p5,R,width5,height5,mask5)

### Mollweide ###
name = "mollweide"
sf = 1. #1.11077844
R=sf*R0

p6=Proj(proj='moll', ellps='sphere', a=R, b=R)

width6 = 2*p6(180,0)[0]   #width of the image, mm
height6 = 2*p6(0,90)[1]  #height of the image, mm 

def mask6(xy):
	return (  (xy[0])**2/(width6/2.)**2 + (xy[1])**2/(height6/2.)**2 < 1.  ) 

PJ6 = MyProj(name,p6,R,width6,height6,mask6)



