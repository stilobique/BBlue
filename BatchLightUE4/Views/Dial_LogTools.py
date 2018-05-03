from PyQt5 import QtWidgets

from BatchLightUE4.Views.Dial_LogTools_convert import Ui_DialogLog


class Dial_Log_Tools(QtWidgets.QDialog, Ui_DialogLog):
    """Log Panel"""
    def __init__(self, parent=None):
        super(LogView, self).__init__(parent)
        self.setupUi(self)

        print('Windows Log Show')