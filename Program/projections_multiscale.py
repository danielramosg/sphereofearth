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

from math import *
from pyproj import Proj
import types

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):     # "bundled" on a executable
	application_path = os.path.dirname(sys.executable)
elif __file__:     # "live" script, running using an interpreter
	application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, 'param.ini')

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read(config_path)

#src_img = params.get('Source_Image','src_img')
R0 = params.getfloat('Maps_Size','radius_of_the_globe')
#resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')




class MyProj():
	def __init__(self, name, fullname, p, R, width, height):
		self.name=name
		self.fullname=fullname
		self.p=p
		self.R=R
		self.width=width
		self.height=height
		#self.mask=mask
PJlist =[]

### Plate Carree ###
name = "platecarre"
fullname = u"Plate Carrée"
sf = 1.
R=sf*R0

p=Proj(proj='eqc', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(pj,xy):
	return True

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ) 	#add a method to this instance of MyProj
PJlist.append(PJ)


### Mercator ###
name = "mercator"
fullname = u"Mercator"
sf = 1.
R=sf*R0

p=Proj(proj='merc', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,82)[1]  # Cut at 82 deg North and South   #height of the image, mm 

def mask(pj,xy):
	return (fabs(xy[0])<1/2.*pj.width and fabs(xy[1])<1/2.*pj.height)

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Gall-Peters ###
name = "gallpeters"
fullname = u"Gall-Peters"
sf = 1.4142312
R=sf*R0

p=Proj(proj='cea', lat_ts = 45, ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(pj,xy):
	return True

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Azimuthal Equidistant ###
name = "aziequi"
fullname = u"Azimuthal Equidistant"
sf = 1.
R=sf*R0

p = Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width = 2*pi*R  #width of the image, mm
height = width  #height of the image, mm 

def mask(pj,xy):
	return (hypot(xy[0],xy[1]) < pj.width/2.)

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Gnomonic ###
name = "gnomo"
fullname = u"Gnomonic"
sf = 1.1438848
R=sf*R0

p = Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

width = 2*R*tan(70*3.14159265358979/180) # field of vision of 140 deg   #width of the image, mm
height = width  #height of the image, mm 

def mask(pj,xy):
	return ((fabs(xy[0]) < 1/2. * pj.width) and (fabs(xy[1]) < 1/2. * pj.width))

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Mollweide ###
name = "mollweide"
fullname = u"Mollweide"
sf = 1.11077844
R=sf*R0

p=Proj(proj='moll', ellps='sphere', a=R, b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]  #height of the image, mm 

def mask(pj,xy):
	return (  (xy[0])**2/(pj.width/2.)**2 + (xy[1])**2/(pj.height/2.)**2 < 1.  ) 

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Stereographic ###
name = "stere"
fullname = u"Stereographic"
sf = 1.1438848
R=sf*R0
p = Proj(proj='stere', ellps='sphere',a=R,b=R)

width = 2*R*tan(70*3.14159265358979/180) # field of vision of 140 deg   #width of the image, mm
height = width  #height of the image, mm 

def mask(pj,xy):
	return ((fabs(xy[0]) < 1/2. * pj.width) and (fabs(xy[1]) < 1/2. * pj.width))

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### van der Grinten ###
name = "vandg"
fullname = u"van der Grinten"
sf = 1.1438848
R=sf*R0
p = Proj(proj='vandg', ellps='sphere',a=R,b=R)

width = 2*pi*R  #width of the image, mm
height = width  #height of the image, mm 

def mask(pj,xy):
	return (hypot(xy[0],xy[1]) < pj.width/2.)

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

#### Winkel Tripel ###
#name = "wintri"
#fullname = u"Winkel Tripel"
#sf = 1.1438848
#R=sf*R0
#p = Proj(proj='wintri', ellps='sphere',a=R,b=R)

#width = 2*p(180,0)[0]   #width of the image, mm
#height = 2*p(0,90)[1]   #height of the image, mm 

#def mask(pj,xy):
#	return True #(hypot(xy[0],xy[1]) < pj.width/2.)

#PJ = MyProj(name,fullname,p,R,width,height)
#PJ.mask = types.MethodType(mask,PJ)
#PJlist.append(PJ)

### Interrupted Goode Homolosine ###
name = "goode"
fullname = u"Goode Homolosine"
sf = 1.1438848
R=sf*R0
p = Proj(proj='igh', ellps='sphere',a=R,b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(pj,xy):
	return True 

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Sinusoidal ###
name = "sinu"
fullname = u"Sinusoidal"
sf = 1.1438848
R=sf*R0
p = Proj(proj='sinu', ellps='sphere',a=R,b=R)

width = 2*p(180,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]   #height of the image, mm 

def mask(pj,xy):
	return fabs(xy[0]) <= pj.width/2. * cos(fabs(xy[1]) / float(pj.height) * 3.141592)   

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)

### Transversal Mercator ###
name = "tmerc"
fullname = u"Transversal Mercator"
sf = 1.
R=sf*R0

p=Proj(proj='tmerc', ellps='sphere', a=R, b=R)

width = 200 #2*p(90,0)[0]   #width of the image, mm
height = 2*p(0,90)[1]  #height of the image, mm 

def mask(pj,xy):
	return (fabs(xy[0])<1/2.*pj.width and fabs(xy[1])<1/2.*pj.height)

PJ = MyProj(name,fullname,p,R,width,height)
PJ.mask = types.MethodType(mask,PJ)
PJlist.append(PJ)


