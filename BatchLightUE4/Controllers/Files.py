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

    self.paths_dict['folder'] = self.sub_folder_text.text()
    setup_tab_paths_save(popup, self.paths_dict)

    if close:
        self.close()


def file_open(self, index):
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

    popup = load_generic(self, description, file)
    self.paths_dict[key_value] = popup[0]
    self.tab_project_setup(
        unreal=self.paths_dict['unreal'],
        project=self.paths_dict['project'],
    )

    return self


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
