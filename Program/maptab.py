# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maptab.ui'
#
# Created: Sun Sep  6 15:31:41 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_maptab(object):
    def setupUi(self, maptab):
        maptab.setObjectName(_fromUtf8("maptab"))
        maptab.resize(946, 553)
        maptab.setWindowTitle(_fromUtf8("Form"))
        self.horizontalLayout = QtGui.QHBoxLayout(maptab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.map_place = QtGui.QFrame(maptab)
        self.map_place.setMinimumSize(QtCore.QSize(420, 422))
        self.map_place.setFrameShape(QtGui.QFrame.NoFrame)
        self.map_place.setObjectName(_fromUtf8("map_place"))
        self.gridLayout_2.addWidget(self.map_place, 0, 0, 1, 2)
        self.text_place = QtGui.QTextEdit(maptab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.text_place.sizePolicy().hasHeightForWidth())
        self.text_place.setSizePolicy(sizePolicy)
        self.text_place.setMinimumSize(QtCore.QSize(500, 0))
        self.text_place.setFrameShape(QtGui.QFrame.NoFrame)
        self.text_place.setReadOnly(True)
        self.text_place.setObjectName(_fromUtf8("text_place"))
        self.gridLayout_2.addWidget(self.text_place, 0, 2, 2, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(maptab)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.radiusbox = QtGui.QDoubleSpinBox(maptab)
        self.radiusbox.setMaximumSize(QtCore.QSize(70, 16777215))
        self.radiusbox.setProperty("value", 20.0)
        self.radiusbox.setObjectName(_fromUtf8("radiusbox"))
        self.gridLayout.addWidget(self.radiusbox, 0, 1, 1, 1)
        self.clearbutton = QtGui.QPushButton(maptab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearbutton.sizePolicy().hasHeightForWidth())
        self.clearbutton.setSizePolicy(sizePolicy)
        self.clearbutton.setObjectName(_fromUtf8("clearbutton"))
        self.gridLayout.addWidget(self.clearbutton, 0, 2, 1, 1)
        self.label = QtGui.QLabel(maptab)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.coordlabel = QtGui.QLabel(maptab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coordlabel.sizePolicy().hasHeightForWidth())
        self.coordlabel.setSizePolicy(sizePolicy)
        self.coordlabel.setMinimumSize(QtCore.QSize(120, 0))
        self.coordlabel.setText(_fromUtf8(""))
        self.coordlabel.setObjectName(_fromUtf8("coordlabel"))
        self.gridLayout.addWidget(self.coordlabel, 1, 1, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(maptab)
        QtCore.QMetaObject.connectSlotsByName(maptab)

    def retranslateUi(self, maptab):
        self.label_2.setText(_translate("maptab", "r =", None))
        self.clearbutton.setText(_translate("maptab", "Clear", None))
        self.label.setText(_translate("maptab", "Coordinates:", None))

