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

	self.maps=[]
	for pj in PJlist:
		pjmap = SoeMap(self, self.ui, pj, resol)
		self.ui.tab_maps.addTab(pjmap, pj.fullname)
		self.maps.append(pjmap)
		

	self.updateMap()
	self.setTexts()
	self.connect(self.ui.infobutton,SIGNAL("clicked(bool)"),self.ui.text_place.setVisible)
	self.connect(self.ui.langbox, SIGNAL("currentIndexChanged(int)"), self.setTexts)
	self.connect(self.ui.tab_maps, SIGNAL("currentChanged(int)"), self.setTexts)
	self.connect(self.ui.tab_maps, SIGNAL("currentChanged(int)"), self.updateMap)

	self.connect(self.ui.tissot_clear, SIGNAL("clicked()"),self.ClearEllipses)
	self.connect(self.ui.tissot_undo, SIGNAL("clicked()"),self.UndoEllipse)
	self.connect(self.ui.tissot_sample, SIGNAL("clicked()"),self.SampleEllipses)

    def ClearEllipses(self):
	self.listellip = []
	for mp in self.maps:
		mp.tissotLayer_bg.update()

    def UndoEllipse(self):
	if len(self.listellip) > 0 :
		self.listellip.pop()
	for mp in self.maps:
		mp.tissotLayer_bg.update()

    def SampleEllipses(self):
	for i in range(-120,180,60):
		for j in range(-40,80,40):
			self.listellip.append([i,j])
	for i in range(-150,180,60):
		for j in range(-60,80,40):
			self.listellip.append([i,j])
	for mp in self.maps:
		mp.tissotLayer_bg.update()

    def setTexts(self):
	self.lang=Languages[self.ui.langbox.currentIndex()]

	translator.load(os.path.join(application_path,"soe_"+self.lang))
	self.ui.retranslateUi(self)

	txtfile=open(os.path.join(application_path,'txt',self.lang,'intro.html'),'r')
	txt=QString.fromUtf8(txtfile.read())
	self.ui.text_intro.document().setMetaInformation(QTextDocument.DocumentUrl,application_path+'/')
	self.ui.text_intro.setHtml(txt)
	txtfile.close()

	currentmap = self.ui.tab_maps.currentIndex()
	try:
		txtfile=open(os.path.join(application_path,'txt',self.lang,PJlist[currentmap].name + '.html'),'r')
	except:
		txtfile=open(os.path.join(application_path,'txt','common','noinfo.html'),'r')

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
	currentmap = self.ui.tab_maps.currentIndex()
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




#wd.setFont(qfontdb.font("Ubuntu", "Normal", 12))
#wd.setFont(QFont("Times", 12, QFont.Bold))
#wd.show()
#wd.showFullScreen()




if "--allprojs" in sys.argv :
	Projs = ["platecarre", "mercator", "gallpeters", "aziequi", "gnomo", "mollweide", "stere", "vandg", "goode", "sinu", "tmerc", "robin"]
else:
	Projs = ["platecarre","mercator","gallpeters","aziequi","gnomo","mollweide"]

PJlist=[]
for key in Projs:
	PJlist.append(AllPJdict[key])


wd =  Mywidget()
if "--fullscreen" in sys.argv :
	wd.showFullScreen()
else:
	wd.show()


app.exec_() 
