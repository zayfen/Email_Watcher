#!/bin/env python

# -*- coding: utf-8 -*-

import json


# class EmailLoginAttrs(object):
# 	"""docstring for EmailLoginItem"""
# 	def __init__(self, pop3_server, account, passwd, enable_ssl=True, port=995):
# 		super(EmailLoginItem, self).__init__()
# 		self.pop3_server = pop3_server
# 		self.account = account
# 		self.passwd = passwd
# 		self.prot = port
# 		self.enable_ssl = enable_ssl


class Config(object):
	"""parse config.json
	"""
	def __init__(self, config_path="./config.json"):
		super(Config, self).__init__()
		self.config_path = config_path
		with open(self.config_path) as self.json_data:
			self.data = json.load(self.json_data)

		self.emails = []
		self.white_list = []
		self.emails = self.data['emails']
		self.white_list = self.data['white_list']

		self.db_path = self.data['db']['path']
		self.db_name = self.data['db']['name']
		self.publish_path = self.data['publish_path']

	def in_white_list(self, email):
		if email in self.white_list:
			return True
		return False

	def get_login_emails(self):
		return self.emails

	def get_white_list(self):
		return self.white_list

def main():
	config = Config()
	print(config.emails)
	print(config.white_list)
	print(config.db_path)
	print(config.db_name)
	print(config.publish_path)

if __name__ == '__main__':
	main()

		