# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/AstrApple/WorkSpace/BlenderVR_Workspace/BlenderVR_git/samples/simple/designer/simple.ui'
#
# Created: Sun Jan 25 22:18:09 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_simple(object):
    def setupUi(self, simple):
        simple.setObjectName("simple")
        simple.resize(406, 300)
        self.gridLayout_2 = QtGui.QGridLayout(simple)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtGui.QGroupBox(simple)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.set_user_name = QtGui.QPushButton(self.groupBox)
        self.set_user_name.setObjectName("set_user_name")
        self.gridLayout.addWidget(self.set_user_name, 1, 0, 1, 1)
        self.user_name = QtGui.QLineEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.user_name.sizePolicy().hasHeightForWidth())
        self.user_name.setSizePolicy(sizePolicy)
        self.user_name.setObjectName("user_name")
        self.gridLayout.addWidget(self.user_name, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 2)
        self.HC_nav = QtGui.QWidget(simple)
        self.HC_nav.setObjectName("HC_nav")
        self.gridLayout_2.addWidget(self.HC_nav, 0, 0, 1, 2)
        self.ArcBall = QtGui.QWidget(simple)
        self.ArcBall.setObjectName("ArcBall")
        self.gridLayout_2.addWidget(self.ArcBall, 2, 0, 1, 2)

        self.retranslateUi(simple)
        QtCore.QMetaObject.connectSlotsByName(simple)

    def retranslateUi(self, simple):
        simple.setWindowTitle(QtGui.QApplication.translate("simple", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("simple", "User name", None, QtGui.QApplication.UnicodeUTF8))
        self.set_user_name.setText(QtGui.QApplication.translate("simple", "Set user name", None, QtGui.QApplication.UnicodeUTF8))

