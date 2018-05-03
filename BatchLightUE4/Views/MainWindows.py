import perforce
import psutil

from os.path import join, isdir, expanduser, basename, dirname
from PyQt5 import QtWidgets, QtGui, QtCore

from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal

# Adding all view used
from BatchLightUE4.Views.WindowsMainWindows import Ui_MainWindow
from BatchLightUE4.Views.Dial_SetupTab import DialSetupTab
from BatchLightUE4.Views.WindowsHelpView import Ui_Help
from BatchLightUE4.Views.WindowsLogView import Ui_DialogLog
from BatchLightUE4.Views.WindowsRendering import Ui_Rendering

# Adding Data Base utils
from BatchLightUE4.Models.Database import TableProgram

# Adding all Operator used
from BatchLightUE4.Controllers.Perfoce import \
    p4_checkout, p4_submit
from BatchLightUE4.Controllers.Project import project_name
from BatchLightUE4.Controllers.Setup import Setup
from BatchLightUE4.Controllers.Swarm import build, swarm_setup

# TODO Add a check if an UE version has launch

"""
This page control all views generate with Qt-Designer, to make an update or 
change something about the UI, update the .ui and generate a news .py.
"""


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


class ViewRendering(QtWidgets.QDialog, Ui_Rendering):
    """Rendering Dialog Box."""
    value_slide = pyqtSignal(int)

    def __init__(self, parent, lvl_list, csv='False', submit=False):
        """lvl_list: list with all level rendering.
        csv: data with the CSV used (booelan or list)"""
        super(ViewRendering, self).__init__(parent)
        self.setupUi(self)

        # TODO Split the rendering process on a another thread.
        # Je setup ma progress bar avec les data de base
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

    # def progress_built(self, value):
    #     self.value_slide.emit(value)
        # # value = QtCore.pyqtSignal([int], ['ProgressValue'])
        # print('+1 progress bar')
        # print(self.progressBar.value())
        # value = self.progressBar.value() + 1
        # print(value)
        # max_value = self.progressBar.maximum()
        # print('Max > ', max_value)
        # self.progressBar.setValue(value)
        #
        # if value == max_value:
        #     print('Rendering Finished')
        #     btn = QtWidgets.QDialogButtonBox
        #     self.buttonBox.button(btn.Ok).setEnabled(True)


class LogView(QtWidgets.QDialog, Ui_DialogLog):
    """Log Panel"""
    def __init__(self, parent=None):
        super(LogView, self).__init__(parent)
        self.setupUi(self)

        print('Windows Log Show')


class ViewTabHelp(QtWidgets.QDialog, Ui_Help):
    """This widget contains all help tabs ; information about number
    version, release and licence, and all shortcut inside the program."""
    def __init__(self, parent=None):
        super(ViewTabHelp, self).__init__(parent)
        self.setupUi(self)

        self.data = Setup()

        # Version Panel
        self.lineEdit.setText(self.data.number)
        url_octi = self.label_url_octicons
        url_website = self.label_url_website
        url_octi.setText('''<a 
        href='https://octicons.github.com/'>Github's Icons - Octicons</a>''')
        url_website.setText('''<a 
        href='https://github.com/stilobique/BatchBuildLightUE4/'>Github 
        Depot</a>''')

        self.pushButtonClose.clicked.connect(self.close)


