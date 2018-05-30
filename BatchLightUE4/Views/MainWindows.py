import perforce

from os.path import basename, dirname
from PyQt5 import QtWidgets

# Adding all view used
from BatchLightUE4.Views.Dial_About import DialViewAbout
from BatchLightUE4.Views.Dial_LogTools import DialLogTools
from BatchLightUE4.Views.Dial_Rendering import DialRendering
from BatchLightUE4.Views.Dial_SetupTab import DialSetupTab
from BatchLightUE4.Views.MainWindows_convert import Ui_MainWindow
# Adding Data Base utils
from BatchLightUE4.Models.Database import TableProgram

# Adding all Operator used
from BatchLightUE4.Models.Setup import Setup
from BatchLightUE4.Controllers.Swarm import swarm_setup
from BatchLightUE4.Controllers.Files import load_generic, popup_msg

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

        # Generate all variable needed with this window
        self.settings = Setup()
        self.data = TableProgram()
        self.job = self.settings.last_job_run()

        if self.job:
            self.csv = self.data.select_scv()

        self.checkBoxLevels = {}

        self.menu_setup()
        self.levels_tools()
        self.levels_generate()
        self.bottom_tools()

    # Ui Function -------------------------------------------------------------
    #   File Menu setup -------------------------------------------------------
    def menu_setup(self):
        """
        Function to setup all connection an signal inside the File Menu bar.
        :return:
        """
        # File Menu
        self.actionNew_Setup.triggered.connect(self.dial_setup_project)
        open_project = self.actionLoad_Lastproject
        open_project.triggered.connect(lambda: load_generic(self,
                                                            'Open Project',
                                                            '*.db'))

        # Setup Menu
        self.actionProject.triggered.connect(self.dial_setup_project)
        self.actionNetworks.triggered.connect(lambda:
                                              self.dial_setup_project(2))
        self.actionCSV.triggered.connect(lambda:
                                         self.dial_setup_project(1))

        # Log Menu
        self.actionShow_log_folder.triggered.connect(self.dialogue_log)
        self.actionClean_Log.triggered.connect(self.dialogue_log)

        # Help Menu
        self.actionAbout.triggered.connect(self.dialogue_help)
        self.actionShortcut.triggered.connect(lambda: self.dialogue_help(1))

    # Ui Function -------------------------------------------------------------
    #   Toolbars and function about the levels --------------------------------
    def levels_tools(self):
        """
        Function to setup the tools about the levels, add all signal used.
        :return:
        """
        self.pushLevelsSelect.clicked.connect(lambda: self.select_level(2))
        self.pushLevelsDeselect.clicked.connect(self.select_level)
        self.toolLevelsEdit.clicked.connect(self.dial_setup_project)

    def levels_generate(self):
        """
        Function to draw all levels setup with this project.
        :return:
        """
        # Generate all Checkbox Levels.
        if self.job:
            levels = self.data.select_levels()
            level_checkbox = self.data.select_levels(state=2)
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

    # Ui Function -------------------------------------------------------------
    #   Bottom Toolbars, option to launch the rendering and the log -----------
    def bottom_tools(self):
        """
        Function to add signal on the bottom toolbars.
        :return:
        """
        self.pushToolsBuils.clicked.connect(self.view_rendering)
        self.pushToolsBuils.setToolTip(self.pushToolsBuils.statusTip())

    # Window Call -------------------------------------------------------------
    #   Tab Setup dialogue ---------------------------------------------------
    def dial_setup_project(self, index):
        """
        Function to show the dialogue 'Setup Tab', when it's close the
        function 'levels_generate' is rebuilt.
        :param index: A simple index to select the Tab opened.
        :return:
        """
        ui_setup_tab = DialSetupTab()
        ui_setup_tab.tabWidget.setCurrentIndex(index)

        ui_setup_tab.show()
        rsp = ui_setup_tab.exec_()

        if rsp == QtWidgets.QDialog.Rejected:
            layout_levels = self.allLevelsCheck
            for item in reversed(range(layout_levels.count())):
                delete_item = layout_levels.itemAt(item).widget()
                layout_levels.removeWidget(delete_item)
                delete_item.setParent(None)
            self.levels_generate()

    # Old, refactoring function -----------------------------------------------
    def dialogue_log(self):
        """
        A simple function to show the Windows Log with all option
        :return:
        """
        dialog_log = DialLogTools(self)
        dialog_log.show()

    def dialogue_help(self, index):
        """
        Function to show the dialogue 'Help'.

        :param index: A simple index to select the Tab opened.
        :return:
        """
        dialog_help = DialViewAbout(self)
        dialog_help.show()
        dialog_help.tabWidget.setCurrentIndex(index)

    def select_level(self, state=0):
        """
        Evvent to select or deselect all levels,
        :param state: return the state checkbox, 0 to off, 1 to be
        semi-push and 2 to be check
        :return:
        """
        for key, value in self.checkBoxLevels.items():
            btn = self.checkBoxLevels[key]
            if QtWidgets.QAbstractButton.isEnabled(btn):
                btn.setCheckState(state)

    def view_rendering(self):
        """
        Event to launch the rendering windows and all build -check the
        swarm, the source control used... and more.
        :return:
        """
        lvl_rendering = []

        for key, value in self.checkBoxLevels.items():
            btn = self.checkBoxLevels[key]
            if QtWidgets.QAbstractButton.isChecked(btn):
                lvl_rendering.append(key)

        if len(lvl_rendering) == 0:
            message = 'No level selected !'
            popup_msg(self, 'information', 'Error', message)

        else:
            message = 'Launch the rendering ?'
            reply = popup_msg(self, 'question', 'Rendering', message)
            lvl_rendering.sort()

            if reply.Yes:
                machines = self.checkBoxMachines
                swarm_setup(QtWidgets.QAbstractButton.isChecked(machines))
                submit = self.checkBoxSubmit

                dial_rendering = DialRendering(self,
                                               lvl_list=lvl_rendering,
                                               csv=False,
                                               submit=submit)
                dial_rendering.show()
                rsp = dial_rendering.exec_()

                if rsp == QtWidgets.QDialog.Accepted:
                    print('Rendering Validate')
                    swarm_setup(False)
                    message = 'Level Build'

            else:
                message = 'Rendering abort.'

        self.statusbar.showMessage(message)
