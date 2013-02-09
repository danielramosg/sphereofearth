
# -*- coding: utf-8 -*-

# Author: Daniel Ramos



from PyQt4 import QtCore, QtGui
import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ui_soe import *

from pyproj import Proj


from tissot import *    

lon0 = 2.170035 #Bcn
lat0 = 41.386996 #Bcn



class Mywidget (QWidget):

    def __init__(self):
        QWidget.__init__(self)

	self.ui=Ui_Form()
	self.ui.setupUi(self)

	
	
	self.resize(1050,650)
	self.tabsize = QRect(0, 0, 1050, 650)
	
	
	pj1 = Proj(proj='eqc',ellps='sphere',a=R,b=R)
	pix1 = QPixmap("platecarre.png")
	self.pc = MyTissot(self.ui.tab_pc, pix1 ,0.8, pj1) #QRect(0, 0, 1000, 500)
	self.pc.setGeometry(self.tabsize)
	#self.pc.SC = 40000.	

	pj2 = Proj(proj='merc',ellps='sphere',a=R,b=R)
	pix2 = QPixmap("mercator.png")
	self.merc = MyTissot(self.ui.tab_merc, pix2 ,0.6, pj2 ) #QRect(201, 0, 597, 500)
	self.merc.setGeometry(self.tabsize)
	#self.merc.SC = 47790.

	pj3 = Proj(proj='cea', lat_ts = 45, ellps='sphere', a=R, b=R)
	pix3 = QPixmap("gallpeters.png")
	self.peters = MyTissot(self.ui.tab_peters, pix3 , 0.95 , pj3) #QRect(50, 0, 900, 573)
	self.peters.setGeometry(self.tabsize)
	#self.peters.SC = 31427.

	pj4 = Proj(proj='aeqd', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)
	pj4trick =  Proj(proj='aeqd', lat_0=90 , ellps='sphere',a=R,b=R)
	pix4 = QPixmap("aziequi.png")
	self.aziequi = MyTissot(self.ui.tab_aziequi, pix4 , 0.45 , pj4 , pj4trick) #QRect(250, 0, 500, 500)
	#Okay, that's a trick. The projection in polar aspect (lat_0=90) instead of the oblique aspect (lon_0=lon0, lat_0=lat0) produces the same Tissot ellipses but it's much more stable numerically.
	self.aziequi.setGeometry(self.tabsize)
	#self.aziequi.SC = 40000000/500.
	
	pj5 = Proj(proj='gnom', lon_0=lon0, lat_0=lat0, ellps='sphere',a=R,b=R)
	pj5trick = Proj(proj='gnom', lat_0 = 90 , ellps='sphere',a=R,b=R)
	pix5 = QPixmap("gnomo.png")
	self.gnomo = MyTissot(self.ui.tab_gnomo, pix5 , 0.5 , pj5 , pj5trick) #Same trick.#QRect(250, 0, 500, 500)
	self.gnomo.setGeometry(self.tabsize)
	#self.gnomo.SC = 18006324./500

	pj6 = Proj(proj='moll',ellps='sphere',a=R,b=R)
	pix6 = QPixmap("mollweide.png")
	self.moll = MyTissot(self.ui.tab_moll, pix6 , 0.9 , pj6) #QRect(0, 0, 1000, 500)
	self.moll.setGeometry(self.tabsize)
	#self.moll.SC = 18006324./500.
	


app = QApplication(sys.argv)
wd =  Mywidget()
wd.show()
app.exec_() 
