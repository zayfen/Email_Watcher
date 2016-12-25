#!/bin/env python

# -*- coding: utf-8 -*-

import json


class Config(object):
	"""parse config.json
	"""
	def __init__(self, config_path="./config/config.json"):
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
		for email_ in self.white_list:
			if email_ in email:
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

		
