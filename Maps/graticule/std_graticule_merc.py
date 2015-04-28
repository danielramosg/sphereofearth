#!/usr/bin/env python

#meridians
for i in range(-180,181,10):
	print 'nan nan'
	for j in range(-82,83):
		print '%f %f' % (i,j)
#parallels
for j in range(-80,82,10):
	print 'nan nan'
	for i in range(-180,181):
		print '%f %f' % (i,j)

print 'nan nan'

# python grat.py > grat.dat
