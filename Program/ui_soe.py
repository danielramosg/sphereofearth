# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'soe.ui'
#
# Created: Sun Dec 16 19:31:19 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(720, 491)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "The Sphere of the Earth", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_pc = QtGui.QWidget()
        self.tab_pc.setObjectName(_fromUtf8("tab_pc"))
        self.tabWidget.addTab(self.tab_pc, _fromUtf8(""))
        self.tab_merc = QtGui.QWidget()
        self.tab_merc.setObjectName(_fromUtf8("tab_merc"))
        self.tabWidget.addTab(self.tab_merc, _fromUtf8(""))
        self.tab_peters = QtGui.QWidget()
        self.tab_peters.setObjectName(_fromUtf8("tab_peters"))
        self.tabWidget.addTab(self.tab_peters, _fromUtf8(""))
        self.tab_aziequi = QtGui.QWidget()
        self.tab_aziequi.setObjectName(_fromUtf8("tab_aziequi"))
        self.tabWidget.addTab(self.tab_aziequi, _fromUtf8(""))
        self.tab_gnomo = QtGui.QWidget()
        self.tab_gnomo.setObjectName(_fromUtf8("tab_gnomo"))
        self.tabWidget.addTab(self.tab_gnomo, _fromUtf8(""))
        self.tab_moll = QtGui.QWidget()
        self.tab_moll.setObjectName(_fromUtf8("tab_moll"))
        self.tabWidget.addTab(self.tab_moll, _fromUtf8(""))
        self.tab_about = QtGui.QWidget()
        self.tab_about.setObjectName(_fromUtf8("tab_about"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.tab_about)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label = QtGui.QLabel(self.tab_about)
        self.label.setMinimumSize(QtCore.QSize(161, 101))
        self.label.setMaximumSize(QtCore.QSize(161, 101))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("logo.png")))
        self.label.setScaledContents(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.textEdit = QtGui.QTextEdit(self.tab_about)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.textEdit.setReadOnly(True)
        self.textEdit.setHtml(QtGui.QApplication.translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:200; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The Sphere of the Earth.</span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Version 1.0.0. </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">December 2012</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Author: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Daniel Ramos </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">daniel.ramos@mmaca.cat</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">www.mmaca.cat</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.horizontalLayout_3.addWidget(self.textEdit)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.tabWidget.addTab(self.tab_about, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pc), QtGui.QApplication.translate("Form", "Plate Carrée", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_merc), QtGui.QApplication.translate("Form", "Mercator", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_peters), QtGui.QApplication.translate("Form", "Gall-Peters", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_aziequi), QtGui.QApplication.translate("Form", "Azimuthal Equidistant", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_gnomo), QtGui.QApplication.translate("Form", "Gnomonic", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_moll), QtGui.QApplication.translate("Form", "Mollweide", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), QtGui.QApplication.translate("Form", "About", None, QtGui.QApplication.UnicodeUTF8))

