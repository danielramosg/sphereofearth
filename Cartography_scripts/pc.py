#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
from pyproj import Proj
from time import time


R = 100 # Radio de la Tierra (globo terráqueo) en mm

p=Proj(proj='eqc', ellps='sphere', a=R, b=R)

im=Image.open('ori_8192_mar.tif')

srcx, srcy= im.size
assert srcx == 2*srcy


resol=150. #resolucion, dpi #150
ancho=2*p(180,0)[0]  #anchura de la imagen, mm
alto=2*p(0,90)[1]  #altura de la imagen, mm 

MM2PX=resol/25.4  # pixels/mm  # 1 inch = 25.4 mm
PX2MM=1./MM2PX

dimx=int(ancho*MM2PX) 
dimy=int(alto*MM2PX)

print 'Size: %.2f x %.2f mm (%d x %d pixels at %d dpi)' % (ancho, alto, dimx, dimy, resol)

print "Loading 'plate carree' data..."
orig=im.load()
imfinale=Image.new('RGB',[dimx,dimy])
resul=imfinale.load()

(cx , cy) = (dimx/2 , dimy/2)
(sx , sy) = (srcx/2 , srcy/2)
k=float(srcy)/180.

print "Transforming the image..."

start=time()
for i in range(dimx):
	for j in range(dimy):
		try:
			z=p((i-cx)*PX2MM,(-j+cy)*PX2MM,inverse=True)
			(x0 , y0) = (sx+k*z[0] , sy-k*z[1])		
			resul[i,j]=orig[x0,y0]		
		except:
			resul[i,j]=(255,0,0)

imfinale.save('eqc.pdf', 'PDF', resolution=resol)


print "Done. Elapsed time: %.2f sec" % (time()-start)






