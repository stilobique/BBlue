"""Generate a Packages with the update version, launch this file and follow
all indication."""

# 1/ Check the number version -> Valid
# 2/ Propose a news number version -> Valid
# 3/ Edit the INI file and pack-it -> Valid
# 4/ Upload on Github :) .

import subprocess
import fileinput
import re

from os.path import dirname, join
from BatchLightUE4.Controllers.Setup import Setup

# All Variable
init = Setup()
setup_file = join(
    'E:\WORKS\Git\BatchBuildLightUE4\BatchLightUE4\Controllers\Setup.py')
# str_find = re.search('number = \'\' ', setup_file)
package = dirname(__file__) + '/packages.bat'

print('Actual Version : ', init.version())
nbr_version = input('Number Version : ')

with fileinput.FileInput(setup_file, inplace=True) as file:
    for line in file:
        # print(re.search(r"number = '(.)*'", 'wesh = ', line.rstrip()))
        str_old = r"number = '" + init.version() + "'"
        str_new = r"number = '" + nbr_version + "'"
        print(line.rstrip().replace(str_old, str_new))

init.version(update=nbr_version)

subprocess.call(package)
