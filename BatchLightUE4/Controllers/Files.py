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
