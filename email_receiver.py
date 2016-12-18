#!/bin/env python

# -*- coding: utf-8 -*-

import email
from email.parser import Parser
import poplib


class Message:
    def __init__(self):
        self.subject = None
        self.from_ = None
        self.to = None
        self.date = None
        self.file_name = None
        self.contents_plain = []
        self.contents_html = []
        self.id = None

    # @property
    # def subject(self):
    #     return self.subject

    # @subject.setter
    # def subject(self, subject):
    #     self.subject = subject

    # @property
    # def date(self):
    #     return self.date

    # @date.setter
    # def date(self, date):
    #     self.date = date

    # @property
    # def from_(self):
    #     return self.from_

    # @from_.setter
    # def from_(self, from_):
    #     self.from_ = from_

    # @property
    # def to(self):
    #     return self.to

    # @to.setter
    # def to(self, to):
    #     self.to = to

    # @property
    # def fileName(self):
    #     return self.file_name

    # @fileName.setter
    # def fileName(self, file_name):
    #     self.file_name = file_name


def toMessage(msg):
    message = Message()
    message.subject = email.Header.decode_header(msg.get('Subject'))
    message.subject = message.subject[0][0].decode(message.subject[0][1])
    message.date = msg.get('Date')
    message.from_ = msg.get('from')
    message.to = msg.get('to')

    for part in msg.walk():
        content_type = part.get_content_type()
        charset = part.get_content_charset()

        if content_type == 'text/plain':
            data_content = part.get_payload(decode=True)
            text_content = data_content.decode(charset)
            message.contents_plain.append(text_content)

        if content_type == 'text/html':
            data_content = part.get_payload(decode=True)
            text_content = data_content.decode(charset)
            message.contents_html.append(text_content)

    message.contents_plain = "".join(message.contents_plain)
    message.contents_html = "".join(message.contents_html)
    return message


class EmailReceiver(object):
    def __init__(self, pop3_server, port=995):
        self._pop3_server = pop3_server
        self._port = port
        self._server = None

    @property
    def server(self):
        return self._pop3_server

    @server.setter
    def server(self, server):
        self._pop3_server = server

    @property
    def email(self):
        return self._email_addr

    @email.setter
    def email(self, email_addr):
        self._email_addr = email_addr

    def set_password(self, passwd):
        self._passwd = passwd

    def login(self, email_addr, passwd, use_ssl=True):
        self._email_addr = email_addr
        self._passwd = passwd
        if (use_ssl):
            self._server = poplib.POP3_SSL(self._pop3_server, self._port)
        else:
            self._server = poplib.POP3(self._pop3_server, self._port)
        self._server.user(self._email_addr)
        self._server.pass_(self._passwd)

    def get_emails_state(self):
        return self._server.stat()

    def fetch_emails_list(self):
        self.resp, self.mails, self.octets = self._server.list()

    def get_email_by_id(self, id):
        _, lines, _ = self._server.retr(id)
        msg_content = b'\r\n'.join(lines)
        emailMsg = Parser().parsestr(msg_content.decode('utf-8'))
        message = toMessage(emailMsg)
        message.id = id
        return message

    def get_email_count(self):
        count = 0
        if self.mails:
            count = len(self.mails)
        return count

    def get_latest_email(self):
        self.fetch_emails_list()
        length = len(self.mails)
        return self.get_email_by_id(length)

    def logout(self):
        self._server.quit()

if __name__ == '__main__':
    pop3_server = 'pop.163.com'
    email_addr = 'article_receiver@163.com'
    passwd = 'zyf515815'
    # pop3_server = 'pop.qq.com'
    # email_addr = input("qq email: ")
    # passwd = input("qq password: ")
    receiver = EmailReceiver(pop3_server)
    receiver.login(email_addr, passwd)
    receiver.fetch_emails_list()
    latest_email = receiver.get_latest_email()
    print('subject: ' + latest_email.subject)
    print('date: ' + latest_email.date)
    print('from: ' + latest_email.from_)
    print('to: ' + latest_email.to)
    print( latest_email.contents_plain)

