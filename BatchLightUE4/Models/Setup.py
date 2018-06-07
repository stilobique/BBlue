import os

from configparser import ConfigParser
from os.path import dirname, join, exists, expanduser

"""
    This file control the instances to work with the INI files, write and
    read it. He include the setup name file and the number version ; it's
    automatically update with the built setup.

    The ``Setup`` Class
    ===================

    Main Class, all function use this class.

"""


class Setup(object):
    config = ConfigParser()
    config_name = 'settings.ini'
    number = '0.9.4'
    config_path = join(expanduser('~'), 'BBLUE4', config_name)

    if not exists(dirname(config_path)):
        os.makedirs(dirname(config_path))

    def __init__(self):
        if exists(self.config_path):
            self.read()
        else:
            self.write()

    def write(self):
        self.config.add_section('Project Work')
        self.config.add_section('All Projects')
        self.config.add_section('Default')
        self.config.add_section('Version')

        self.config['Project Work'] = {'Run': '', }
        self.config['Default'] = {
            'Editor': '',
            'Project': '',
            'Sub Folder': '',
            'CSV': False,
        }

        self.config['Version'] = {'Version': self.number, }

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

    def read(self):
        data = self.config.read(self.config_path)

        return data

    def base(self, option):
        self.config.read(self.config_path)
        data = self.config.get('Default', option)

        return data

    def last_job_run(self):
        """
        Function to call the 'last job run'
        :return: return a string with the path for the job used
        """
        self.config.read(self.config_path)
        data = self.config.get('Project Work', 'run')

        return data

    def last_job_add(self, filename):
        self.config.read(self.config_path)
        self.config.set('Project Work', 'Run', filename)

        with open(self.config_path, 'w') as configfile:
            self.config.write(configfile)

