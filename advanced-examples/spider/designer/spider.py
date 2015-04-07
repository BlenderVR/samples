# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/AstrApple/WorkSpace/BlenderVR_Workspace/BlenderVR_git/samples/spider/designer/spider.ui'
#
# Created: Sat Jan 31 09:33:53 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Mountain(object):
    def setupUi(self, Mountain):
        Mountain.setObjectName("Mountain")
        Mountain.resize(410, 277)
        self.gridLayout_2 = QtGui.QGridLayout(Mountain)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.HC_Nav = QtGui.QWidget(Mountain)
        self.HC_Nav.setObjectName("HC_Nav")
        self.gridLayout_2.addWidget(self.HC_Nav, 0, 0, 1, 1)

        self.retranslateUi(Mountain)
        QtCore.QMetaObject.connectSlotsByName(Mountain)

    def retranslateUi(self, Mountain):
        Mountain.setWindowTitle(QtGui.QApplication.translate("Mountain", "Form", None, QtGui.QApplication.UnicodeUTF8))

