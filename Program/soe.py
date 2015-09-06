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


Languages = {QString(u'English'):"en", QString(u'Español'):"es"}
PJS = [0,PJ1,PJ2,PJ3,PJ4,PJ5,PJ6]



class Mywidget (QWidget):

    def __init__(self):
        QWidget.__init__(self)

	#QApplication.setOverrideCursor(QCursor(Qt.BlankCursor)) #No cursor. Use for touchscreens.

	self.ui=Ui_Form()
	self.ui.setupUi(self)


	self.maptabs=[0]
	for i in range(1,7):
		maptab=Ui_maptab()
		maptab.setupUi(self.ui.tabWidget.widget(i))
	
		layo=QHBoxLayout()
		maptab.map_place.setLayout(layo)

		if i==4:
			pj4trick =  Proj(proj='aeqd', lat_0=90 , ellps='sphere',a=PJ4.R,b=PJ4.R)
			pjmap = MyTissot(maptab.map_place, maptab, PJ4, resol, pj4trick)
			#Okay, that's a trick. The projection in polar aspect (lat_0=90) instead of the oblique aspect (lon_0=lon0, lat_0=lat0) 			produces the same Tissot ellipses but it's much more stable numerically.
		elif i==5:
			pj5trick = Proj(proj='gnom', lat_0 = 90 , ellps='sphere',a=PJ5.R,b=PJ5.R)
			pjmap= MyTissot(maptab.map_place, maptab, PJ5, resol, pj5trick)
			#Same trick.
		else:
			pjmap = MyTissot(maptab.map_place, maptab, PJS[i], resol)

		layo.addWidget(pjmap)

		self.maptabs.append(maptab)
	#self.maptabs[1].text_place.hide()

	self.setTexts()
	self.connect(self.ui.langbox, SIGNAL("currentIndexChanged(int)"), self.setTexts)
	



    def setTexts(self):
	self.lang=Languages[self.ui.langbox.currentText()]

	translator.load("soe_"+self.lang)
	self.ui.retranslateUi(self)
	for i in range(1,7):
		self.maptabs[i].retranslateUi(None)

	txtfile=open('./txt/'+self.lang+'/intro.html','r')
	txt=QString.fromUtf8(txtfile.read())
	self.ui.text_place.setHtml(txt)
	txtfile.close()

	for i in range(1,7):
		txtfile=open('./txt/' + self.lang +'/' + PJS[i].name + '.html','r')
		txt=QString.fromUtf8(txtfile.read())
		self.maptabs[i].text_place.setHtml(txt)
		txtfile.close()


	


app = QApplication(sys.argv)

translator= QTranslator()
#translator.load("soe_es")
#translator.load("soe_en")
app.installTranslator(translator)

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
