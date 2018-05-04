import perforce

from os.path import basename, dirname
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMessageBox

# Adding all view used
from BatchLightUE4.Views.Dial_About import DialViewAbout
from BatchLightUE4.Views.Dial_LogTools import DialLogTools
from BatchLightUE4.Views.Dial_Rendering import DialRendering
from BatchLightUE4.Views.Dial_SetupTab import DialSetupTab
from BatchLightUE4.Views.MainWindows_convert import Ui_MainWindow
# Adding Data Base utils
from BatchLightUE4.Models.Database import TableProgram

# Adding all Operator used
from BatchLightUE4.Controllers.Setup import Setup
from BatchLightUE4.Controllers.Swarm import swarm_setup

# TODO Add a check if an UE version has launch

"""
This page control all views generate with Qt-Designer, to make an update or 
change something about the UI, update the .ui and generate a news .py.
"""


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

        self.file_menu_setup()
        self.levels_tools()
        self.levels_generate()
        self.bottom_tools()

    # -------------
    # UI Function
    def file_menu_setup(self):
        # Triggered Menu
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

    def levels_tools(self):
        self.pushLevelsSelect.clicked.connect(lambda: self.select_level(True))
        self.pushLevelsDeselect.clicked.connect(self.select_level)
        self.toolLevelsEdit.clicked.connect(self.dial_setup_project)

    def levels_generate(self):
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

    def bottom_tools(self):
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

        return print('New Project, empty Setup')

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
        dialog_log = DialLogTools(self)
        dialog_log.show()

    def view_help(self, index):
        dialog_help = DialViewAbout(self)
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

                DialRendering(self,
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
