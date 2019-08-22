############################
#
# fastqc.py - runs FastQC for data
#
#===================================================================

import os
import sys
import subprocess
import logging

class fastqcPileup:
	""" Wrapper for running fastqc """
	def __init__(self, outDir):
		self.logger = logging.getLogger('timestamp')
	def checkFastQC(self):
		""" Check if FastQC is in system path! """
		
		# Assume that a successful fastqc -h returns and anything
		# else returns something non-zero
		try:
			subprocess.call(['fastqc', '-h'], stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
		except:
			self.logger.error(" [Error] Make sure FastQC is in system path.")
			sys.exit(1)
		

