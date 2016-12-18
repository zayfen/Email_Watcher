#!/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from subprocess import CompletedProcess
import time

def main() :
	while True:
		completed_process = None
		try:
			print("start process...")
			completed_process = subprocess.run(['dirs'])
			print("end process")
		except Exception as e:
			print ("terminal process")
			pass
		finally:
			time.sleep(2)
			if isinstance(completed_process, CompletedProcess) :
				print(completed_process.returncode)
				print(completed_process.output)
				print(completed_process.stdout)
				print(completed_process.stderr)


if __name__ == '__main__':
	main()