import sys

from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication

from BatchLightUE4.Views.MainWindows import MainWindows

# Add option to the Debug mode
if 'pydevd' in sys.modules:
    import pydevd
    pydevd.settrace('192.168.2.93', port=22,
                    stdoutToServer=True, stderrToServer=True)

app_info = 'B-BLUE4'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindows()
    app.setWindowIcon(QtGui.QIcon('Resources/Icons/light-bulb.png'))
    w.setWindowTitle(app_info)
    w.show()

    sys.exit(app.exec_())
