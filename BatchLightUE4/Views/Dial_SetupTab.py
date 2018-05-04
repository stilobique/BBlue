from PyQt5 import QtWidgets
from os.path import join, expanduser

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject

from BatchLightUE4.Models.Setup import Setup
from BatchLightUE4.Models.Database import TableProgram


class DialSetupTab(QtWidgets.QDialog, Ui_DialogSetupProject):
    def __init__(self):
        super(DialSetupTab, self).__init__()
        self.setupUi(self)

        # Defined all Data and Variable use
        self.all_path = {
            'unreal': self.ue4_path_text.text(),
            'game': self.project_file_text.text(),
            'folder': self.sub_folder_text.text(),
            'name': self.project_name_text.text()
        }

        self.settings = Setup()
        self.database = TableProgram()
        # self.job = self.data.last_job_run()

        # All Tab setup, options are split inside many function
        # Tab Project setup ---------------------------------------------------
        self.ue4_path_edit.clicked.connect(lambda: self.btn_open(1))
        self.project_file_edit.clicked.connect(lambda: self.btn_open(2))
        self.tab_project_setup()

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
    def tab_project_setup(self, unreal='', game='', folder='', name=''):
        self.ue4_path_text.setText(unreal)
        self.project_file_text.setText(game)
        self.sub_folder_text.setText(folder)
        self.project_name_text.setText(name)

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
        popup = QtWidgets.QFileDialog.getSaveFileName(
            parent=self,
            directory=directory,
            caption=description,
            filter=file,
        )

        # Write the setup file (.ini) with the last DB write.
        self.settings.last_job_add(popup[0])

        # Write the .db file
        self.database.write_data_path(
            self.all_path.get('unreal'),
            self.all_path.get('game'),
            self.all_path.get('folder'))
        self.close()

    def btn_open(self, index):
        if index == 1:
            description = 'Select your Unreal Path'
            file = 'UE4Editor.exe'
            key_value = 'unreal'
        elif index == 2:
            description = 'Select your Project file'
            file = '*.uproject'
            key_value = 'game'
        else:
            description = 'Load a project generate with BBlue'
            file = '*.db'
            key_value = 'other'

        popup = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption=description,
            filter=file,
        )

        self.all_path[key_value] = popup[0]

        return self.tab_project_setup(
            self.all_path.get('unreal'),
            self.all_path.get('game'))
