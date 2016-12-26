#!/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from subprocess import CompletedProcess
import time

import sys
import io

print("default encoding: " + sys.getdefaultencoding())
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

gExceptionOccured = False

def notifyException(exception_msg):
	global gExceptionOccured
	if gExceptionOccured:
		return 0
	# TODO: 发通知，告知服务异常

	# 值 gExceptonOccured = True， 防止重复地去发异常通知
	gExceptonOccured = True


def main() :
	while True:
		completed_process = None
		try:
			print("start process...")
			completed_process = subprocess.run(['python', 'meta_process.py'])
			print("end process")
		except Exception as e:
			print ("terminal process")
			pass
		finally:
			time.sleep(10)
			if isinstance(completed_process, CompletedProcess) :
				print(completed_process.returncode)
				print(completed_process.stdout)
				print(completed_process.stderr)


if __name__ == '__main__':
	main()
