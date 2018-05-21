import re

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt
from os import listdir
from os.path import join, expanduser, dirname, normpath, basename, isdir

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject

from BatchLightUE4.Models.Setup import Setup
# from BatchLightUE4.Models.Database import TableProgram

from BatchLightUE4.Controllers.View_Setup import \
    setup_tab_paths, \
    setup_tab_paths_save


class DialSetupTab(QtWidgets.QDialog, Ui_DialogSetupProject):
    header1, header2, header3 = range(3)

    def __init__(self):
        super(DialSetupTab, self).__init__()
        self.setupUi(self)

        self.settings = Setup()

        # All Tab setup, options are split inside many function
        # Tab Project setup ---------------------------------------------------
        #   Defined data needed -----------------------------------------------
        self.paths_dict = {
            'unreal': self.ue4_path_text.text(),
            'project': self.project_file_text.text(),
            'folder': self.sub_folder_text.text(),
        }
        self.list_levels = QtGui.QStandardItemModel()

        #   Write all Slot and Connect ----------------------------------------
        self.ue4_path_edit.clicked.connect(lambda: self.btn_open(1))
        self.project_file_edit.clicked.connect(lambda: self.btn_open(2))
        self.sub_folder_edit.clicked.connect(
            lambda: self.tab_project_setup(
                self.paths_dict['unreal'],
                self.paths_dict['project']))
        # Don't work :-(
        self.sub_folder_text.returnPressed.connect(
            lambda: self.tab_project_setup(
                self.paths_dict['unreal'],
                self.paths_dict['project']))
        self.tab_project_setup()

        self.model = self.model_base(self)
        self.ProjectTreeLevels.setModel(self.model)

        # Tab Network Setup ---------------------------------------------------
        # self.tab_network()

        # Tab Source Control Setup --------------------------------------------
        self.tab_source_control()

        # Setups Buttons
        box_btn = QtWidgets.QDialogButtonBox
        btn = self.buttonBox.button
        btn(box_btn.RestoreDefaults).clicked.connect(self.btn_restore)
        btn(box_btn.Save).clicked.connect(self.btn_save)
        btn(box_btn.Open).clicked.connect(self.btn_open)
        btn(box_btn.Cancel).clicked.connect(self.close)

    # Ui Functions ------------------------------------------------------------
    #   Tab Project setup -----------------------------------------------------
    def tab_project_setup(self, unreal='', project=''):
        """
        Generate the Tab Setup, include the Paths field and the Tree Levels
        with all editable data.
        It's only a function to add the slot and signal inside the Ui.

        :param unreal: string with the editor path
        :param project: string with the 'uproject' file path
        :return:
        """
        folder = self.sub_folder_text.text()
        data = setup_tab_paths(unreal, project, folder)

        self.ue4_path_text.setText(data['editor'])
        self.project_file_text.setText(data['project'])
        if self.project_file_text.text():
            level_path = join(dirname(self.project_file_text.text()),
                              'Content',
                              self.sub_folder_text.text())

            self.tree_levels(self.model)

        return self

    #   Generate the Tree Levels ----------------------------------------------
    def tree_levels(self, model):
        # self.ProjectTreeLevels.reset()
        path = normpath(dirname(self.project_file_text.text()) + '/Content/')
        levels_list = self.levels_list(path)
        # levels_list = [x for x in levels_list if x != []]

        for name_object, root in levels_list:
            self.model_data(model, 'edit', name_object, root)

    def levels_list(self, path):
        """
        Generate a list with all levels inside a path give than argument
        :param path: specify a path to scan the folder
        :return: a list with all levels
        """
        levels = []
        for item in listdir(path):
            absolute_path = join(path, item)
            if isdir(absolute_path):
                sublevel = [(item, self.levels_list(absolute_path))]
                levels.extend(sublevel)
            else:
                if '.umap' in item:
                    sublevel = [(item, absolute_path)]
                    levels.extend(sublevel)

        return levels

    def model_base(self, parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.header1, Qt.Horizontal, 'Editable')
        model.setHeaderData(self.header2, Qt.Horizontal, 'Names')
        model.setHeaderData(self.header3, Qt.Horizontal, 'Paths')
        return model

    def model_data(self, model, editable, name, path):
        model.insertRow(0)
        model.setData(model.index(0, self.header1), editable)
        model.setData(model.index(0, self.header2), name)
        model.setData(model.index(0, self.header3), path)

    # Ui Functions ------------------------------------------------------------
    #   Tab Source Control ----------------------------------------------------
    def tab_source_control(self):
        soft_work = self.softwares_comboBox
        soft_work.currentIndexChanged.connect(self.sc_software)

    def sc_software(self):
        # Todo Use a loop with a children to change the statue
        if self.softwares_comboBox.currentText() == 'Disabled':
            self.path_sc_label.setDisabled(True)
            self.path_sc_text.setDisabled(True)
            self.path_sc_edit.setDisabled(True)
            self.user_label.setDisabled(True)
            self.user_text.setDisabled(True)
            self.password_label.setDisabled(True)
            self.password_text.setDisabled(True)

        else:
            self.path_sc_label.setDisabled(False)
            self.path_sc_text.setDisabled(False)
            self.path_sc_edit.setDisabled(False)
            self.user_text.setDisabled(False)
            self.user_label.setDisabled(False)
            self.password_text.setDisabled(False)
            self.password_label.setDisabled(False)

    # Buttons Box Function ----------------------------------------------------
    @staticmethod
    def btn_restore():
        return print('Restore View')

    def btn_save(self):
        description = 'Save your Project'
        file = '*.db'
        directory = join(expanduser('~'), 'BBLUE4')
        options = QtWidgets.QFileDialog.Options()
        popup = QtWidgets.QFileDialog()
        popup = popup.getSaveFileName(
            parent=self,
            directory=directory,
            caption=description,
            filter=file,
            options=options
        )

        # Write the setup file (.ini) with the last DB write.
        self.settings.last_job_add(popup[0])

        self.paths_dict['folder'] = self.sub_folder_text.text()
        setup_tab_paths_save(popup, self.paths_dict)
        # self.close()

    def btn_open(self, index):
        if index == 1:
            description = 'Select your Unreal Path'
            file = 'UE4Editor.exe'
            key_value = 'unreal'
        elif index == 2:
            description = 'Select your Project file'
            file = '*.uproject'
            key_value = 'project'
        else:
            description = 'Load a project generate with BBlue'
            file = '*.db'
            key_value = 'folder'

        popup = self.load(description, file)
        self.paths_dict[key_value] = popup[0]
        self.tab_project_setup(
            unreal=self.paths_dict['unreal'],
            project=self.paths_dict['project'],
        )

        return self

    def load(self, description, file):
        """
        This function generate a popup to load a file, it's to take a string
        path and all data returns is the Path and the file name.
        :param description: this field give the dialogue name
        :param file: use it to specify a type file (.png, .db...)
        :return: a tuple with the path and the file name
        """
        options = QtWidgets.QFileDialog.Options()
        popup = QtWidgets.QFileDialog()
        popup = popup.getOpenFileName(
            parent=self,
            caption=description,
            filter=file,
            options=options
        )

        return popup