class MainWindows(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        """
        Main Window, principal view, this windows can show all level,
        access on many option -path setup, network, log...
        """
        super(MainWindows, self).__init__(parent)
        self.setupUi(self)
        # Setup settings base

        self.data = Setup()
        self.job = self.data.last_job_run()
        self.checkBoxLevels = {}

        self.FileMenuSetup()
        self.LevelsTools()
        self.LevelsGenerate()
        self.BottomTools()

    # -------------
    # UI Function
    def FileMenuSetup(self):
        # Triggered Menu
        #     File Menu
        self.actionNew_Setup.triggered.connect(self.project_new)
        self.actionLoad_Lastproject.triggered.connect(self.open_save)

        #    Setup and Option Menu
        self.actionProject.triggered.connect(self.dial_setup_project)
        self.actionNetworks.triggered.connect(lambda:
                                              self.dial_setup_project(2))
        self.actionCSV.triggered.connect(lambda:
                                         self.dial_setup_project(3))

        #   Log Panel
        self.actionShow_log_folder.triggered.connect(self.view_log)
        self.actionClean_Log.triggered.connect(self.view_log)

        #   Help Tab
        self.actionAbout.triggered.connect(self.view_help)
        self.actionShortcut.triggered.connect(lambda: self.view_help(1))

    def LevelsTools(self):
        self.pushLevelsSelect.clicked.connect(lambda: self.select_level(True))
        self.pushLevelsDeselect.clicked.connect(self.select_level)
        self.toolLevelsEdit.clicked.connect(self.dial_setup_project)

    def LevelsGenerate(self):
        # Generate all Checkbox Levels.
        if self.job:
            self.data = TableProgram()
            levels = self.data.select_levels()
            level_checkbox = self.data.select_levels(state=2)
            self.csv = self.data.csv_data()
            i = 0
            while i < len(level_checkbox):
                key = level_checkbox[i][1]
                key_folder = basename(dirname(level_checkbox[i][2]))
                self.checkBoxLevels[key] = QtWidgets.QCheckBox(key)
                self.checkBoxLevels[key].setObjectName(key)
                csv_value = self.csv[0]
                if csv_value != str('False'):
                    # TODO Add a progress bar, the the soft check many levels
                    #  the request can be long.
                    for level_name in levels:
                        if key_folder in level_name[2]:
                            p4 = perforce.connect()
                            filename = perforce.Revision(p4, level_name[2])

                            if 'otherOpen' in filename._p4dict:
                                bubble_msg = filename._p4dict.get('otherOpen0')
                                tooltip = bubble_msg
                                self.checkBoxLevels[key].setToolTip(tooltip)
                                self.checkBoxLevels[key].setEnabled(False)

                self.allLevelsCheck.addWidget(self.checkBoxLevels[key])
                self.allLevelsCheck.contentsMargins()
                i = i + 1

            if 'False' not in self.csv[0]:
                self.checkBoxSubmit.setEnabled(True)

    def BottomTools(self):
        self.pushToolsBuils.clicked.connect(self.view_rendering)
        self.pushToolsBuils.setToolTip(self.pushToolsBuils.statusTip())

    # -------------
    # File Menu Events
    def open_save(self, state):
        # TODO Proof of concept, no object has setup
        if state == 1:
            self.str_debug = 'First Value'
            self.file_setup = filter="Project (*.db)"
        else:
            self.str_debug = 'Pas de status, basique way'
            self.file_setup = filter="Project (*.db)"

        (filename, filter) = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Open a previous project',
            self.file_setup)

    def project_new(self):
        """
        This action open the Windows Setup with all empty field. The don't
        return object.
        """
        dialog_setup = ViewTabSetup()
        dialog_setup.show()
        dialog_setup.new = True
        dialog_setup.setCurrentIndex(0)

    @staticmethod
    def dial_setup_project(index):
        ui_setup_tab = DialSetupTab()
        ui_setup_tab.tabWidget.setCurrentIndex(index)

        ui_setup_tab.show()
        rsp = ui_setup_tab.exec_()

        if rsp == QtWidgets.QDialog.Accepted:
            print('Project Saved')

        elif rsp == QtWidgets.QDialog.Rejected:
            print('Rejected !')
        else:
            print('Error, nothing ??')

    def view_log(self):
        dialog_log = LogView(self)
        dialog_log.show()

    def view_help(self, index):
        dialog_help = ViewTabHelp(self)
        dialog_help.show()
        dialog_help.tabWidget.setCurrentIndex(index)

    # -------------
    # Events
    def select_level(self, state):
        boolean = False
        if state:
            boolean = 2

        data = self.checkBoxLevels
        for key, value in data.items():
            btn = self.checkBoxLevels[key]
            if QtWidgets.QAbstractButton.isEnabled(btn):
                btn.setCheckState(boolean)

    def view_rendering(self):
        lvl_rendering = []
        level_count = 0

        for key, value in self.checkBoxLevels.items():
            btn = self.checkBoxLevels[key]
            if QtWidgets.QAbstractButton.isChecked(btn):
                lvl_rendering.append(key)
                level_count = len(lvl_rendering)

        # Check si je peut faire un build (More than 1 levels selected ?
        # -> Non, abort rendering
        # -> Oui, je lance mon thread et ma progress bar.

        if level_count == 0:
            msg = 'No level(s) selected !'
            QMessageBox.information(self, 'Information', msg)

        else:
            text = 'Launch the rendering ?'
            reply = QMessageBox.question(self, 'Rendering', text)
            lvl_rendering.sort()

            if reply == QMessageBox.Yes:
                machines = self.checkBoxMachines
                swarm_setup(QtWidgets.QAbstractButton.isChecked(machines))
                submit = self.checkBoxSubmit

                ViewRendering(self,
                              lvl_rendering,
                              self.csv[0],
                              submit).show()

                swarm_setup(False)
                msg = 'Level Build'

            else:
                msg = 'Rendering abort.'

        self.statusbar.showMessage(msg)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindows()
    app.exec_()
