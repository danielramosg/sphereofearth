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

from soemath import *
import numpy as np

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
	self.geodesiclayer = GeodesicLayer(self)


	self.imageLayer.setScaledContents(True)
	self.imageLayer.setPixmap(image)
        self.mouseLayer.setMouseTracking(True)
        self.mouseLayer.setScaledContents(True)

	self.resizeEvent(self)
        
	self.connect(self.cnx.clearbutton, SIGNAL("clicked()"),self.ClearEllipses)
	self.connect(self.cnx.radiusbox, SIGNAL("valueChanged(double)"),self.ellipsesLayer.update)

	self.geodesiclayer.update()
	

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
	
	rectW = self.imw*imPX_2_scrPX
	rectH = self.imh*imPX_2_scrPX

	rect = QRect(HRES/2-rectW/2,VRES/2-rectH/2,rectW,rectH)	
	#rect = QRect(0,0,self.imw*imPX_2_scrPX , self.imh*imPX_2_scrPX)	
	scrPX_2_imPX = 1/imPX_2_scrPX

	self.CX = rect.width()/2	#center of the rectangle
	self.CY = rect.height()/2

	imPX_2_mapMM = 1/self.resol * 25.4 		#image pixels to map milimeters
	self.SC = scrPX_2_imPX * imPX_2_mapMM	#screen pixels to map milimeters

        self.imageLayer.setGeometry(rect)
        self.ellipsesLayer.setGeometry(rect)
	self.mouseLayer.setGeometry(rect)
	self.geodesiclayer.setGeometry(rect)
	self.mouseLayer.raise_()
	self.ClearEllipses()
	
    def Map_2_Screen(self,ptMap):
	aa = np.array(ptMap)
	return ( (aa / self.SC) - np.array([-self.CX,self.CY]) ) * np.array([1,-1])

    def Screen_2_Map(self,ptScreen):
	bb = np.array(ptScreen)
	return self.SC * ( bb * np.array([1,-1]) + np.array([-self.CX,self.CY]) ) 
	

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

	Map_loc = self.mytissot.Screen_2_Map([self.lastX, self.lastY])

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


class GeodesicLayer(QLabel): # Class containing the geodesic path 

    def __init__(self, window):
        super(GeodesicLayer, self).__init__(window) 
        self.mytissot = window 
	self.pointA = (0,0) #already in lon, lat
	self.pointB = (50,70) #this is a test.

    def paintEvent(self, event): 
	painter = QPainter()
	
	n=100
	
	geo = GeodesicArc(self.pointA[0],self.pointA[1],self.pointB[0],self.pointB[1],n)
	#print geo
	geo_map = np.array(self.mytissot.PJ.p(geo[:,0],geo[:,1])).transpose()
	geo_scr = self.mytissot.Map_2_Screen(geo_map)

	qpoints = QPolygonF()
	for p in geo_scr:
		qpoints.append(QPointF(*p))

	painter.begin(self)
	painter.setPen(QPen(QColor(Qt.yellow), 2))
	painter.setRenderHint(QPainter.Antialiasing,True)
	painter.drawPolyline(qpoints)
	painter.end()

        super(GeodesicLayer, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	#print 'GeodesicLayer actualizada'
















