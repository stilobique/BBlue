from os.path import isfile

from BatchLightUE4.Views.Dial_SetupTab_convert import Ui_DialogSetupProject
from BatchLightUE4.Models.Setup import Setup
from BatchLightUE4.Models.Database import TableProgram


"""
All function to work between the View Setup Tab and the Data Base.
"""


def setup_tab_paths(unreal, project, folder, update=False):
    view_tab = Ui_DialogSetupProject()
    data = TableProgram()
    setup = Setup()

    paths_field = {
        'editor': unreal,
        'project': project,
        'folder': folder,
        'name': ''
    }

    print('Check the data')

    if isfile(setup.last_job_run()):
        print('Use the last job')
        paths_data = data.select_paths(1)
        print(paths_data)
    #     paths_data = paths_data[0]
    #     paths_field['editor'] = paths_data[1]
    #     paths_field['project'] = paths_data[2]
    #     paths_field['folder'] = paths_data[3]

    return paths_field


def setup_tab_paths_save(file, paths):
    """
    Function to generate or update the database file.
    :param file: tuple with the path file and file format
    :param paths: dict fill with all paths

    :return: return a success or an error
    """
    print('Make a new or rewrite file')
    print('Path >> ', file[0])
    print('All paths >> ', paths)

    data = TableProgram()
    data.write_data_path(paths['unreal'], paths['project'], paths['folder'])

    return 'Data Save'
