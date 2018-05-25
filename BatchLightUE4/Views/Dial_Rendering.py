import psutil

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal

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

        # TODO Split the rendering process on a another thread.
        # Setup the Progress bar with the data
        self.progressBar.setMaximum(len(lvl_list))
        self.progressBar.setValue(0)
        btn = QtWidgets.QDialogButtonBox
        self.buttonBox.button(btn.Ok).setEnabled(False)
        self.swarm = ThreadRendering(lvl_list, csv, submit)
        self.progressBar.valueChanged.connect(self.progress_built)
        self.swarm.start()

    def value_connect(self, slider_object):
        slider_object.changedValue.connect(self.get_slider_value)

    @pyqtSlot(int)
    def get_progress_value(self, value):
        self.progressBar.setValue(value)

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


class ThreadRendering(QtCore.QThread):
    def __init__(self, level_rendering, csv, submit):
        """
        This Class use the building operator in a separated thread, without
        this class the program freeze when a built it.

        :param level_rendering: A level list we want build it
        :type level_rendering: list
        :param csv: infomartion about the CSV used (False or other)
        :type csv: String
        :param submit: Info if the instance need to submit the rendering
        :type submit: bool
        """
        QtCore.QThread.__init__(self)
        self.lvl_list = level_rendering
        self.csv_data = csv
        self.submit = submit

    def __del__(self):
        self.wait()

    def run(self):
        # My Thread :) .
        print('Hello, i am a thread')

        self.sleep(4)

        for level in self.lvl_list:
            if 'False' not in self.csv_data:
                cl = p4_checkout(self.lvl_list[0])
            swarm = build(level)
            while swarm:
                self.sleep(30)
                if swarm.pid in psutil.pids():
                    print('looping 30s | ', swarm.pid)

                else:
                    print('Update progress bar')
                    self.value_progress()
                    break

            if QtWidgets.QAbstractButton.isChecked(self.submit):
                p4_submit(cl)

            print('End Looping')

    def progress_built(self, value):
        self.value_slide.emit(value)
