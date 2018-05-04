from PyQt5 import QtWidgets

from BatchLightUE4.Views.Dial_About_convert import Ui_Help

from BatchLightUE4.Controllers.Setup import Setup


class DialViewAbout(QtWidgets.QDialog, Ui_Help):
    """This widget contains all help tabs ; information about number
    version, release and licence, and all shortcut inside the program."""
    def __init__(self, parent=None):
        super(DialViewAbout, self).__init__(parent)
        self.setupUi(self)

        self.data = Setup()

        # Version Panel
        self.lineEdit.setText(self.data.number)
        url_icons = self.label_url_octicons
        url_website = self.label_url_website
        url_icons.setText('''<a 
        href='https://octicons.github.com/'>Github's Icons - Octicons</a>''')
        url_website.setText('''<a 
        href='https://github.com/stilobique/BatchBuildLightUE4/'>Github 
        Depot</a>''')

        self.pushButtonClose.clicked.connect(self.close)
