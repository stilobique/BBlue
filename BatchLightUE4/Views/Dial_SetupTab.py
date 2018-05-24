from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from os import listdir
from os.path import join, dirname, basename, isdir

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject
from BatchLightUE4.Models.Setup import Setup
from BatchLightUE4.Models.Database import TableProgram
# from BatchLightUE4.Controllers.View_Setup import setup_tab_paths
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
        self.ue4_path_edit.clicked.connect(lambda: file_open(self, 1))
        self.project_file_edit.clicked.connect(lambda: file_open(self, 2))
        self.sub_folder_edit.clicked.connect(self.tab_project_setup)
        self.sub_folder_text.returnPressed.connect(self.tab_project_setup)
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

        :return:
        """
        if self.settings.last_job_run():
            db = self.data.select_paths()
            self.ue4_path_text.setText(db[0][1])
            self.project_file_text.setText(db[0][2])
            self.sub_folder_text.setText(db[0][3])

        elif index:
            if index == 1:
                self.ue4_path_text.setText(value)
            elif index == 2:
                self.project_file_text.setText(value)
        else:
            print('Clean Value')

        level_path = join(dirname(self.project_file_text.text()),
                          'Content',
                          self.sub_folder_text.text())

        root_model = self.model_base(self)
        self.ProjectTreeLevels.setModel(root_model)
        if self.project_file_text.text():
            data_tree = self.levels_list(level_path)
            self.model_populate(data_tree,
                                root_model.invisibleRootItem())
        self.ProjectTreeLevels.expandAll()
        self.ProjectTreeLevels.setColumnWidth(0, 300)
        self.ProjectTreeLevels.clicked.connect(self.update_level)

        return self

    def levels_list(self, path):
        """
        Generate a list with all levels inside a path give than argument
        :param path: specify a path to scan the folder
        :return: a dict with all levels and folder
        """
        folders = {}
        levels = []
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
                    levels.append(item)
                    key = basename(dirname(absolute_path))
                    folders[key] = levels

        return folders

    def update_level(self, level_name=''):
        """
        Function to save or remove the levels from the Data Base
        :param level_name: A string with the level name to save it.
        :return:
        """
        print('hi')
        print(level_name)
        self.data.write_data_levels()

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
                        sub_item = QStandardItem(value)
                        sub_item.setCheckable(True)
                        item_object.appendRow(sub_item)
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
        """
        Function to restore the clean view.
        :return:
        """
        return print('Restore View')
