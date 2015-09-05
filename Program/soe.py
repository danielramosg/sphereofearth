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



from PyQt4 import QtCore, QtGui
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui_soe import *
from maptab import *

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
lang = params.get('Language','lang')



class Mywidget (QWidget):

    def __init__(self):
        QWidget.__init__(self)

	#QApplication.setOverrideCursor(QCursor(Qt.BlankCursor)) #No cursor. Use for touchscreens.

	self.ui=Ui_Form()
	self.ui.setupUi(self)


	txtfile=open('./txt/'+lang+'/intro.html','r')
	txt=QString.fromUtf8(txtfile.read())
	self.ui.text_place.setHtml(txt)
	txtfile.close()
	
	#PJ1 - Plate Carree
	self.maptab_pc=Ui_maptab()
	self.maptab_pc.setupUi(self.ui.tab_pc)
	
	self.layo_pc=QHBoxLayout()
	self.maptab_pc.map_place.setLayout(self.layo_pc)

	self.map_pc = MyTissot(self.maptab_pc.map_place, self.maptab_pc, PJ1, resol)
	self.layo_pc.addWidget(self.map_pc)

	#self.maptab_pc.text_place.hide()

#	#PJ2 - Mercator
	self.maptab_merc=Ui_maptab()
	self.maptab_merc.setupUi(self.ui.tab_merc)
	
	self.layo_merc=QHBoxLayout()
	self.maptab_merc.map_place.setLayout(self.layo_merc)

	self.map_merc = MyTissot(self.maptab_merc.map_place, self.maptab_merc, PJ2, resol)
	self.layo_merc.addWidget(self.map_merc)

#	#PJ3 - Gall-Peters
	self.maptab_peters=Ui_maptab()
	self.maptab_peters.setupUi(self.ui.tab_peters)
	
	self.layo_peters=QHBoxLayout()
	self.maptab_peters.map_place.setLayout(self.layo_peters)

	self.map_peters = MyTissot(self.maptab_peters.map_place, self.maptab_peters, PJ3, resol)
	self.layo_peters.addWidget(self.map_peters)

#	#PJ4 - Azimuthal Equidistant
	self.maptab_aziequi=Ui_maptab()
	self.maptab_aziequi.setupUi(self.ui.tab_aziequi)
	
	self.layo_aziequi=QHBoxLayout()
	self.maptab_aziequi.map_place.setLayout(self.layo_aziequi)

	pj4trick =  Proj(proj='aeqd', lat_0=90 , ellps='sphere',a=PJ4.R,b=PJ4.R)
	self.map_aziequi = MyTissot(self.maptab_aziequi.map_place, self.maptab_aziequi, PJ4, resol, pj4trick)
	self.layo_aziequi.addWidget(self.map_aziequi)
	#Okay, that's a trick. The projection in polar aspect (lat_0=90) instead of the oblique aspect (lon_0=lon0, lat_0=lat0) produces the same Tissot ellipses but it's much more stable numerically.

#	#PJ5 - Gnomonic
	self.maptab_gnomo=Ui_maptab()
	self.maptab_gnomo.setupUi(self.ui.tab_gnomo)
	
	self.layo_gnomo=QHBoxLayout()
	self.maptab_gnomo.map_place.setLayout(self.layo_gnomo)

	pj5trick = Proj(proj='gnom', lat_0 = 90 , ellps='sphere',a=PJ5.R,b=PJ5.R)
	self.map_gnomo = MyTissot(self.maptab_gnomo.map_place, self.maptab_gnomo, PJ5, resol, pj5trick)
	self.layo_gnomo.addWidget(self.map_gnomo)
	#Same trick.

#	#PJ6 - Mollweide
	self.maptab_moll=Ui_maptab()
	self.maptab_moll.setupUi(self.ui.tab_moll)
	
	self.layo_moll=QHBoxLayout()
	self.maptab_moll.map_place.setLayout(self.layo_moll)

	self.map_moll = MyTissot(self.maptab_moll.map_place, self.maptab_moll, PJ6, resol)
	self.layo_moll.addWidget(self.map_moll)
	


app = QApplication(sys.argv)
wd =  Mywidget()
#wd.show()
#wd.showFullScreen()

if len(sys.argv)==2:
	try:
		ar=sys.argv[1]
	except:
		sys.exit()
else:
	ar=None


if ar=="--fullscreen":
	wd.showFullScreen()
elif ar==None:
	wd.show()
else:
	print "Option not valid"
	sys.exit()

app.exec_() 
