###################################
#
# trimmomatic.py - runs trimmomatic and provides stat result output
#
########################################################################

import os
import sys
import logging
import subprocess

from filterfq.fastqc import fastqcPileup


class trimmomaticPileup:
	""""Trimmomoatic wrapper"""
	def __init__(self, outDir):
		self.logger = logging.getLogger("timestamp")
	
	
	
	def checkFastUniq(self):
		"""Check if fastuniq is in the system."""
		try:
			subprocess.run(['fastuniq'], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
		except:
			self.logger.error(" [Error] Make sure fastuniq is on your system path.")
			sys.exit(1)

	def checkJava(self):
		"""Check if java is in the system."""
		try:
			subprocess.run(['java', '-h'], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
		except:
			self.logger.error(" [Error] Make sure java is on your system path.")
			sys.exit(1)
	
	def checkTrimmomatic(self):
		""""Check if trimmomatic is in the system."""
		try:
			subprocess.run(['java', ])


