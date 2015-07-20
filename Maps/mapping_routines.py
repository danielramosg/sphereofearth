#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
from math import *
from pyproj import Proj
from time import time
import numpy as np
import matplotlib.pyplot as plt

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('../param.ini')

src_img = params.get('Source_Image','src_img')
R = params.getfloat('Maps_Size','radius_of_the_globe')
resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')



MM2PX=resol/25.4  # pixels/mm  # 1 inch = 25.4 mm
PX2MM=1./MM2PX

im=Image.open(src_img)
srcx, srcy= im.size
assert srcx == 2*srcy


def topo_map(p,width,height,mask,name):
	dimx=int(width*MM2PX) 
	dimy=int(height*MM2PX)
	print "Creating projection \"" + name + "\"..."
	print 'Earth radius: %d mm' % R
	print 'Size: %.2f x %.2f mm (%d x %d pixels at %d dpi)' % (width, height, dimx, dimy, resol)

	print "Loading source image..."
	orig=im.load()
	imfinale=Image.new('RGB',[dimx,dimy])
	resul=imfinale.load()

	(cx , cy) = (dimx/2 , dimy/2)
	(sx , sy) = (srcx/2 , srcy/2)
	k=float(srcy)/180.

	print "Transforming the image..."
	for i in range(dimx):
		for j in range(dimy):
			x, y = (i-cx)*PX2MM, (-j+cy)*PX2MM			
			if mask([x,y]):
				z=p(x,y,inverse=True)
				x0 , y0 = sx+k*z[0] , sy-k*z[1]
				try: resul[i,j]=orig[x0 % srcx , y0 % srcy]	
				except: resul[i,j]=(255,0,0)	
			else:
				resul[i,j]=(255,255,255)
	
	imfinale.save(name + '_0.png')



def standard_graticule(S=4):
	print "Creating standard graticule..."
	grat = np.empty((0,2))

	#meridians
	for i in range(-180,181,10):
		x = np.full(180*S,i,dtype=float)
		y = np.linspace(-90,90,180*S)
		grat = np.vstack((grat, np.column_stack((x,y))))
		grat = np.append(grat, [[np.nan,np.nan]] , axis=0)

	#parallels
	for j in range(-90,91,10):
		x = np.linspace(-180,180,360*S)
		y = np.full(360*S,j,dtype=float)
		grat = np.vstack((grat, np.column_stack((x,y))))
		grat = np.append(grat, [[np.nan,np.nan]],axis=0)

	return grat

def project_graticule(p,grat,mask):
	print "Projecting graticule..."
	#gratpj = p(grat)
	gratpj = np.column_stack( p(grat[:,0], grat[:,1]) )
	gratpj[gratpj>1e29]=np.nan
	msk = np.apply_along_axis(mask,1,gratpj)

	gratpj[~msk,:] = np.nan

	gratpj = gratpj*MM2PX

	#np.savetxt('outgratpj.dat',gratpj)
	return gratpj


def merge_map_grat(name,gratpj):
	print "Merging map with graticule..."
	im = plt.imread(name + '_0.png')
	dimy, dimx = im.shape[0], im.shape[1]

	w, h = float(dimx)/resol, float(dimy)/resol
	fig = plt.figure(figsize=[w,h], frameon=False)

	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.axis('off')
	ax.get_xaxis().set_visible(False)
	ax.get_yaxis().set_visible(False)
	fig.add_axes(ax)

	VV=[-dimx/2,dimx/2.,-dimy/2.,dimy/2.]

	ax.imshow(im, extent=VV, aspect='auto')

	plt.plot(gratpj[:,0], gratpj[:,1],color='0.60',linewidth=0.5)
	plt.axis(v=VV)
	plt.axis('tight')

	plt.savefig(name + '.png',dpi=resol, bbox_inches='tight', pad_inches=0)
	#plt.savefig(name + '.pdf',dpi=resol, bbox_inches='tight', pad_inches=0)


