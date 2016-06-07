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



from PyQt4 import QtCore, QtGui
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui_soe import *

from pyproj import Proj

from projections_multiscale import *
from tissot import *    

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):     # "bundled" on a executable
	application_path = os.path.dirname(sys.executable)
elif __file__:     # "live" script, running using an interpreter
	application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, 'param.ini')

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read(config_path)	
	
R = params.getfloat('Maps_Size','radius_of_the_globe')
resol = params.getfloat('Maps_Size','resolution')
lon0 =  params.getfloat('Center_of_projections','longitude')
lat0 =  params.getfloat('Center_of_projections','latitude')

NUMVERSION = '1.2.0'


Languages = ["ca","en","es","fr","nl"] #Avaliable languages, ordered.
LangNames = {"ca":QString(u'Català'), "en":QString(u'English'), "es":QString(u'Español'), "fr":QString(u'Français'), "nl":QString(u'Nederlands')}
PJS = [0,PJ1,PJ2,PJ3,PJ4,PJ5,PJ6]



class Mywidget (QWidget):

    def __init__(self):
        QWidget.__init__(self)

	#QApplication.setOverrideCursor(QCursor(Qt.BlankCursor)) #No cursor. Use for touchscreens.

	self.ui=Ui_Form()
	self.ui.setupUi(self)
	for lng in Languages:
		self.ui.langbox.insertItem(99,LangNames[lng])
	self.ui.langbox.setCurrentIndex(0) #Sets the default language, the index is that of Languages list.


	self.listellip = []   # list of points where ellipses are to be drawn, in format [lon,lat]
	self.geoptA = None
	self.geoptB = None
	self.loxptA = None
	self.loxptB = None

	self.maps=[0]
	for i in range(1,7):
		placement = self.ui.tab_maps.widget(i-1)
		
		layo=QHBoxLayout()
		#layo.setGeometry(QRect(0,0,100,100))
		placement.setLayout(layo)

		if i==4:
			pj4trick =  Proj(proj='aeqd', lat_0=90 , ellps='sphere',a=PJ4.R,b=PJ4.R)
			pjmap = SoeMap(self, self.ui, PJ4, resol, pj4trick)
			#Okay, that's a trick. The projection in polar aspect (lat_0=90) instead of the oblique aspect (lon_0=lon0, lat_0=lat0) produces the same Tissot ellipses but it's much more stable numerically.
		elif i==5:
			pj5trick = Proj(proj='gnom', lat_0 = 90 , ellps='sphere',a=PJ5.R,b=PJ5.R)
			pjmap= SoeMap(self, self.ui, PJ5, resol, pj5trick)
			#Same trick.
		else:
			pjmap = SoeMap(self, self.ui, PJS[i], resol)

		layo.addWidget(pjmap)
		self.maps.append(pjmap)
		

	self.updateMap()
	self.setTexts()
	self.connect(self.ui.infobutton,SIGNAL("clicked(bool)"),self.ui.text_place.setVisible)
	self.connect(self.ui.langbox, SIGNAL("currentIndexChanged(int)"), self.setTexts)
	self.connect(self.ui.tab_maps, SIGNAL("currentChanged(int)"), self.setTexts)
	self.connect(self.ui.tab_maps, SIGNAL("currentChanged(int)"), self.updateMap)


    def setTexts(self):
	self.lang=Languages[self.ui.langbox.currentIndex()]

	translator.load(os.path.join(application_path,"soe_"+self.lang))
	self.ui.retranslateUi(self)

	txtfile=open(os.path.join(application_path,'txt',self.lang,'intro.html'),'r')
	txt=QString.fromUtf8(txtfile.read())
	self.ui.text_intro.document().setMetaInformation(QTextDocument.DocumentUrl,application_path+'/')
	self.ui.text_intro.setHtml(txt)
	txtfile.close()

	currentmap = self.ui.tab_maps.currentIndex() + 1
	txtfile=open(os.path.join(application_path,'txt',self.lang,PJS[currentmap].name + '.html'),'r')
	txt=QString.fromUtf8(txtfile.read())
	self.ui.text_place.setHtml(txt)
	txtfile.close()

	txtfile=open(os.path.join(application_path,'txt',self.lang,'about.html'),'r')
	txt=QString.fromUtf8(txtfile.read().replace('\NumVersion',NUMVERSION))
	self.ui.text_about.setLineWrapMode(QTextEdit.NoWrap)
	self.ui.text_about.document().setMetaInformation(QTextDocument.DocumentUrl,application_path+'/')
	self.ui.text_about.setHtml(txt)
	txtfile.close()
	
    def updateMap(self):
	currentmap = self.ui.tab_maps.currentIndex() + 1
	self.maps[currentmap].tissotLayer_bg.update()
	

app = QApplication(sys.argv)

#app.setStyleSheet("QWidget { font: bold }")

translator= QTranslator()
#translator.load("soe_es")
#translator.load("soe_en")
app.installTranslator(translator)

#qfontdb = QFontDatabase()
#qfontdb.addApplicationFont("Ubuntu-M.ttf")

#stylesheet = QtCore.QFile("soestyle.qss")
#if stylesheet.open(QtCore.QIODevice.ReadOnly | QtCore.QIODevice.Text) :
#	app.setStyleSheet(stylesheet.readAll().data())


wd =  Mywidget()

#wd.setFont(qfontdb.font("Ubuntu", "Normal", 12))
#wd.setFont(QFont("Times", 12, QFont.Bold))
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
