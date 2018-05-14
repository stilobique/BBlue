from os.path import isfile

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject
from BatchLightUE4.Models.Setup import Setup
from BatchLightUE4.Models.Database import TableProgram


"""
All function to work between the View Setup Tab and the Data Base.
"""


def setup_tab_paths():
    view_tab = Ui_DialogSetupProject()
    data = TableProgram()
    paths_field = {
        'editor': '',
        'project': '',
        'folder': '',
        'name': ''
    }

    setup = Setup()
    if isfile(setup.last_job_run()):
        print('Use the last job')
        paths_data = data.select_paths(1)
        paths_data = paths_data[0]
        paths_field['editor'] = paths_data[1]
        paths_field['project'] = paths_data[2]
        paths_field['folder'] = paths_data[3]

    return paths_field
