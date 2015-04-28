#!/usr/bin/env python

import sys
from numpy import *
from pyproj import Proj

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('../../param.ini')

R = params.getfloat('Maps_Size','radius_of_the_globe')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')


proje=sys.argv[1]
print proje

if proje == 'mollweide':
	p=Proj(proj='moll',ellps='sphere', a=R, b=R)
elif proje == 'pc':
	p=Proj(proj='eqc', ellps='sphere',a=R,b=R)
elif proje == 'aziequi':
	p=Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)
elif proje == 'gallpeters':
	p=Proj(proj='cea', lat_ts = 45, ellps='sphere', a=R, b=R)
elif proje == 'gnomo':
	#p=Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)
	print "Gnomonic must be done manually"
elif proje == 'merc':
	p=Proj(proj='merc', ellps='sphere', a=R, b=R) 
	print "Warning: Change grat.dat to maxparal = 82"
else:
	sys.exit("Add the desired projection")



a=genfromtxt("grat.dat")
b=p(a[:,0],a[:,1])
c=column_stack(b)
#print type(c)
c[c>1e29]=nan
savetxt("gratpj.dat",c, fmt='%.6f', delimiter='\t')

