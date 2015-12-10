# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'maptab.ui'
#
# Created: Thu Dec 10 19:40:49 2015
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
        maptab.resize(1208, 555)
        maptab.setWindowTitle(_fromUtf8("Form"))
        self.verticalLayout = QtGui.QVBoxLayout(maptab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
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
        self.text_place.setMinimumSize(QtCore.QSize(600, 0))
        self.text_place.setFrameShape(QtGui.QFrame.NoFrame)
        self.text_place.setReadOnly(True)
        self.text_place.setObjectName(_fromUtf8("text_place"))
        self.gridLayout_2.addWidget(self.text_place, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(13, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.geod_select = QtGui.QRadioButton(maptab)
        self.geod_select.setMouseTracking(False)
        self.geod_select.setFocusPolicy(QtCore.Qt.TabFocus)
        self.geod_select.setChecked(True)
        self.geod_select.setObjectName(_fromUtf8("geod_select"))
        self.gridLayout.addWidget(self.geod_select, 0, 0, 1, 1)
        self.label = QtGui.QLabel(maptab)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(maptab)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        self.label_4 = QtGui.QLabel(maptab)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 3, 1, 1)
        self.distlabel = QtGui.QLabel(maptab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.distlabel.sizePolicy().hasHeightForWidth())
        self.distlabel.setSizePolicy(sizePolicy)
        self.distlabel.setMinimumSize(QtCore.QSize(400, 0))
        self.distlabel.setText(_fromUtf8(""))
        self.distlabel.setObjectName(_fromUtf8("distlabel"))
        self.gridLayout.addWidget(self.distlabel, 0, 2, 1, 1)
        self.geod_clear = QtGui.QPushButton(maptab)
        self.geod_clear.setObjectName(_fromUtf8("geod_clear"))
        self.gridLayout.addWidget(self.geod_clear, 0, 5, 1, 1)
        self.unitbox = QtGui.QDoubleSpinBox(maptab)
        self.unitbox.setSuffix(_fromUtf8(" km"))
        self.unitbox.setDecimals(0)
        self.unitbox.setMinimum(500.0)
        self.unitbox.setMaximum(20000.0)
        self.unitbox.setSingleStep(100.0)
        self.unitbox.setProperty("value", 1000.0)
        self.unitbox.setObjectName(_fromUtf8("unitbox"))
        self.gridLayout.addWidget(self.unitbox, 0, 4, 1, 1)
        self.tissot_select = QtGui.QRadioButton(maptab)
        self.tissot_select.setFocusPolicy(QtCore.Qt.TabFocus)
        self.tissot_select.setObjectName(_fromUtf8("tissot_select"))
        self.gridLayout.addWidget(self.tissot_select, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(maptab)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.radiusbox = QtGui.QDoubleSpinBox(maptab)
        self.radiusbox.setDecimals(1)
        self.radiusbox.setProperty("value", 20.0)
        self.radiusbox.setObjectName(_fromUtf8("radiusbox"))
        self.gridLayout.addWidget(self.radiusbox, 1, 4, 1, 1)
        self.tissot_clear = QtGui.QPushButton(maptab)
        self.tissot_clear.setObjectName(_fromUtf8("tissot_clear"))
        self.gridLayout.addWidget(self.tissot_clear, 1, 5, 1, 1)
        self.coordlabel = QtGui.QLabel(maptab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.coordlabel.sizePolicy().hasHeightForWidth())
        self.coordlabel.setSizePolicy(sizePolicy)
        self.coordlabel.setMinimumSize(QtCore.QSize(150, 0))
        self.coordlabel.setText(_fromUtf8(""))
        self.coordlabel.setObjectName(_fromUtf8("coordlabel"))
        self.gridLayout.addWidget(self.coordlabel, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(maptab)
        QtCore.QMetaObject.connectSlotsByName(maptab)

    def retranslateUi(self, maptab):
        self.geod_select.setText(_translate("maptab", "Geodesic", None))
        self.label.setText(_translate("maptab", "Coordinates:", None))
        self.label_3.setText(_translate("maptab", "Distance:", None))
        self.label_4.setText(_translate("maptab", "Unit:", None))
        self.geod_clear.setText(_translate("maptab", "Clear", None))
        self.tissot_select.setText(_translate("maptab", "Tissot\'s Indicatrix", None))
        self.label_2.setText(_translate("maptab", "Radius:", None))
        self.tissot_clear.setText(_translate("maptab", "Clear", None))

