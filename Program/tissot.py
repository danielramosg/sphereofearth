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




# Here we implement the class SoeMap, which is the main widget that contains each map projection.
# SoeMap contains several layers:
# - imageLayer
# - tissotLayer_fg
# - tissotLayer_bg
# - geodesicLayer
# - loxodromeLayer


import sys, os

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from soemath import *
import numpy as np

class SoeMap(QWidget):

    def __init__(self, parent, cnx, PJ, resol): #image,R, pr,
        super(QWidget, self).__init__(parent) #llamar al constructor de la superclase
	self.parent = parent
	self.resol = resol
	self.PJ = PJ
	self.cnx = cnx # object to connect i/o	
	
	# determine if application is a script file or frozen exe
	if getattr(sys, 'frozen', False):     # "bundled" on a executable
		application_path = os.path.dirname(sys.executable)
	elif __file__:     # "live" script, running using an interpreter
		application_path = os.path.dirname(__file__)

	imgfilename = os.path.join(application_path,'img',PJ.name + '.png')

	if not os.path.isfile(imgfilename):
		print "Image for %s projection not found. Creating..." % PJ.name
		import mapping_routines as mr
		grat = mr.standard_graticule()
		mr.topo_map(PJ)
		gratpj = mr.project_graticule(PJ,grat)
		mr.merge_map_grat(PJ,gratpj)
		image = QPixmap(imgfilename)
		print "Done."

	image = QPixmap(imgfilename)

	self.imw = image.width()
	self.imh = image.height()

	self.setMinimumSize(30,30)

	self.imageLayer = QLabel(self)
	self.tissotLayer_bg = TissotLayer_bg(self)
	self.tissotLayer_fg = TissotLayer_fg(self)
	self.geodesicLayer = GeodesicLayer(self)
	self.loxodromeLayer = LoxodromeLayer(self)

	self.coords = None, None

	self.tissotLayer_fg.raise_()

	self.imageLayer.setScaledContents(True)
	self.imageLayer.setPixmap(image)
	
	self.resizeEvent(self)
        
	self.connect(self.cnx.tissot_clear, SIGNAL("clicked()"),self.tissotLayer_bg.Clear)
	self.connect(self.cnx.radiusbox, SIGNAL("valueChanged(double)"),self.tissotLayer_bg.update)
	self.connect(self.cnx.geod_clear, SIGNAL("clicked()"),self.geodesicLayer.Clear)
	self.connect(self.cnx.loxo_clear, SIGNAL("clicked()"),self.loxodromeLayer.Clear)
	self.connect(self.cnx.unitbox, SIGNAL("valueChanged(double)"),self.geodesicLayer.update)
	self.connect(self.cnx.geod_extend, SIGNAL("toggled(bool)"),self.geodesicLayer.update)
	self.connect(self.cnx.loxo_extend, SIGNAL("toggled(bool)"),self.loxodromeLayer.update)
	
	self.connect(self.cnx.geod_select, SIGNAL("clicked()"),self.geodesicLayer.raise_)
	self.connect(self.cnx.loxo_select, SIGNAL("clicked()"),self.loxodromeLayer.raise_)		
	self.connect(self.cnx.tissot_select, SIGNAL("clicked()"),self.tissotLayer_fg.raise_)

	#self.geodesicLayer.update()
	#self.loxodromeLayer.update()

