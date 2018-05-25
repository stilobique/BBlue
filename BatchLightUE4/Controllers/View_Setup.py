from os import listdir
from os.path import isfile, isdir, join, dirname, normpath

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

    if isfile(setup.last_job_run()):
        paths_data = data.select_paths()
    #     paths_data = paths_data[0]
    #     paths_field['editor'] = paths_data[1]
    #     paths_field['project'] = paths_data[2]
    #     paths_field['folder'] = paths_data[3]

    return paths_field


def setup_tab_paths_save(paths):
    """
    Function to generate or update the database file.
    :param file: tuple with the path file and file format
    :param paths: dict fill with all paths

    :return: return a success or an error
    """

    data = TableProgram()
    data.write_data_path(paths['unreal'], paths['project'], paths['folder'])
    # generate_levels(paths['project'], paths['folder'])
    # data.write_data_levels()

    return 'Data Save'


def generate_levels(project, subfolder):
    """
    Generate a dict with all levels to save it on your database
    :param project: a simple string with the path to search all levels
    :param subfolder: subfolder with the levels paths
    :return:
    """

    path = join(dirname(project), 'Content', subfolder)
    path = normpath(path)
    levels = []

    for item in listdir(path):
        abs_path = join(path, item)
        if isdir(abs_path):
            sublevel = [(item, generate_levels(abs_path, ''))]
            levels.extend(sublevel)

        else:
            if '.umap' in item:
                sublevel = [(item, [])]
                levels.extend(sublevel)

    print(levels)

    return levels
