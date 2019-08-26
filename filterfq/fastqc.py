############################
#
# fastqc.py - runs FastQC for data
#
#===================================================================

import os
import sys
import subprocess
import logging

from universal import checkPathExists, makeSurePathExists,checkFilesExist

class fastqcPileup:
	""" Wrapper for running fastqc """
	def __init__(self):
		self.logger = logging.getLogger("timestamp")
		
		self.checkFastQC()

		
	def checkFastQC(self):
		""" Check if FastQC is in system path! """
		
		# Assume that a successful fastqc -h returns and anything
		# else returns something non-zero
		try:
			subprocess.call(['fastqc', '-h'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		except:
			self.logger.error(" [Error] Make sure FastQC is in system path.")
			sys.exit(1)


	def run(self, fqs, adapters, outDir):
		
		checkFilesExist(fqs, adapters)

		makeSurePathExists(outDir)

		os.system("fastqc -a %s -o %s %s 2>/dev/null" % (adapters, outDir, " ".join()))
		os.system("ls %s/*_fastqc.zip|xargs -t -i unzip -u -d %s {}" % (outDir, outDir))

class statFastQCResult:
	""" Stat result of FastQC """
	def __init__(self):
		self.logger = logging.getLogger("timestamp")
		
		
		
		

