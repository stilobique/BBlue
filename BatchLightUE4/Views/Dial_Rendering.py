import psutil

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

from BatchLightUE4.Views.Dial_Rendering_convert import Ui_Rendering
from BatchLightUE4.Controllers.Swarm import build
from BatchLightUE4.Controllers.Perfoce import p4_checkout, p4_submit


class DialRendering(QtWidgets.QDialog, Ui_Rendering):
    def __init__(self, parent, lvl_list, csv=False, submit=False):
        """
        Rendering Dialog Box, all connect and slot.

        :param lvl_list: a list with all level rendering.
        :param csv: data with the CSV used (boolean or list)
        :param submit: Boolean, launch or not the submit phase
        """
        super(DialRendering, self).__init__(parent)
        self.setupUi(self)

        # Define data and variables.
        self.levels = lvl_list
        self.levels_count = len(lvl_list)

        # Base UI
        self.levels_works(self.levels)
        self.progress_bar_ui()
        self.buttons_box()

        # Launch all building light.
        self.building_light = ThreadRendering(lvl_list, csv, submit)
        self.building_light.start()
        self.building_light.progress_value.connect(self.progress_bar_ui)

    # Ui Function -------------------------------------------------------------
    #   Generate the list with all levels rendering ---------------------------
    def levels_works(self, lvl_list):
        """
        Function to show all levels and what's is working.
        :param lvl_list: list with all levels to build
        :return:
        """
        group_parent = self.levels_group
        vertical_parent = self.layout_vertical
        vertical_parent.setAlignment(Qt.AlignJustify)

        for item in lvl_list:
            # Define horizontal layout
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setObjectName('h_layout')
            h_layout.setAlignment(Qt.AlignLeft)

            # Generate the logo used
            lvl_list.index(item)
            icon = QtGui.QPixmap("Resources/Icons/s-empty.png")

            # Define all label
            level_name = QtWidgets.QLabel(group_parent)
            level_name.setText("Level rendering name :")
            level_logo = QtWidgets.QLabel(group_parent)
            level_logo.setText('')
            level_logo.setPixmap(icon)
            level_item = QtWidgets.QLabel(group_parent)
            level_item.setText(item)

            h_layout.addWidget(level_name, alignment=Qt.AlignRight)
            h_layout.addWidget(level_logo, alignment=Qt.AlignCenter)
            h_layout.addWidget(level_item, alignment=Qt.AlignLeft)
            vertical_parent.addLayout(h_layout)

    #   Bottom Toolbars, option to launch the rendering and the log -----------
    def progress_bar_ui(self, value=0):
        """
        Setup the Progress Bar, give the maximum value and the value used.
        :param value: a Int value, this value give the statue about the bar
        :return:
        """
        # Setup the Progress bar with the data
        self.progressBar.setValue(value)
        self.progressBar.setMaximum(self.levels_count)

    #   Bottom Toolbars, option to launch the rendering and the log -----------
    def buttons_box(self, state=True):
        """
        Setup the UI Buttons
        :param state: Boolean to define the state about the button "Ok"
        :return:
        """
        box_btn = QtWidgets.QDialogButtonBox
        btn = self.buttonBox.button
        btn(box_btn.Ok).clicked.connect(self.close)
        btn(box_btn.Ok).setEnabled(state)
        btn(box_btn.Abort).clicked.connect(self.stop_rendering)

    @staticmethod
    def stop_rendering():
        print('Stop Rendering')


class ThreadRendering(QtCore.QThread):
    progress_value = pyqtSignal(int)

    def __init__(self, level_rendering, csv, submit):
        """
        This Class use the building operator in a separated thread, without
        this class the program freeze when a built it.

        :param level_rendering: A level list we want build it
        :type level_rendering: list
        :param csv: information about the CSV used (False or other)
        :type csv: String
        :param submit: Info if the instance need to submit the rendering
        :type submit: bool
        """
        QtCore.QThread.__init__(self)
        self.lvl_list = level_rendering
        self.csv_data = csv
        self.submit = submit
        self._running = True

    def __del__(self):
        self.wait()

    def run(self):
        print('Hello, i am a thread')
        self.sleep(4)

        for level in self.lvl_list:
            swarm = build(level)
            while swarm:
                self.sleep(20)
                if swarm.pid not in psutil.pids():
                    count = self.lvl_list.index(level)
                    self.progress_value.emit(count + 1)
                    break

            print('End Looping')
