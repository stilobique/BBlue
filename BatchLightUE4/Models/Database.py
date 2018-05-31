import os
import sqlite3

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
                scv         TEXT)''')

        self.bd.execute('''CREATE TABLE  paths(
                path_id     INTEGER PRIMARY KEY,
                editor      TEXT,
                project     TEXT,
                scene       TEXT,
                scv         TEXT)''')

        self.bd.execute('''CREATE TABLE levels(
                level_id    INTEGER PRIMARY KEY,
                name        TEXT,
                path        TEXT,
                state       INTEGER)''')

        self.bd.execute('''CREATE TABLE scv(
                software    TEXT,
                user        TEXT,
                password    TEXT)''')

        self.bd.execute('''INSERT INTO scv VALUES (?, ?, ?)''',
                        ('False', '', ''))

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

    def select_scv(self):
        """
        Function to select all Source Control options
        :return:
        """
        data = self.bd.execute('''SELECT * FROM scv''')
        data = data.fetchone()

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
        # self.bd.close()

    def write_data_levels(self, state, data):
        self.bd.cursor()

        name = data[0]
        path = data[1]

        if state:
            self.bd.execute('''INSERT INTO levels
                                            (name, path, state)
                                            VALUES(?, ?, ?)''',
                            (name, path, state))

        else:
            self.bd.execute('''DELETE FROM levels WHERE name=?''', (name,))

        self.bd.commit()

    def write_scv(self, scv_data):
        """
        Function to Write the Source Control data.
        :param scv_data: a list with all data to saved :
                            - The software used
                            - username
                            - password
        :return:
        """
        self.bd.cursor()
        print(scv_data)
        scv_db = self.select_scv()

        if not scv_db:
            print('No data, write something')
            self.bd.execute('''INSERT INTO scv
                                            (software, user, password)
                                            VALUES(?, ?, ?)''',
                            (scv_data[0], scv_data[1], scv_data[2]))

        else:
            print('Update a data')
            print(scv_db[0])
            self.bd.execute('''UPDATE scv 
                            SET software = ?, user = ?, password = ? 
                            WHERE software = ?''',
                            (scv_data[0], scv_data[1], scv_data[2], scv_db[0]))
