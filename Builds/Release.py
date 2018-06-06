"""Generate a Packages with the update version, launch this file and follow
all indication."""

# 1/ Check the number version -> Valid
# 2/ Propose a news number version -> Valid
# 3/ Edit the INI file and pack-it -> Valid
# 4/ Upload on Github :) .

import subprocess
import fileinput
import BatchLightUE4

from os.path import dirname, join, realpath
from BatchLightUE4.Models.Setup import Setup

# All Variable
init = Setup()
path_current_file = dirname(realpath(BatchLightUE4.__file__))
setup_file = join(path_current_file, r"Models\Setup.py")
package = dirname(__file__) + '/packages.bat'

print('Actual Version : ', init.number)
nbr_version = input('Number Version : ')

with fileinput.FileInput(setup_file, inplace=True) as file:
    for line in file:
        str_old = r"number = '" + init.number + "'"
        str_new = r"number = '" + nbr_version + "'"
        print(line.rstrip().replace(str_old, str_new))

subprocess.call(package)
