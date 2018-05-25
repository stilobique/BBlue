from PyQt5.QtWidgets import QFileDialog
from os.path import join, expanduser
from BatchLightUE4.Controllers.View_Setup import setup_tab_paths_save


def file_save_project(self, close=None):
    """
    Function to save a Project (a .db file at the moment).

    :param self: need to keep all data, paths, sc... and more.
    :param close: a Boolean option for close the Windows, optional setup
    :return:
    """
    description = 'Save your Project'
    file = '*.db'
    directory = join(expanduser('~'), 'BBLUE4')
    options = QFileDialog.Options()
    popup = QFileDialog()
    popup = popup.getSaveFileName(
        parent=self,
        directory=directory,
        caption=description,
        filter=file,
        options=options
    )

    # Write the setup file (.ini) with the last DB write.
    self.settings.last_job_add(popup[0])

    dict_path = {
        'unreal': self.ue4_path_text.text(),
        'project': self.project_file_text.text(),
        'folder': self.sub_folder_text.text()
    }
    setup_tab_paths_save(dict_path)

    if close:
        self.close()


def file_open(self, index):
    """
    Popup to select a file.

    :param self: a 'parent' parameter, need to find all data.
    :param index: this index (a Int) give an info to specify the type file
    desired and the description.
    :return:
    """
    if index == 1:
        description = 'Select your Unreal Path'
        file = 'UE4Editor.exe'
    elif index == 2:
        description = 'Select your Project file'
        file = '*.uproject'
    else:
        description = 'Load a project generate with BBlue'
        file = '*.db'

    popup = load_generic(self, description, file)

    return popup


def load_generic(self, description, file):
    """
    This function generate a popup to load a file, it's to take a string
    path and all data returns is the Path and the file name.

    :param self: windows data, needed to keep information
    :param description: this field give the dialogue name
    :param file: use it to specify a type file (.png, .db...)
    :return: a tuple with the path and the file name
    """
    options = QFileDialog.Options()
    popup = QFileDialog()
    popup = popup.getOpenFileName(
        parent=self,
        caption=description,
        filter=file,
        options=options
    )

    return popup
