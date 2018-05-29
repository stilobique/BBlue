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
        self.levels_layout = QtWidgets.QHBoxLayout()
        self.levels_layout.setObjectName("levels_layout")
        self.lvl_name_placeholder = QtWidgets.QLabel(self.levels_group)
        self.lvl_name_placeholder.setToolTip("")
        self.lvl_name_placeholder.setStatusTip("")
        self.lvl_name_placeholder.setWhatsThis("")
        self.lvl_name_placeholder.setAccessibleName("")
        self.lvl_name_placeholder.setAccessibleDescription("")
        self.lvl_name_placeholder.setText("Level rendering name :")
        self.lvl_name_placeholder.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lvl_name_placeholder.setObjectName("lvl_name_placeholder")
        self.levels_layout.addWidget(self.lvl_name_placeholder)
        self.lvl_logo_placeholder = QtWidgets.QLabel(self.levels_group)
        self.lvl_logo_placeholder.setMinimumSize(QtCore.QSize(16, 16))
        self.lvl_logo_placeholder.setMaximumSize(QtCore.QSize(16, 16))
        self.lvl_logo_placeholder.setText("")
        self.lvl_logo_placeholder.setPixmap(QtGui.QPixmap("Resources/Icons/s-valid.png"))
        self.lvl_logo_placeholder.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lvl_logo_placeholder.setObjectName("lvl_logo_placeholder")
        self.levels_layout.addWidget(self.lvl_logo_placeholder)
        self.lvl_state_placeholder = QtWidgets.QLabel(self.levels_group)
        self.lvl_state_placeholder.setObjectName("lvl_state_placeholder")
        self.levels_layout.addWidget(self.lvl_state_placeholder)
        self.verticalLayout.addLayout(self.levels_layout)
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
        self.lvl_state_placeholder.setText(_translate("Rendering", "statut levels"))

