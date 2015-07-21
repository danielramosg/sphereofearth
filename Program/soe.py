
# -*- coding: utf-8 -*-

# Author: Daniel Ramos



from PyQt4 import QtCore, QtGui
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui_soe import *

from pyproj import Proj

from projections_multiscale import *
from tissot import *    

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('param.ini')

R = params.getfloat('Maps_Size','radius_of_the_globe')
resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')


class Mywidget (QWidget):

    def __init__(self):
        QWidget.__init__(self)

	#QApplication.setOverrideCursor(QCursor(Qt.BlankCursor)) #No cursor. Use for touchscreens.

	self.ui=Ui_Form()
	self.ui.setupUi(self)

	dw = QDesktopWidget()

	self.tabsize = QRect(0, 0, dw.availableGeometry().width(), dw.availableGeometry().height())	
	#self.tabsize = QRect(0, 0, 400, 400)

	self.ui.tab_pc.setGeometry(self.tabsize)
	self.ui.tab_merc.setGeometry(self.tabsize)
	self.ui.tab_peters.setGeometry(self.tabsize)
	self.ui.tab_aziequi.setGeometry(self.tabsize)
	self.ui.tab_gnomo.setGeometry(self.tabsize)
	self.ui.tab_moll.setGeometry(self.tabsize)


	#PJ1 - Plate Carree
	pix1 = QPixmap("platecarre.png")	
	self.pc = MyTissot(self.ui.tab_pc, pix1, resol, PJ1.R, PJ1.p)
	self.pc.setGeometry(self.tabsize)

	#PJ2 - Mercator
	pix2 = QPixmap("mercator.png")
	self.merc = MyTissot(self.ui.tab_merc, pix2, resol, PJ2.R, PJ2.p ) 
	self.merc.setGeometry(self.tabsize)

	#PJ3 - Gall-Peters
	pix3 = QPixmap("gallpeters.png")
	self.peters = MyTissot(self.ui.tab_peters, pix3, resol, PJ3.R, PJ3.p)
	self.peters.setGeometry(self.tabsize)

	#PJ4 - Azimuthal Equidistant
	#pj4 = Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)
	pj4trick =  Proj(proj='aeqd', lat_0=90 , ellps='sphere',a=PJ4.R,b=PJ4.R)
	pix4 = QPixmap("aziequi.png")
	self.aziequi = MyTissot(self.ui.tab_aziequi, pix4, resol, PJ4.R, PJ4.p, pj4trick) 
	#Okay, that's a trick. The projection in polar aspect (lat_0=90) instead of the oblique aspect (lon_0=lon0, lat_0=lat0) produces the same Tissot ellipses but it's much more stable numerically.
	self.aziequi.setGeometry(self.tabsize)
	
	#PJ5 - Gnomonic
	#pj5 = Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)
	pj5trick = Proj(proj='gnom', lat_0 = 90 , ellps='sphere',a=PJ5.R,b=PJ5.R)
	pix5 = QPixmap("gnomo.png")
	self.gnomo = MyTissot(self.ui.tab_gnomo, pix5, resol, PJ5.R, PJ5.p , pj5trick) #Same trick.
	self.gnomo.setGeometry(self.tabsize)

	#PJ6 - Mollweide
	pix6 = QPixmap("mollweide.png")
	self.moll = MyTissot(self.ui.tab_moll, pix6, resol, PJ6.R, PJ6.p)
	self.moll.setGeometry(self.tabsize)
	


app = QApplication(sys.argv)
wd =  Mywidget()
#wd.show()
wd.showFullScreen()
app.exec_() 
