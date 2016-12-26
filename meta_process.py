#!/bin/env python
# -*- coding: utf-8 -*-

import base64
from config import Config
from email_db import EmailDb
from email_db import EmailItem
from email_receiver import EmailReceiver
from email_receiver import Message
import imp
import time
import sys
import unicodedata


class MetaRun(object):
    """docstring for MetaRun"""

    def __init__(self):
        super(MetaRun, self).__init__()
        self.config = Config()
        self.email_db = EmailDb(self.config.db_path, self.config.db_name)
        self.email_db.connect()
        self.receiver = EmailReceiver(self.config.emails[0]['pop3'])
        self.receiver.login(self.config.emails[0]['account'], self.config.emails[0]['passwd'])

    def save_email(self, email_item):
        self.email_db.save_email_item(email_item)

    def publish_article(self, title, content):
        file_path_name = self.config.publish_path + title + ".md"
        with open(file_path_name, mode='w') as file_:
            file_.write(content.encode('utf-8'))

    def run(self):
        ''' step1 receive email per 1 minute
                when receive an email, check sender whether in white list
				if is, get save email to db, and write email content to {subject}.md 
        '''
        while True:
            self.receiver.login(self.config.emails[0]['account'], self.config.emails[0]['passwd'])

            emails_state = self.receiver.get_emails_state()
            print("Count: %d,  Size: %d" % (emails_state[0], emails_state[1]))

            self.receiver.fetch_emails_list()
            email_count = emails_state[0]
            while email_count:
                this_id = email_count
                email_count = email_count - 1
                this_email = self.receiver.get_email_by_id(this_id)
                from_ = this_email.from_
                b_in_white_list = self.config.in_white_list(from_)
                b_existed = self.email_db.is_email_existed(this_email.id)
                print('ID: ' + str(this_email.id) + "  Existed: " + str(b_existed))
                if b_in_white_list and not b_existed:
                    email_item = EmailItem()
                    email_item.id = this_email.id
                    email_item.from_ = this_email.from_
                    email_item.to = this_email.to
                    email_item.date = this_email.date
                    email_item.subject = this_email.subject
                    email_item.content = this_email.contents_plain
                    print("subject: " + email_item.subject)
                    print("content: " + email_item.content)
                    self.publish_article(email_item.subject, email_item.content)
                    self.save_email(email_item)
                else:
                    print("no new article ")
                    break
            
            self.receiver.logout()
            time.sleep(2 * 60) # relogin after 2 minutes
            
def main():
    meta = MetaRun()
    meta.run()

if __name__ == '__main__':
    main()
