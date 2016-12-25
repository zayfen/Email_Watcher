#!/bin/env python
# -*- coding: utf-8 -*-

import imp
import sqlite3
import sys
from utils import Utils


## id, date, from_, to, subject, content
class EmailItem(object):
    def __init__(self):
        self.id = None
        self.date = None
        self.from_ = None
        self.to = None
        self.subject = None
        self.content = None

    def __str__(self):
        s = ('id: ' + str(self.id) + '\n'
            'date: ' + self.date + '\n'
            'from_: ' + self.from_ + '\n'
            'to: ' + self.to + '\n'
            'subject: ' + self.subject + '\n'
            'content: ' + self.content + '\n')
        return s

class EmailDb(object):
    def __init__(self, db_path=None, db_name=None):
        self._db_path = db_path
        self._db_name = db_name
        self._db_connecter = None
        self.__CREATE_DB_IF_NOT_EXIST = ''
        self.__CREATE_TABLE_IF_NOT_EXIST = ('create table if not exists t_email ('
                                            'id INTEGER PRIMARY KEY,'
                                            'date TEXT,'
                                            'from_ TEXT,'
                                            'to_ TEXT,'
                                            'subject TEXT,'
                                            'content TEXT);')
        self.__cursor = None
        self._connected = False

    def __enter__(self):
        return self

    def __exist__(self):
        if self._db_connecter:
            self.close()

    def connect(self):
        self._db_connecter = sqlite3.connect(self._db_path + "/" + self._db_name)
        if self._db_connecter:
            self._connected = True
            self._cursor = self._db_connecter.cursor()
        self.create_email_table_if_not_exist()
            

    def create_email_table_if_not_exist(self):
        print(self.__CREATE_TABLE_IF_NOT_EXIST)
        assert(self._connected is True)
        self._db_connecter.execute(self.__CREATE_TABLE_IF_NOT_EXIST)
        if self._db_connecter:
            self._cursor.execute(self.__CREATE_TABLE_IF_NOT_EXIST)
            self._db_connecter.commit()

    def save_email_item(self, email_item):
        b64_date = Utils.base64_encode(email_item.date)
        b64_from = Utils.base64_encode(email_item.from_)
        b64_to = Utils.base64_encode(email_item.to)
        b64_subject = Utils.base64_encode(email_item.subject)
        b64_content = Utils.base64_encode(email_item.content)
        return self.save_email(email_item.id, b64_date, b64_from, b64_to, b64_subject, b64_content)

    def save_email(self, id, date, from_, to, subject, content):
        assert(self._connected is True)
        sql_insert = ""
        try :
            sql_insert = ('insert into t_email values(\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\");'.format(id, date, from_, to, subject, content))
            self._cursor.execute(sql_insert)
            self._db_connecter.commit()
            return True
        except sqlite3.IntegrityError as e:
            print ('can\'t save email due to id has been used')
            raise e
        except Exception as e:
            print ("save email error when execute sql: %s" % sql_insert)
            raise e
        return False

    def delete_email(self, id):
        '''delete a email by email id
        '''
        sql_delete = 'delete from t_email where id={}'.format(id)
        self._cursor.execute(sql_delete)
        self._db_connecter.commit()

    def is_email_existed(self, id):
        sql_fetch_id = 'select * from t_email where id=%d;' % id
        rows = self._cursor.execute(sql_fetch_id)
        for row in rows:
            return True
        return False

    def fetch_email_item(self, id):
        ''' fetch email by id
            Attributes: 
            id -- email id
            Return: EmailItem instance or None when not get a email
        '''
        sql_fetch_email = 'select * from t_email where id=%d' % id
        print(sql_fetch_email)
        row = self._cursor.execute(sql_fetch_email)
       
        for email_tuple in row:
            email_item = EmailItem()
            email_item.id = email_tuple[0]
            email_item.date = Utils.base64_decode(email_tuple[1])
            email_item.from_ = Utils.base64_decode(email_tuple[2])
            email_item.to = Utils.base64_decode(email_tuple[3])
            email_item.subject = Utils.base64_decode(email_tuple[4])
            email_item.content = Utils.base64_decode(email_tuple[5])
            return email_item
        return None


    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._db_connecter:
            self._db_connecter.close()


# def main():
#     email_db = EmailDb('./', 'email.db')
#     email_db.connect()
#     email_db.save_email(43, "2016-10-10", "zhangyunfeng0101@gmail.com", "845835744@qq.com", "just a test中文", "我爱我的祖国this is content")
#     print (email_db.fetch_email_item(2))

# if __name__ == '__main__':
#     main()
