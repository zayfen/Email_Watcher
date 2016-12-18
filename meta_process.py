#!/bin/env python
# -*- coding: utf-8 -*-

from config import Config
from email_db import EmailDb
from email_db import EmailItem
from email_receiver import EmailReceiver
from email_receiver import Message
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
		with open (file_path_name, 'w') as file_:
			file_.write(content)


	def run(self):
		''' step1 receive email per 1 minute
			when receive an email, check sender whether in white list
			if is, get save email to db, and write email content to {subject}.md 
		'''
		while True:
			self.receiver.fetch_emails_list()
			latest_email = self.receiver.get_latest_email()
			from_ = latest_email.from_
			a = self.config.in_white_list(from_)
			print(from_)
			b = self.email_db.is_email_existed(latest_email.id)
			print(a , b)
			if self.config.in_white_list(from_) and not self.email_db.is_email_existed(latest_email.id):
				email_item = EmailItem()
				email_item.id = latest_email.id
				email_item.from_ = latest_email.from_
				email_item.to = latest_email.to
				email_item.date = latest_email.date
				email_item.subject = latest_email.subject
				email_item.content = latest_email.contents_plain
				self.save_email(email_item)
				self.publish_article(email_item.subject, email_item.content)
			else:
				print("no new article")
			time.sleep(1 * 60)


def main():
	meta = MetaRun()
	meta.run()

if __name__ == '__main__':
	main()
