# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dial_Rendering.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Rendering(object):
    def setupUi(self, Rendering):
        Rendering.setObjectName("Rendering")
        Rendering.setWindowModality(QtCore.Qt.WindowModal)
        Rendering.resize(400, 211)
        self.gridLayout = QtWidgets.QGridLayout(Rendering)
        self.gridLayout.setObjectName("gridLayout")
        self.levels_group = QtWidgets.QGroupBox(Rendering)
        self.levels_group.setObjectName("levels_group")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.levels_group)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_vertical = QtWidgets.QVBoxLayout()
        self.layout_vertical.setObjectName("layout_vertical")
        self.verticalLayout.addLayout(self.layout_vertical)
        self.gridLayout.addWidget(self.levels_group, 0, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(Rendering)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 1, 0, 1, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(Rendering)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Abort|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 2)

        self.retranslateUi(Rendering)
        self.buttonBox.accepted.connect(Rendering.accept)
        self.buttonBox.rejected.connect(Rendering.reject)
        QtCore.QMetaObject.connectSlotsByName(Rendering)

    def retranslateUi(self, Rendering):
        _translate = QtCore.QCoreApplication.translate
        Rendering.setWindowTitle(_translate("Rendering", "Rendering State"))
        self.levels_group.setTitle(_translate("Rendering", "States building :"))

