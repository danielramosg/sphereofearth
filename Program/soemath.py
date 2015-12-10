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

from pyproj import Proj
from math import *
import numpy as np

H=1e-5 # Derivatives

def Tissot (x,y,p,R):
	#p=PJ.p
	#R=PJ.R	
	# lon, lat coordinates of the point
	(lam, phi) = p(x,y,inverse=True, radians=True)
	#print 'coords: ', lam, phi

	# partial derivatives
	(x0,y0) = p(lam - H/2. , phi , radians=True)
	(x1,y1) = p(lam + H/2. , phi , radians=True)
	dxdl = (x1 - x0)/H
	dydl = (y1 - y0)/H
	(x0,y0) = p(lam , phi - H/2. , radians=True) 
	(x1,y1) = p(lam , phi + H/2. , radians=True)
	dxdp = (x1 - x0)/H
	dydp = (y1 - y0)/H	
	#print 'dxdp= %.4f dydp= %.4f dxdl= %.4f dydl= %.4f ' % (dxdp, dydp, dxdl, dydl)

	# parameters for the ellipse
	h = 1/R * sqrt(fabs( dxdp**2 + dydp**2 )) 
	k = 1/(R*cos(phi)) * sqrt(fabs( dxdl**2 + dydl**2 ))
	stp = 1/(R**2*h*k*cos(phi)) * (dydp*dxdl - dxdp*dydl)
	ap = sqrt(fabs(h**2 + k**2 + 2.*h*k*stp))
	bp = sqrt(fabs(h**2 + k**2 - 2.*h*k*stp))
	a = (ap+bp)/2.
	b = (ap-bp)/2.	
	

	if fabs(dydp)>1e-6 :	
		bt0 = atan2(-dxdp,dydp)
	else:
		bt0 = pi/2.


	if fabs(a-b)<1e-6 : 
		btp = 0
	elif fabs(h-b) >1e-6 :
		btp = atan( b/a * sqrt( fabs( (a**2 - h**2) / (h**2 - b**2) ) ) )

	else :
		btp = atan( b/a * sqrt( fabs( (k**2 - b**2) / (a**2 - k**2) ) ) )
		

	B = copysign(fabs(bt0)+btp,bt0)
	
	#print 'bt0 = %.8f , btp = %.8f , sign = %d' % (bt0,btp,copysign(1,bt0))	
	#print 'h= %.4f k= %.4f stp= %.4f ap= %.4f bp= %.4f btp= %.4f bt0= %.4f' % (h,k,stp,ap,bp,btp,bt0)
	
	return a,b,B



def GeodesicArc (lam1,phi1,lam2,phi2,pointsperdegree):
	"""Returns the geodesic arc in the sphere joining the point (lam1,phi1) and (lam2,phi2) with numpoints points. lam=lon, phi=lat """
	l1 = lam1 * pi/180 #computations in radians
	p1 = phi1 * pi/180
	l2 = lam2 * pi/180
	p2 = phi2 * pi/180
	L = l2-l1	# With this L we can suppose that A is on the 0 meridian.
	sL = sin(L)
	cL = cos(L)
	sp1 = sin(p1)
	cp1 = cos(p1)
	sp2 = sin(p2)
	cp2 = cos(p2)

	x = cL*cp1*cp2+sp1*sp2
	y = sL*cp2
	z = -cL*sp1*cp2+cp1*sp2

	Y = sqrt(y**2 + z**2)

	M = np.array([(cp1,0.0,sp1), (-z/Y*sp1,y/Y,z/Y*cp1), (-y/Y*sp1,-z/Y,y/Y*cp1)])
	# To obtain M, we compose two rotations of the sphere (3x3 matrices) so that the geodesic joining A and B lies on the equator.
	#print M

	d = acos(x)
	ddeg = d * 57.29577951308232087794
	#print "Distance(A,B) = %f"% ddeg

	numpoints = int(ddeg*pointsperdegree) # each point in the path is one minute of geodesic from the previous.
	print "Numpoints: ", numpoints
	geo0 = np.linspace(0,d,numpoints)
	geo0xyz = np.column_stack((np.cos(geo0),np.sin(geo0),np.zeros(numpoints)))
	#print geo0xyz

	geoxyzb = np.dot(geo0xyz,M)
	#print geoxyzb
	ll = np.arctan2(geoxyzb[:,1],geoxyzb[:,0])
	pp = np.arcsin(geoxyzb[:,2])
	geolpb = np.column_stack((ll,pp))
	geolp = geolpb + np.array([l1,0])
	geolpdeg = geolp * 57.29577951308232087794

	return ddeg , geolpdeg














