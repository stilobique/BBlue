import psutil

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt

from BatchLightUE4.Views.Dial_Rendering_convert import Ui_Rendering
from BatchLightUE4.Controllers.Swarm import build
from BatchLightUE4.Controllers.Perfoce import p4_checkout, p4_submit


class DialRendering(QtWidgets.QDialog, Ui_Rendering):
    value_slide = pyqtSignal(int)

    def __init__(self, parent, lvl_list, csv=False, submit=False):
        """
        Rendering Dialog Box, all connect and slot.

        :param lvl_list: a list with all level rendering.
        :param csv: data with the CSV used (boolean or list)
        :param submit: Boolean, launch or not the submit phase
        """
        super(DialRendering, self).__init__(parent)
        self.setupUi(self)

        # Base UI
        self.levels_works(lvl_list)
        self.progress_bar_ui(total=len(lvl_list))
        self.buttons_box()

        # Setup the Progress bar with the data
        # self.swarm = ThreadRendering(lvl_list, csv, submit)
        # self.progressBar.valueChanged.connect(self.progress_built)
        # self.swarm.start()

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
        for item in lvl_list:
            # Define horizontal layout
            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setObjectName('h_layout')

            # Generate the logo used
            icon = QtGui.QPixmap("Resources/Icons/s-valid.png")

            # Define all label
            level_name = QtWidgets.QLabel(group_parent)
            level_name.setText("Level rendering name :")
            level_logo = QtWidgets.QLabel(group_parent)
            level_logo.setText('')
            level_logo.setPixmap(icon)
            level_logo.setMaximumSize(QtCore.QSize(16, 16))
            level_item = QtWidgets.QLabel(group_parent)
            level_item.setText(item)

            h_layout.addWidget(level_name, alignment=Qt.AlignRight)
            h_layout.addWidget(level_logo, alignment=Qt.AlignCenter)
            h_layout.addWidget(level_item, alignment=Qt.AlignLeft)
            # layout.addWidget(level)
            vertical_parent.addLayout(h_layout)

    #   Bottom Toolbars, option to launch the rendering and the log -----------
    def progress_bar_ui(self, value=0, total=100):
        """
        Setup the Progress Bar, give the maxime value and the value used.
        :param value: a Int value, this value give the statue about the bar
        :param total: another Int, give the maximum value
        :return:
        """
        # Setup the Progress bar with the data
        self.progressBar.setValue(value)
        self.progressBar.setMaximum(total)

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

    def value_connect(self, slider_object):
        slider_object.changedValue.connect(self.get_slider_value)

    # @pyqtSlot(value=int)
    # def get_progress_value(self, value):
    #     self.progressBar.setValue(value)

    def progress_built(self, value):
        self.value_slide.emit(value)
        # value = QtCore.pyqtSignal([int], ['ProgressValue'])
        print('+1 progress bar')
        print(self.progressBar.value())
        value = self.progressBar.value() + 1
        print(value)
        max_value = self.progressBar.maximum()
        print('Max > ', max_value)
        self.progressBar.setValue(value)

        if value == max_value:
            print('Rendering Finished')
            btn = QtWidgets.QDialogButtonBox
            self.buttonBox.button(btn.Ok).setEnabled(True)

    def stop_rendering(self):
        print('Stop Rendering')
        # self.swarm.stop()


class ThreadRendering(QtCore.QThread):
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
        # My Thread :) .
        print('Hello, i am a thread')

        self.sleep(4)

        for level in self.lvl_list:
            # if 'False' not in self.csv_data:
            #     cl = p4_checkout(self.lvl_list[0])
            swarm = build(level)
            while swarm:
                self.sleep(30)
                if swarm.pid in psutil.pids():
                    print('looping 30s | ', swarm.pid)

                else:
                    print('Update progress bar')
                    # self.value_progress()
                    count = self.lvl_list.index(level)
                    print('Progress Bar', count)
                    break

            # if QtWidgets.QAbstractButton.isChecked(self.submit):
            #     p4_submit(cl)

            print('End Looping')

    # def progress_built(self, value):
    #     self.value_slide.emit(value)

    # @pyqtSlot()
    # def stop(self):
    #     print('Abort the thread')
    #     self._running = False
    #     self.terminate()