#	self.exitbutton = QPushButton(self)
#	self.exitbutton.setText("Exit")
#	self.exitbutton.setGeometry(QRect(HRES-150,VRES-165,90,27))
#	self.connect(self.exitbutton, SIGNAL("clicked()"),self.exit)

	
    
    def resizeEvent(self,event):
	HRES = self.width()	
	VRES = self.height() 

	try:
		imPX_2_scrPX = min(float(HRES)/self.imw , float(VRES)/self.imh)	 #image pixels to screen pixels
	except:
		imPX_2_scrPX = 1
		print "Warning: imPX_2_scrPX raised an exception (division by zero)"
		
	rectW = self.imw*imPX_2_scrPX
	rectH = self.imh*imPX_2_scrPX

	rect = QRect(HRES/2-rectW/2,VRES/2-rectH/2,rectW,rectH)	

	scrPX_2_imPX = 1/imPX_2_scrPX

	self.CX = rect.width()/2	#center of the rectangle
	self.CY = rect.height()/2

	imPX_2_mapMM = 1/self.resol * 25.4 		#image pixels to map milimeters
	self.SC = scrPX_2_imPX * imPX_2_mapMM	#screen pixels to map milimeters

        self.imageLayer.setGeometry(rect)
        self.tissotLayer_bg.setGeometry(rect)
        self.tissotLayer_fg.setGeometry(rect)
	self.geodesicLayer.setGeometry(rect)
	self.loxodromeLayer.setGeometry(rect)

    def Map_2_Screen(self,ptMap):
	aa = np.array(ptMap)
	return ( (aa / self.SC) - np.array([-self.CX,self.CY]) ) * np.array([1,-1])

    def Screen_2_Map(self,ptScreen):
	bb = np.array(ptScreen)
	return self.SC * ( bb * np.array([1,-1]) + np.array([-self.CX,self.CY]) ) 

    def UpdateCoords(self,cursor):
	Map_loc = self.Screen_2_Map([cursor.x(), cursor.y()])

	if self.PJ.mask(Map_loc):
		coords = self.PJ.p( Map_loc[0],Map_loc[1], inverse=True )

		if coords[0] >= 0.:
			lsign = 'E'
		else:
			lsign = 'W'
		if coords[1] >= 0. :
			psign = 'N'
		else:
			psign = 'S'

		coordstxt = u"%.2f\u00B0 %s   %.2f\u00B0 %s" % (fabs(coords[1]), psign, fabs(coords[0]), lsign)
		self.cnx.coordlabel.setText(coordstxt)

		self.coords = coords
	else:
		self.coords = None,None

	

#    def exit (self):
#	quit()





def TissotEllipse(lon, lat, Map):
	"""Given longitude and latitude of a point on a given SoeMap, return the parameters of the Tissot ellipse"""

	if lon == None or lat == None:
		return None,None,None,None,None,None

	xy = Map.PJ.p(lon,lat)
	r = Map.cnx.radiusbox.value()
	f = r * Map.PJ.R / 6371 * 1/Map.SC # r realKM * R mapMM / EarthRadiusinKM * 1/scrPX_2_mapMM

	if Map.PJ.mask(xy):
		a,b,S = Tissot(xy[0],xy[1],Map.PJ)
		
		if fabs(a - b) < 1e-2 :
			pencolor = QPen(Qt.green,1.2)
		else:
			pencolor = QPen(Qt.red,1.2)

		if fabs(a * b - 1.) <1e-2 :
			brushcolor = QColor(0,255,0,50)
		else:
			brushcolor = QColor(255,0,0,50)
		
		a = f * a
		b = f * b

	else:
		xy,a,b,S,pencolor,brushcolor = None,None,None,None,None,None

	return xy,a,b,S,pencolor,brushcolor



