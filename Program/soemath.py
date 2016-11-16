# -*- coding: utf-8 -*-

# The Sphere of the Earth.
# Copyright (C) 2013 - 2016  Daniel Ramos
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

def Tissot (x,y,PJ):
	p=PJ.p
	R=PJ.R	
	# lon, lat coordinates of the point
	try:
		(lam, phi) = p(x,y,inverse=True, radians=True, errcheck=True)
	except:
		return None,None,None

#	print 'coords: ', lam, phi

	# partial derivatives
	(x0,y0) = p(lam - H/2. , phi , radians=True)
	(x1,y1) = p(lam + H/2. , phi , radians=True)
	dxdl = (x1 - x0)/H
	dydl = (y1 - y0)/H
	(x0,y0) = p(lam , phi - H/2. , radians=True) 
	(x1,y1) = p(lam , phi + H/2. , radians=True)
	dxdp = (x1 - x0)/H
	dydp = (y1 - y0)/H	
#	print 'dxdp= %.4f dydp= %.4f dxdl= %.4f dydl= %.4f ' % (dxdp, dydp, dxdl, dydl)

#	# parameters for the ellipse. Synthetic geometry algorithm, see Snyder "Map projections: A working manual".
#	h = 1/R * sqrt(fabs( dxdp**2 + dydp**2 )) 
#	k = 1/(R*cos(phi)) * sqrt(fabs( dxdl**2 + dydl**2 ))
#	stp = 1/(R**2*h*k*cos(phi)) * (dydp*dxdl - dxdp*dydl)
#	ap = sqrt(fabs(h**2 + k**2 + 2.*h*k*stp))
#	bp = sqrt(fabs(h**2 + k**2 - 2.*h*k*stp))
#	a = (ap+bp)/2.
#	b = (ap-bp)/2.	
#	
#	#print "a=%.4f b=%.4f" %(a,b)

#	if fabs(dydp)>1e-6 :	
#		bt0 = atan2(-dxdp,dydp)
#	else:
#		bt0 = pi/2.

#	if fabs(a-b)<1e-6 : 
#		btp = 0
#	elif fabs(h-b) >1e-6 :
#		btp = atan( b/a * sqrt( fabs( (a**2 - h**2) / (h**2 - b**2) ) ) )
#	elif fabs(a-k) >1e-6 :
#		btp = atan( b/a * sqrt( fabs( (k**2 - b**2) / (a**2 - k**2) ) ) )
#	else:
#		btp =pi/2.		

#	B = copysign(fabs(bt0)+btp,bt0)

#	B = -57.29577950 * B
#	print "B ", B

	#print 'bt0 = %.8f , btp = %.8f , sign = %d' % (bt0,btp,copysign(1,bt0))	
	#print 'h= %.4f k= %.4f stp= %.4f ap= %.4f bp= %.4f btp= %.4f bt0= %.4f' % (h,k,stp,ap,bp,btp,bt0)


	# parameters for the ellipse. Linear algebra approach.
	A = np.array([ [1/(R*cos(phi)) * dxdl , 1/R * dxdp] , [1/(R*cos(phi)) * dydl , 1/R * dydp] ])
	M = np.linalg.inv(np.dot(A,A.transpose()))
	vps = np.linalg.eig(M)
	sax0 = 1/sqrt(vps[0][0])
	sax1 = 1/sqrt(vps[0][1])
	ang = 57.29577950 * atan2(vps[1][0,1],vps[1][0,0])

#	print "A = ", A
#	print "M = ", M
#	print "vaps = ", vps[0]
#	print "veps = ", vps[1]
#	print "saxis = ", sax0, sax1 
#	print "angle = ", ang
	
#	return a,b,B
	return sax0, sax1, ang


def GeodesicArc (lam1,phi1,lam2,phi2,pointsperdegree,complete):
	"""Returns the geodesic arc in the sphere joining the point (lam1,phi1) and (lam2,phi2). lam=lon, phi=lat """
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

	if complete:
		d = 6.2831853071795864770

	ddeg = d * 57.29577951308232087794
	#print "Distance(A,B) = %f"% ddeg	

	numpoints = int(ddeg*pointsperdegree) # each point in the path is one minute of geodesic from the previous.
	#print "Numpoints: ", numpoints
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



def LoxodromeArc (lam1,phi1,lam2,phi2,pointsdensity,complete):
	"""Returns the loxodrome arc in the sphere joining the point (lam1,phi1) and (lam2,phi2). lam=lon, phi=lat """

	p=Proj(proj='merc', ellps='sphere', a=100, b=100)

	x1,y1 = p(lam1,phi1)
	x2,y2 = p(lam2,phi2)

	azimuth = atan2(x2-x1,y2-y1) * 57.29577951308232087794 % 360

	d = fabs(x2-x1) + fabs(y2-y1)
	numpoints = int(d*pointsdensity) 
#	print "Numpoints lox: ", numpoints

	if not complete:
		t = np.linspace(0,1,numpoints)
	else:
		t = np.linspace(-10,10,10*numpoints)	
	
	lox0 = np.column_stack(( x1+t*(x2-x1)  , y1 + t* (y2-y1) ))
	
	lox = np.array(p(lox0[:,0],lox0[:,1],inverse=True)).transpose()

	#print "Azimuth: ", azimuth
	return azimuth, lox











