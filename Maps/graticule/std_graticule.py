#!/usr/bin/env python

#Creates a standard (cartesian) graticule of meridians and parallels.
#The spacing is 10 deg x 10 deg.
#The parameter S is the number of subdivisions of each segment (a segment joins two adjacent intersections between meridians and parallels).

#Example usage: 
#python grat.py > grat.dat

import sys
from numpy import linspace

S=int(sys.argv[1])

#meridians
for i in range(-180,181,10):
	print 'nan nan'
	for j in linspace(-90,90,180*S):
		print '%f %f' % (i,j)
#parallels
for j in range(-90,91,10):
	print 'nan nan'
	for i in linspace(-180,180,360*S):
		print '%f %f' % (i,j)

print 'nan nan'


