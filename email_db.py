#!/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

class EmailDb(object):
    def __init__(self, db_path=None, db_name=None):
        self._db_path = db_path
        self._db_name = db_name
        self._db_connecter = None
        self.__CREATE_DB_IF_NOT_EXIST = ''
        self.__CREATE_TABLE_IF_NOT_EXIST = ('create table "email"  ('
                                            'id int(11) not null,'
                                            'date varchar(20),'
                                            'from varchar(50),'
                                            'to varchar(50),'
                                            'subject varchar(200),'
                                            'content text'
                                            'primary key (\'id\')) if not exists;')
        self._connected = False

    def connect(self):
        self._db_connecter = sqlite3.connect(self._db_path + "/" + self._db_name)
        self.create_email_table_if_not_exist()
        self._connected = True

    def create_email_table_if_not_exist(self):
        assert(self._connected is True)
        self._db_connecter.execute(self.__CREATE_TABLE_IF_NOT_EXIST)
        if self._db_connecter:
            self._cursor = self._db_connecter.cursor()
            self._cursor.execute(self.__CREATE_TABLE_IF_NOT_EXIST)
            self._db_connecter.commit()
            self._cursor.close()


    def save_email(self, id, date, from_, to, subject, content):
        assert(self._connected is True)
        sql_insert = ('insert into email values({},{},{},{},{},{});'.format(id, date, from_, to, subject, content))
        self._cursor = self._db_connecter.cursor()
        self._cursor.execute(sql_insert)
        self._db_connecter.commit()
        self._cursor.close()

    def is_email_existed(self, id):
        sql_fetch_id = 'select id from email;'
        self._cursor = self._db_connecter.cursor()
        self._cursor.execute(sql_fetch_id)
        ids = self._cursor.fetchall()
        for id_ in ids:
            if id == id_:
                return True;
        return False
        
    def close(self):
        self._cursor.close()
        self._db_connecter.close()
