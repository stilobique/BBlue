import re
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from os import listdir
from os.path import join, dirname, basename, isdir, normpath

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject
from BatchLightUE4.Models.Setup import Setup
from BatchLightUE4.Models.Database import TableProgram
from BatchLightUE4.Controllers.Files import \
    file_save_project, file_open, load_generic


class DialSetupTab(QtWidgets.QDialog, Ui_DialogSetupProject):
    header1, header2 = range(2)

    def __init__(self):
        super(DialSetupTab, self).__init__()
        self.setupUi(self)

        self.settings = Setup()
        self.data = TableProgram()

        # All Tab setup, options are split inside many function
        # Tab Project setup ---------------------------------------------------
        #   Defined data needed -----------------------------------------------
        self.list_levels = QtGui.QStandardItemModel()

        #   Write all Slot and Connect ----------------------------------------
        self.field_setup()
        self.tab_project_setup()

        # Tab Network Setup ---------------------------------------------------
        # self.tab_network()

        # Tab Source Control Setup --------------------------------------------
        self.tab_source_control()

        # Setups Buttons
        box_btn = QtWidgets.QDialogButtonBox
        btn = self.buttonBox.button
        btn(box_btn.RestoreDefaults).clicked.connect(self.btn_restore)
        btn(box_btn.Save).clicked.connect(lambda: file_save_project(self))
        btn(box_btn.Open).clicked.connect(load_generic)
        btn(box_btn.Close).clicked.connect(self.close)

    # Ui Functions ------------------------------------------------------------
    #   Tab Project setup -----------------------------------------------------
    def tab_project_setup(self, index=None, value=str):
        """
        Generate the Tab Setup, include the Paths field and the Tree Levels
        with all editable data.
        It's only a function to add the slot and signal inside the Ui.

        :param index: None by default, this value give a Int to choice the
        field used, Unreal Editor (1) or the Project field (2).
        :param value: String data, it a simple information to send it a field
        :return:
        """
        if index:
            if index == 1:
                self.ue4_path_text.setText(value)
            elif index == 2:
                self.project_file_text.setText(value)
            elif index == 3:
                value = self.sub_folder_text.text()
                self.sub_folder_text.setText(value)
        elif self.settings.last_job_run():
            db = self.data.select_paths()
            self.ue4_path_text.setText(db[0][1])
            self.project_file_text.setText(db[0][2])
            self.sub_folder_text.setText(db[0][3])
            print(self.sub_folder_text.text())

        level_path = join(dirname(self.project_file_text.text()),
                          'Content',
                          self.sub_folder_text.text())

        root_model = self.model_base(self)
        self.ProjectTreeLevels.reset()
        self.ProjectTreeLevels.setModel(root_model)
        if self.project_file_text.text():
            data_tree = self.levels_list(level_path)
            self.model_populate(data_tree,
                                root_model.invisibleRootItem())
        self.ProjectTreeLevels.expandAll()
        self.ProjectTreeLevels.setColumnWidth(0, 250)
        self.ProjectTreeLevels.setSortingEnabled(True)
        self.ProjectTreeLevels.sortByColumn(0, Qt.AscendingOrder)
        root_model.itemChanged.connect(self.update_level)

        return self

    def field_setup(self):
        """Generate the fields and signal about all paths"""
        self.ue4_path_edit.clicked.connect(lambda: self.select_file(1))
        self.project_file_edit.clicked.connect(lambda: self.select_file(2))
        self.sub_folder_edit.clicked.connect(lambda: self.tab_project_setup(
            index=3))

    def levels_list(self, path):
        """
        Generate a list with all levels inside a path give than argument
        :param path: specify a path to scan the folder, it's a simple string
        :return: a dict with all levels and folder
        """
        folders = {}
        levels = []
        if isdir(path):
            for item in listdir(path):
                absolute_path = join(path, item)
                if isdir(absolute_path):
                    key = basename(dirname(absolute_path))
                    sub_levels = self.levels_list(absolute_path)
                    if len(sub_levels) and type(sub_levels) == dict:
                        levels.append(sub_levels)
                        folders[key] = levels
                else:
                    if '.umap' in item:
                        regex = r"^.*\Content"
                        folder = dirname(absolute_path)
                        absolute_path = normpath(absolute_path)
                        relative_path = re.sub(regex, '', folder)
                        levels.append(join(relative_path, item))
                        key = basename(dirname(absolute_path))
                        folders[key] = levels
        else:
            folders = {'No Data': 'Error Path'}

        return folders

    def update_level(self, index_item):
        """
        Function to save or remove the levels from the Data Base
        :param index_item: A string with the level name to save it.
        :return:
        """
        state = index_item.checkState()
        if state == Qt.Checked:
            info = [index_item.text(), 'Path', 1]
        else:
            info = [index_item.text(), 'Path', 0]

        self.data.write_data_levels(state=state, data=info)

    def model_populate(self, children, parent):
        """
        Function to work with the Model.
        You need to give 2 parameter, a dict with your Data you want show,
        and a parent to define the index.
        It's a recursive function, if your Data has a Dict inside a Dict,
        the function generate the Tree with all sub-node.
        :param children: It's only a Dict, included your Data
        :param parent: Define your first level, work with the Invisible Root
        :return: nothing returns.
        """
        for key, values in sorted(children.items()):
            item_object = QStandardItem(key)
            folder_icon = QtGui.QIcon()
            folder_icon.addPixmap(
                QtGui.QPixmap("Resources/Icons/file-submodule.png"))
            item_object.setIcon(folder_icon)
            parent.appendRow(item_object)

            if type(values) == list:
                for value in values:
                    if type(value) == str:
                        level_name = basename(value)
                        check = False
                        if self.settings.last_job_run():
                            if len(self.data.select_levels(name=level_name)):
                                check = 2
                        item_name = QStandardItem(level_name)
                        item_name.setCheckable(True)
                        item_name.setCheckState(check)
                        item_path = QStandardItem(value)
                        item_object.appendRow([item_name, item_path])
                    elif type(value) == dict:
                        self.model_populate(value, item_object)

    def model_base(self, parent):
        """
        Function to work with the Model.
        This function generate the Tree View base, with all header generate.
        :param parent: QTreeView
        :return: give a Model
        """
        model = QStandardItemModel(0, 2, parent)
        model.setHeaderData(self.header1, Qt.Horizontal, 'Names')
        model.setHeaderData(self.header2, Qt.Horizontal, 'Paths')

        return model

    def select_file(self, index):
        select = file_open(self, index)
        self.tab_project_setup(index, select[0])

    # Ui Functions ------------------------------------------------------------
    #   Tab Source Control ----------------------------------------------------
    def tab_source_control(self):
        """
        The Ui about the Source Control panel, all option and slot connect.
        :return:
        """
        soft_work = self.softwares_comboBox
        soft_work.currentIndexChanged.connect(self.sc_software)

    def sc_software(self):
        """
        Event on the Source control tab, activate or disable all fields about
        the option on this tab.
        :return:
        """
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
        """
        Function to restore the clean view.
        :return:
        """
        return print('Restore View')
