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

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from math import *
from numpy import *


#R=6366197.
#R=100 * 742/3710.
#R=100.
H=1e-5

#HRES = 1280 #screen resolution (hor)
#VRES = 1024 #screen resolution (ver)

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




class MyTissot(QWidget):

    def __init__(self, parent, cnx, PJ, resol, prtrick = None): #image,R, pr,
        super(QWidget, self).__init__(parent) #llamar al constructor de la superclase
        
	self.resol = resol
	self.PJ = PJ
	self.cnx = cnx # object to connect i/o	

	if prtrick is None:
		self.prtiss = PJ.p
	else:
		self.prtiss = prtrick
	
	image = QPixmap('./img/' + PJ.name + '.png')

	self.imw = image.width()
	self.imh = image.height()

	self.imageLayer = QLabel(self)
	self.ellipsesLayer = EllipsesLayer(self)
	self.mouseLayer = MouseLayer(self)

	self.imageLayer.setScaledContents(True)
	self.imageLayer.setPixmap(image)
        self.mouseLayer.setMouseTracking(True)
        self.mouseLayer.setScaledContents(True)

	self.resizeEvent(self)
        
	self.connect(self.cnx.clearbutton, SIGNAL("clicked()"),self.ClearEllipses)
	self.connect(self.cnx.radiusbox, SIGNAL("valueChanged(double)"),self.ellipsesLayer.update)

	

#	self.exitbutton = QPushButton(self)
#	self.exitbutton.setText("Exit")
#	self.exitbutton.setGeometry(QRect(HRES-150,VRES-165,90,27))
#	self.connect(self.exitbutton, SIGNAL("clicked()"),self.exit)

	
    def ClearEllipses (self):
	self.ellipsesLayer.listellip = []
	self.ellipsesLayer.update()

    def resizeEvent(self,event):
	HRES = self.width()	
	VRES = self.height() 

	imPX_2_scrPX = min(float(HRES)/self.imw , float(VRES)/self.imh)	 #image pixels to screen pixels
	
	rect = QRect(0,0,self.imw*imPX_2_scrPX , self.imh*imPX_2_scrPX)	
	scrPX_2_imPX = 1/imPX_2_scrPX

	self.CX = rect.width()/2	#center of the rectangle
	self.CY = rect.height()/2

	imPX_2_mapMM = 1/self.resol * 25.4 		#image pixels to map milimeters
	self.SC = scrPX_2_imPX * imPX_2_mapMM	#screen pixels to map milimeters

        self.imageLayer.setGeometry(rect)
        self.ellipsesLayer.setGeometry(rect)
	self.mouseLayer.setGeometry(rect)

#    def exit (self):
#	quit()



class MouseLayer(QLabel): # Clase de la imagen con interaccion de raton #subclase de QLabel

    def __init__(self, parent):
        super(MouseLayer, self).__init__(parent) #llamar al constructor de la superclase
        self.mytissot = parent #guardar referencia a la instancia de MyTissot
        self.lastX = 0
        self.lastY = 0
	self.point = QPoint(0,0)
	self.a = 0
	self.b = 0
	self.S = 0
	self.pencolor = Qt.red
	self.brushcolor = QColor(255,0,0,50)

    #método sobreescrito llamado cuando hay eventos mouseMove
    def mouseMoveEvent(self, event):
        self.lastX= event.x()
        self.lastY = event.y()
	self.point = QPoint(event.x(),event.y())
	
	Map_loc = [self.mytissot.SC * (self.lastX - self.mytissot.CX) , self.mytissot.SC * (- self.lastY + self.mytissot.CY)]
	mask=self.mytissot.PJ.mask

	if mask(Map_loc):
		coords = self.mytissot.PJ.p( Map_loc[0],Map_loc[1], inverse=True )
		coordstxt = '(%.2f , %.2f)' % coords
		self.mytissot.cnx.coordlabel.setText(coordstxt)

		self.b, self.a, self.S = Tissot( Map_loc[0], Map_loc[1] , self.mytissot.prtiss,self.mytissot.PJ.R)
	
		if fabs(self.a - self.b) < 1e-2 :
			self.pencolor = Qt.green
		else:
			self.pencolor = Qt.red

		if fabs(self.a * self.b - 1.) <1e-2 :
			self.brushcolor = QColor(0,255,0,50)
		else:
			self.brushcolor = QColor(255,0,0,50)

		#r = self.mytissot.radiusbox.value()
		#self.a = r * self.a	
		#self.b = r * self.b
		self.S = -57.29577950 * self.S
	
	else:
#		self.lastX = 0
#		self.lastY = 0
#		self.point = QPoint(0,0)
		self.a = 0
		self.b = 0
#		self.S = 0

	self.update() #repintar


    def mousePressEvent(self, event):
	self.mytissot.ellipsesLayer.listellip.append( [self.point, self.a, self.b, self.S, self.pencolor, self.brushcolor] )
	self.mytissot.ellipsesLayer.update()
	#print "pressed", self.point, self.a, self.b, self.S
	#print self.geometry()

    #método sobreescrito llamado cuando hay evento paint, e.g. al llamar update() o repaint() 
    #siempre hay que pintar con el painter dentro de paintEvent()
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self) #pintar en este objeto MyQLabel
        painter.setPen(self.pencolor) #trazo
        painter.setBrush(self.brushcolor) #relleno
	painter.setRenderHint(QPainter.Antialiasing,True)

	painter.translate(self.point) # cambio de coord
	painter.rotate(self.S) # rotación resp el nuevo origen
	
	r = self.mytissot.cnx.radiusbox.value()
#	r=20
        painter.drawEllipse(QPointF(0,0), r*self.a , r*self.b )
        painter.end()
        super(MouseLayer, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	


class EllipsesLayer(QLabel): # Clase de la imagen con las elipses clicadas  #subclase de QLabel

    def __init__(self, window):
        super(EllipsesLayer, self).__init__(window) 
        self.mytissot = window 
	self.listellip = []   # list of ellipses to be drawn, in format [Qpoint, a, b, S, color]

    def paintEvent(self, event): 
	painter = QPainter()
	r = self.mytissot.cnx.radiusbox.value()
#	r=20
	for Ellip in self.listellip:
		painter.begin(self)
		painter.setPen(Ellip[4]) 
		painter.setBrush(Ellip[5])
		painter.setRenderHint(QPainter.Antialiasing,True)
		painter.translate( Ellip[0] ) # cambio de coord
		painter.rotate( Ellip[3] ) # rotación resp el nuevo origen
		painter.drawEllipse( QPointF(0,0), r*Ellip[1] , r*Ellip[2])
		painter.end()

        super(EllipsesLayer, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	#print 'EllipsesLayer actualizada'
















