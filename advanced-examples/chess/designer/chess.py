# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Users/AstrApple/WorkSpace/BlenderVR_Workspace/blenderVR_git/samples/chess/designer/chess.ui'
#
# Created: Sat Jan 31 09:16:34 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Mountain(object):
    def setupUi(self, Mountain):
        Mountain.setObjectName("Mountain")
        Mountain.resize(406, 300)
        self.gridLayout = QtGui.QGridLayout(Mountain)
        self.gridLayout.setObjectName("gridLayout")
        self.HC_Nav = QtGui.QWidget(Mountain)
        self.HC_Nav.setObjectName("HC_Nav")
        self.gridLayout.addWidget(self.HC_Nav, 0, 0, 1, 1)

        self.retranslateUi(Mountain)
        QtCore.QMetaObject.connectSlotsByName(Mountain)

    def retranslateUi(self, Mountain):
        Mountain.setWindowTitle(QtGui.QApplication.translate("Mountain", "Form", None, QtGui.QApplication.UnicodeUTF8))

