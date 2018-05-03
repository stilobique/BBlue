from PyQt5 import QtWidgets

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject


class DialSetupTab(QtWidgets.QDialog, Ui_DialogSetupProject):
    def __init__(self):
        super(DialSetupTab, self).__init__()
        self.setupUi(self)

        # self.data = Setup()
        # self.job = self.data.last_job_run()

        # All Tab setup, options are split inside many function
        # self.tab_project()
        # self.tab_network()
        # self.tab_source_control()

        # Gestion and button setup
        box_btn = QtWidgets.QDialogButtonBox
        btn = self.buttonBox.button
        btn(box_btn.RestoreDefaults).clicked.connect(self.btn_restore)
        btn(box_btn.Save).clicked.connect(self.btn_save)
        btn(box_btn.Open).clicked.connect(self.btn_open)
        btn(box_btn.Cancel).clicked.connect(self.close)