class TissotLayer_fg(QWidget): # This class contains the mouse interaction of TissotLayer 

    def __init__(self, parent):
        super(TissotLayer_fg, self).__init__(parent) #llamar al constructor de la superclase
	self.thismap = parent

	self.setCursor(Qt.CrossCursor)
	self.setMouseTracking(True)
 	self.point = QPoint(0,0)
	self.a = 0
	self.b = 0
	self.S = 0
	self.pencolor = Qt.red
	self.brushcolor = QColor(255,0,0,50)


    def mouseMoveEvent(self, event):	#overwritten method, it is called whenever there are mouseMove events
        self.point = QPoint(event.x(),event.y())

	self.thismap.UpdateCoords(event)
	self.coords = self.thismap.coords

	foo, self.a, self.b, self.S, self.pencolor, self.brushcolor = TissotEllipse( self.coords[0], self.coords[1] , self.thismap)

	self.update() #repintar


    def mousePressEvent(self, event):
	if self.a == None or self.b == None:
		return None

	self.thismap.parent.listellip.append( self.coords )
	self.thismap.tissotLayer_bg.update()
	
    		
    def paintEvent(self, event):
					#método sobreescrito llamado cuando hay evento paint, e.g. al llamar update() o repaint() 
    					#siempre hay que pintar con el painter dentro de paintEvent()

	if not self.underMouse():
		return None
	if self.a == None or self.b == None:
		return None

        painter = QPainter()	
        painter.begin(self) #pintar en este objeto MyQLabel
	painter.setRenderHint(QPainter.Antialiasing,True)
        painter.setPen(self.pencolor) #trazo
        painter.setBrush(self.brushcolor) #relleno
	painter.translate(self.point) # cambio de coord
	painter.rotate(self.S) # rotación resp el nuevo origen
	
        painter.drawEllipse(QPointF(0,0), self.a , self.b )
        painter.end()
        super(TissotLayer_fg, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	
    def leaveEvent(self,event):
	self.update()


class TissotLayer_bg(QWidget): # This class contains the images with clicked ellipses

    def __init__(self, parent):
        super(TissotLayer_bg, self).__init__(parent) 
        self.thismap = parent

    def Clear (self):
	self.thismap.parent.listellip = []
	self.update()

    def paintEvent(self, event): 
	painter = QPainter()
	for coor in self.thismap.parent.listellip:
		xy,a,b,S,pen,brush = TissotEllipse( coor[0], coor[1] , self.thismap)
		if xy == None:
			pass
		else:
			pt = self.thismap.Map_2_Screen(xy)
			point = QPoint(pt[0],pt[1])
		
			painter.begin(self)
			painter.setRenderHint(QPainter.Antialiasing,True)
			painter.setPen(pen) 
			painter.setBrush(brush)
			painter.translate( point ) # cambio de coord
			painter.rotate( S ) # rotación resp el nuevo origen
			painter.drawEllipse( QPointF(0,0), a , b )
			painter.end()

        super(TissotLayer_bg, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	# print 'TissotLayer_bg actualizada'


class GeodesicLayer(QWidget): # Class containing the geodesic path 

    def __init__(self, window):
        super(GeodesicLayer, self).__init__(window) 
        self.thismap = window 

	self.setCursor(Qt.CrossCursor)
	self.setMouseTracking(True)
	#self.pointA = None #points in lon, lat
	#self.pointB = None
	self.flip = 0

    def mouseMoveEvent(self,event):
	self.thismap.UpdateCoords(event)

    def Clear(self):
	self.thismap.parent.geoptA = None
	self.thismap.parent.geoptB = None
	self.thismap.cnx.distlabel.setText('')
	self.update()

    def mousePressEvent(self,event):
	pt_scr = [event.x(),event.y()]
	pt_map = self.thismap.Screen_2_Map(pt_scr)
	pt_geo = self.thismap.PJ.p(pt_map[0],pt_map[1],inverse=True)
	
	if self.flip == 0:
		self.thismap.parent.geoptA = pt_geo
		#self.thismap.parent.geoptB = None
	else:
		self.thismap.parent.geoptB = pt_geo
		self.update()
	self.flip = self.flip +1
	self.flip = self.flip % 2
	
    def paintEvent(self, event):
	painter = QPainter()

#	for point in (self.thismap.parent.geoptA , self.thismap.parent.geoptB):
#		if point != None:
#			point_map = self.thismap.PJ.p(point[0],point[1])
#			point_scr = self.thismap.Map_2_Screen(point_map)
#			painter.begin(self)
#			painter.setRenderHint(QPainter.Antialiasing,True)
#			painter.setPen(QPen(QColor(Qt.red), 4))
#			painter.drawPoint(QPointF(point_scr[0],point_scr[1]))
#			painter.end()

	if self.thismap.parent.geoptA == None or self.thismap.parent.geoptB == None :
		return None

	
	ppdeg = 2 # points per deg
	ext = self.thismap.cnx.geod_extend.isChecked()

	d , geo = GeodesicArc(self.thismap.parent.geoptA[0],self.thismap.parent.geoptA[1],self.thismap.parent.geoptB[0],self.thismap.parent.geoptB[1],ppdeg, complete=ext)
	#print geo
	#print d

	dist = d * 20000 / 180. # 20000 km = 180 deg. 
	disttxt = '%s  km' % '{:,}'.format(int(dist)).replace(',',' ')
	self.thismap.cnx.distlabel.setText(disttxt)	
	#print "Distance: %d km"% dist
	
	unit = self.thismap.cnx.unitbox.value()
	cpts = int (unit * 0.009 * ppdeg) #numper of points in the path per Unit of the geodesic ruler, 0.009 = 180/20000

	#print "cpts: ",cpts
	geo_map = np.array(self.thismap.PJ.p(geo[:,0],geo[:,1])).transpose()
	geo_scr = self.thismap.Map_2_Screen(geo_map)

	

	numpoints = len(geo_scr) #int(d*ppdeg)
	#print "numpoints: ", numpoints
	
	path = [QPainterPath(), QPainterPath()]

#	print geo_scr.shape
#	print geo_scr[numpoints-1]

	path[0].moveTo(QPointF(*geo_scr[0]))
	for i in range(numpoints) :
		qp = QPointF(*geo_scr[i])
		c = (i // cpts) % 2

		if ((path[c].currentPosition() - qp).manhattanLength() > 20) : # if there is a jump in the projection 
			path[c].moveTo(qp)  
			path[(c+1)%2].moveTo(qp)
		else:
			path[c].lineTo(qp)
			path[(c+1)%2].moveTo(qp)

	painter.begin(self)
	painter.setRenderHint(QPainter.Antialiasing,True)
	painter.setPen(QPen(QColor(Qt.yellow), 3))
	painter.drawPath(path[0])
	painter.drawPath(path[1])
	painter.setPen(QPen(QColor(Qt.white), 2))
	painter.drawPath(path[0])
	painter.setPen(QPen(QColor(Qt.black), 2))
	painter.drawPath(path[1])
	painter.end()

        super(GeodesicLayer, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	#print 'GeodesicLayer actualizada'



class LoxodromeLayer(QWidget): # Class containing the geodesic path 

    def __init__(self, window):
        super(LoxodromeLayer, self).__init__(window) 
        self.thismap = window 

	self.setCursor(Qt.CrossCursor)
	self.setMouseTracking(True)
	#self.pointA = None #points in lon, lat
	#self.pointB = None
	self.flip = 0

    def mouseMoveEvent(self,event):
	self.thismap.UpdateCoords(event)

    def Clear(self):
	self.thismap.parent.loxptA = None
	self.thismap.parent.loxptB = None
	self.thismap.cnx.azimlabel.setText('')
	self.update()

    def mousePressEvent(self,event):
	pt_scr = [event.x(),event.y()]
	pt_map = self.thismap.Screen_2_Map(pt_scr)
	pt_geo = self.thismap.PJ.p(pt_map[0],pt_map[1],inverse=True)
	
	if self.flip == 0:
		self.thismap.parent.loxptA = pt_geo
		#self.thismap.parent.loxptB = None
	else:
		self.thismap.parent.loxptB = pt_geo
		self.update()
	self.flip = self.flip +1
	self.flip = self.flip % 2
	
    def paintEvent(self, event):
	painter = QPainter()

	if self.thismap.parent.loxptA == None or self.thismap.parent.loxptB == None :
		return None
	
	ppdeg = 2 # points per deg
	ext = self.thismap.cnx.loxo_extend.isChecked()

	az, lox = LoxodromeArc(self.thismap.parent.loxptA[0],self.thismap.parent.loxptA[1],self.thismap.parent.loxptB[0],self.thismap.parent.loxptB[1],ppdeg, complete=ext)

	aztxt = u"%.2f\u00B0" % az
	self.thismap.cnx.azimlabel.setText(aztxt)

	lox_map = np.array(self.thismap.PJ.p(lox[:,0],lox[:,1])).transpose()
	lox_scr = self.thismap.Map_2_Screen(lox_map)
	
	numpoints = len(lox_scr) #int(d*ppdeg)
#	print "numpoints: ", numpoints
	
	path = QPainterPath()
	path.moveTo(QPointF(*lox_scr[0]))
	for p in lox_scr[1:] :
		qp = QPointF(*p)
		if (path.currentPosition() - qp).manhattanLength() < 50 : 
			path.lineTo(qp)
		else:
			path.moveTo(qp)  # if there is a jump in the projection 

	painter.begin(self)
	painter.setRenderHint(QPainter.Antialiasing,True)
	painter.setPen(QPen(QColor(Qt.cyan), 1.5))
	painter.drawPath(path)
	painter.end()

        super(LoxodromeLayer, self).paintEvent(event) #llamar al paintEvent() de la superclase, necesario
	#print 'LoxodromeLayer actualizada'













