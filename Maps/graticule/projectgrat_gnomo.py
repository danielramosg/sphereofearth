#!/usr/bin/env python


from numpy import *
from pyproj import Proj

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('../../param.ini')

R = params.getfloat('Maps_Size','radius_of_the_globe')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')



p=Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)

wid=1/2.*(p(lon0+110,lat0)[0] - p(lon0-110,lat0)[0])


a=genfromtxt("grat.dat")
b=[]
for i in a.tolist():
	if isnan(i[0]) or isnan(i[1]):
		b.append([nan,nan])
	else:		
		z=p(i[0],i[1])
		if fabs(z[0])<wid and fabs(z[1])<wid :
			b.append([z[0],z[1]])
		else:
			b.append([nan,nan])
c=array(b)

#b=p(a[:,0],a[:,1])

#c=column_stack(b)
#c[c>1e29]=nan
savetxt("gratpj.dat",c, fmt='%.6f', delimiter='\t')

