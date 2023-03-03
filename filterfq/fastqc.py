############################
#
# fastqc.py - runs FastQC for data
#
#===================================================================

import os
import sys
import subprocess
import logging

import numpy as np
import pandas as pd
from filterfq.universal import checkPathExists, makeSurePathExists, checkFilesExist

class fastqcPileup:
	""" Wrapper for running fastqc """
	def __init__(self):
		self.logger = logging.getLogger("timestamp")
		
		self.__checkFastQC()

	def run(self, fqs, adapters, outDir):
		self.logger.error(fqs)
		self.logger.error(adapters)
		self.logger.error(outDir)
		checkFilesExist([fqs, adapters])

		makeSurePathExists(outDir)
		os.system("fastqc -a %s -o %s %s 2>/dev/null" % (adapters, outDir, " ".join(fqs)))
		os.system("ls %s/*_fastqc.zip|xargs -t -i unzip -u -d %s {}" % (outDir, outDir))
		self.logger.error("skipped fastqc part")
		statFastQCResult(outDir)
	
	def __checkFastQC(self):
		""" Check if FastQC is in system path. """
		# Assume that a successful fastqc -h returns and anything
		# else returns something non-zero
		try:
			subprocess.run(['fastqc', '-h'], stdout=open(os.devnull, "w"), stderr=subprocess.STDOUT)
		except:
			self.logger.error(" [Error] Make sure FastQC is in system path.")
			sys.exit(1)
	

class statFastQCResult:
	""" Stat result of FastQC """
	def __init__(self, outDir):
		self.fastqc_data = outDir + "/*_fastqc/fastqc_data.txt"
		self.out_stat = outDir + "/stats_fastqc_result.xls"
		self.logger = logging.getLogger("timestamp")
		nFiles = os.popen("ls %s|wc -l" % (self.fastqc_data)).read().strip()
		self.stats = pd.DataFrame(np.zeros((int(nFiles), 4)))

		self.statFastQC()

	def statFastQC(self):
		self.stats.index = [os.path.splitext(i.split("\t")[1])[0] for i in os.popen("grep Filename %s" % (self.fastqc_data)).read().splitlines()]
#		self.logger.error(self.stats.index)
		header = ['Encoding', 'Total Sequences', 'Sequence length', '%GC']
		self.stats.columns = header
		for k in header:
#			set(os.popen('cat %s/*_fastqc/fastqc_data.txt|grep "'+k+'"').read().splitlines())
			self.stats[k] = [i.split("\t")[1] for i in os.popen('grep "'+k+'" %s' % (self.fastqc_data)).read().splitlines()]
		
		self.stats.to_csv(self.out_stat, sep="\t")
		

