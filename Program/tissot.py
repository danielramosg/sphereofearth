
# -*- coding: utf-8 -*-

# Author: Daniel Ramos


import sys

from PyQt4 import QtCore, QtGui
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from math import *
from numpy import *




#R=6366197.
#R=100 * 742/3710.
R=100.
H=1e-5

HRES = 1280 #screen resolution (hor)
VRES = 1024 #screen resolution (ver)

def Tissot (x,y,p):
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

    def __init__(self, parent, image, pr, prtrick = None):
        super(QWidget, self).__init__(parent) #llamar al constructor de la superclase
        
	self.pr = pr
	if prtrick is None:
		self.prtiss = pr
	else:
		self.prtiss = prtrick

	w = image.width()
	h = image.height()
	#scalefactor = min( 1894.0/w, 912.0/h ) if (1034.0/h)*w > 1395.0 else 1034.0/h
	scalefactor = min( (HRES-26.)/w, (VRES-168.)/h ) if (1034.0/h)*w > 1395.0 else (VRES-130.)/h	
	rect = QRect(0,0,scalefactor*w,scalefactor*h)		
	#rect=QRect(0,0,parent.width(),parent.height())

	self.CX = rect.width()/2
	self.CY = rect.height()/2
	#self.SC = 30 # must be set manually when created
	self.SC = 0.5083483258 / scalefactor 
	#2*pi*R / (width of the pc proj in pixels) . This is the scale of the png images. Scale 1 for printed maps

	self.imageLayer = QLabel(self)
	self.imageLayer.setScaledContents(True)
	self.imageLayer.setPixmap(image)
        self.imageLayer.setGeometry(rect)
        self.ellipsesLayer = EllipsesLayer(self)
        self.ellipsesLayer.setGeometry(rect)
        self.mouseLayer = MouseLayer(self)
        self.mouseLayer.setGeometry(rect)
        self.mouseLayer.setMouseTracking(True)
        self.mouseLayer.setScaledContents(True)
        
	self.clearbutton = QPushButton(self)
	self.clearbutton.setText("Clear")
        self.clearbutton.setGeometry(QRect(HRES-150,VRES-130,90,27))
	self.connect(self.clearbutton, SIGNAL("clicked()"),self.ClearEllipses)

	self.coordlabel = QLabel(self)
	self.coordlabel.setGeometry(QRect(HRES-250,VRES-100,300,27))
	self.coordlabel.setText('Coordinates:')

	self.radiuslab = QLabel(self)
	self.radiuslab.setGeometry(QRect(HRES-250,VRES-130,25,27))
	self.radiuslab.setText('r=') 
	self.radiusbox = QDoubleSpinBox(self)
	self.radiusbox.setGeometry(QRect(HRES-225,VRES-130,65,27))
	self.radiusbox.setValue(20)
	self.connect(self.radiusbox, SIGNAL("valueChanged(double)"),self.ellipsesLayer.update)

	#self.exitbutton = QPushButton(self)
	#self.exitbutton.setText("Exit")
	#self.exitbutton.setGeometry(QRect(HRES-150,VRES-165,90,27))
	#self.connect(self.exitbutton, SIGNAL("clicked()"),self.exit)

    def ClearEllipses (self):
	self.ellipsesLayer.listellip = []
	self.ellipsesLayer.update()

    #def exit (self):
	#quit()



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
	
	coords = self.mytissot.pr( self.mytissot.SC * (self.lastX - self.mytissot.CX) , self.mytissot.SC * (- self.lastY + self.mytissot.CY), inverse=True )
	coordstxt = 'Coordinates: (%.2f , %.2f)' % coords
	self.mytissot.coordlabel.setText(coordstxt)

	self.b, self.a, self.S = Tissot( self.mytissot.SC * (self.lastX - self.mytissot.CX) , self.mytissot.SC * (- self.lastY + self.mytissot.CY) , self.mytissot.prtiss)
	
	
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
	
	self.update() #repintar

    def mousePressEvent(self, event):
	self.mytissot.ellipsesLayer.listellip.append( [self.point, self.a, self.b, self.S, self.pencolor, self.brushcolor] )
	self.mytissot.ellipsesLayer.update()
	#print "pressed", self.point, self.a, self.b, self.S

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
	
	r = self.mytissot.radiusbox.value()
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
	r = self.mytissot.radiusbox.value()
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
















