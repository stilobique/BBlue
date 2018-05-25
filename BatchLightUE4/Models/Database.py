import os
import sqlite3

from os.path import normpath, dirname, basename
from BatchLightUE4.Models.Setup import Setup


class TableProgram(object):
    """Objects to work with the SQLite"""

    def __init__(self):
        super(TableProgram, self).__init__()
        data = Setup()
        self.base_sql = data.last_job_run()
        self.bd_exist = os.path.exists(self.base_sql)

        self.bd = sqlite3.connect(self.base_sql)

        if not self.bd_exist:
            self.create_all_tables()

        self.bd.cursor()

    def create_all_tables(self):
        """Generate all Table inside the Database"""
        self.bd.cursor()
        self.bd.execute('''CREATE TABLE  projects(
                id          INTEGER PRIMARY KEY,
                name        TEXT,
                CSV         TEXT)''')

        self.bd.execute('''CREATE TABLE  paths(
                path_id     INTEGER PRIMARY KEY,
                editor      TEXT,
                project     TEXT,
                scene       TEXT,
                csv         TEXT)''')

        self.bd.execute('''CREATE TABLE levels(
                level_id    INTEGER PRIMARY KEY,
                name        TEXT,
                path        TEXT,
                state       INTEGER)''')

        self.bd.execute('''CREATE TABLE csv(
                software    TEXT)''')

        csv = 'False'
        self.bd.execute('''INSERT INTO csv VALUES (?)''', (csv,))

        self.bd.commit()
        # self.bd.close()

    def select_paths(self):
        """
        Select a Data path from a project used
        :return:
        """
        id_project = 1
        request = self.bd.cursor()
        request.execute('''SELECT * FROM paths 
                        WHERE path_id = ?''',
                        (id_project, ))

        data = request.fetchall()

        return data

    def select_levels(self, state=None, name=None):
        """Select a Data path from a project used.
        :id_project : The project working"""
        request = self.bd.cursor()
        if state is not None:
            request.execute('''SELECT * FROM levels WHERE state = ?''',
                            (state, ))

        elif name is not None:
            request.execute('''SELECT * FROM levels WHERE name = ?''',
                            (name, ))
        else:
            request.execute('''SELECT * FROM levels''')

        data = request.fetchall()

        return data

    def write_data_path(self, editor, project, scene):
        """
        Function to write all paths data :
        :param editor: path with the Editor path (UE4editor.exe)
        :param project: path with the project path (*.uproject)
        :param scene: string with the sub level
        :return:
        """
        id_project = 1
        self.bd.cursor()
        count_paths = self.bd.execute('''SELECT count(path_id) FROM paths''')
        count_paths = count_paths.fetchone()[0]

        if count_paths == 0:
            self.bd.execute('''INSERT INTO paths VALUES(?, ?, ?, ?, ?)''',
                            (id_project, editor, project, scene, 'None'))

        else:
            self.bd.execute('''UPDATE paths 
                            SET editor = ?, project = ?, scene = ? 
                            WHERE path_id = ?''',
                            (editor, project, scene, id_project))

        self.bd.commit()
        self.bd.close()

    def write_data_levels(self, parent, state, data):
        id_project = 1
        self.bd.cursor()

        dict_path = {
            'unreal': parent.ue4_path_text.text(),
            'project': parent.project_file_text.text(),
            'folder': parent.sub_folder_text.text()
        }

        path_project = dirname(dict_path['project']) + '/Content/' + dict_path[
            'folder']
        path_project = normpath(path_project)

        name = data[0]
        path = data[1]

        if state:
            print('True, add a value')
            self.bd.execute('''INSERT INTO levels
                                            (name, path, state)
                                            VALUES(?, ?, ?)''',
                            (name, path, state))

        else:
            print('False, remove a data')
            self.bd.execute('''DELETE FROM levels WHERE name=?''', (name,))

        self.bd.commit()

    def csv_data(self, csv=str()):
        self.bd.cursor()
        if csv:
            data = self.bd.execute('''UPDATE csv SET software = ?''', (csv, ))
        else:
            data = self.bd.execute('''SELECT * FROM csv''')
            data = data.fetchone()
        self.bd.commit()

        return data

    def debug_data(self):
        cur = self.bd.cursor()
        cur.execute('''SELECT * FROM paths''')

        rows = cur.fetchall()

        for row in rows:
            print('Data : ', row)

        msg_func = 'Read Data from the base data'
        print(msg_func)
