import os
import re

from os.path import normpath, abspath, dirname

import perforce
from ..Models.Database import TableProgram


# -----------------------------
# Connect to Perfoce to check all map (and lvl .uasset)
# -----------------------------
def p4_checkout(level_used):
    """
    Checkout all levels on a folder
    :param level_used:
    :return:
    """
    print('Generate a Changing List')
    data = TableProgram()
    data_levels = data.select_levels(name=level_used)
    path_level = data_levels[0][2]

    project_path = data.select_paths()
    project_path = dirname(project_path[0][2])
    abs_path = normpath(project_path + '/Content/' + path_level)

    regex = r"^.*Perforce"
    rel_path = re.sub(regex, '', abs_path)
    depot = dirname(abs_path)

    p4 = perforce.connect()
    revisions = []

    for filename in os.listdir(depot):
        rel_path = rel_path.replace('\\', '/')
        file = r"/" + dirname(rel_path) + r"/" + filename
        if '.uasset' or '.umap' in file:
            revisions.append(file)

    level_used = level_used.replace('.umap', '')
    description = ("""[ProVolley][GFX][LightmapAuto] Automatic Build """
                   """Lightmap generate for the level """ + level_used)
    cl = p4.findChangelist(description)

    for i in range(len(revisions)):
        p4.ls(revisions[i])
        cl.append(revisions[i])

    revisions.clear()

    return cl


def p4_submit(cl):
    cl.submit()
