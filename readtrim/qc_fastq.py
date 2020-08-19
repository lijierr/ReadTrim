"""
The :mod:`readtrim.qc_fastq` printing version information.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2018

import sys
import logging

import numpy as np
import pandas as pd

from biosut import gt_file, gt_path, gt_exe

logger = logging.getLogger(__name__)

class qc_fastq:
	"""
	Wrapper for running fastq file qc.
	"""
	def __init__(self, fq1:str=None, fq2:str=None, adapter:str=None, \
				outdir:str='./', sample_name:str='Test'):
		"""
		Wrapper for running fastsq qc.

		Parameter
		---------
		fq1 : str
			Fastq file 1.
		fq2 : str
			Fasta file 2.
		adapter : str
			Adapter sequence file in FASTA format.
		outdir : str, default is './'
			Directory to output reuslt.

		Result
		------
			Output qc result to outdir.
		"""

		self.logger = logging.getLogger()
		self.fq1 = fq1
		self.fq2 = fq2
		self.adapter = adapter
		self.outdir = outdir
		self.sample_name = sample_name

		if not self.fq1 and not self.fq2:
			logger.error('Not found fastq 1 and not found fastq file2, please check!')
			sys.exit()

	def fastqc(self):
		self.logger.info('Start to qc fastq using FastQC.')
		self.fastqc_outdir = gt_path.sure_path_exist(
							self.outdir,
							'%s/fastqc' % self.outdir, \
							'%s/fastqc/%s' % (self.outdir, self.sample_name)
							)[2]

		cmd = 'fastqc -o %s' % self.fastqc_outdir
		if self.adapter:cmd += ' -a %s' % self.adapter
		if self.fq1:cmd += ' %s' % self.fq1
		if self.fq2:cmd += ' %s' % self.fq2
		cmd += ' 2>/dev/null'
		gt_exe.exe_cmd(cmd, shell=True)

		cmd = 'ls %s/*_fastqc.zip|xargs -t -i unzip -o -d %s {}' % \
				(self.fastqc_outdir, self.fastqc_outdir)
		gt_exe.exe_cmd(cmd, shell=True)
		self.logger.info('End to qc fastq using FastQC.')
		self._stat_fastqc_result()

	def _stat_fastqc_result(self):
		self.fastqc_data = '%s/*_fastqc/fastqc_data.txt' % self.fastqc_outdir

		self.out_stat = '%s/%s.fastqc.stat.xls' % \
						(self.fastqc_outdir, self.sample_name)

		header = ['Encoding', 'Total Sequences', 'Sequence length', '%GC']

		out, _ = gt_exe.exe_cmd('grep Filename %s' % self.fastqc_data, shell=True)
		index = [gt_file.get_file_prefix(i.split('\t')[1]) for i in out.decode().splitlines()]

		nfiles, _ = gt_exe.exe_cmd('ls %s|wc -l' % self.fastqc_data, shell=True)
		self.stat = pd.DataFrame(np.zeros((int(nfiles.decode().strip()), 4)), \
								columns=header, index=index)
		for t in header:
			#set(os.popen('cat %s/*_fastqc/fastqc_data.txt|grep "'+k+'"').read().splitlines())
			out, _ = gt_exe.exe_cmd('grep "%s" %s' % (t, self.fastqc_data))
			self.stat[t] = [i.split('\t')[1] for i in out.decode().splitlines()]
		self.stat.to_csv(self.out_stat, sep='\t')

#class statFastQCResult:
#	""" Stat result of FastQC """
#	def __init__(self, outDir):
#		self.fastqc_data = outDir + "/*_fastqc/fastqc_data.txt"
#		self.out_stat = outDir + "/stats_fastqc_result.xls"
#		self.logger = logging.getLogger("timestamp")
#		nFiles = os.popen("ls %s|wc -l" % (self.fastqc_data)).read().strip()
#		self.stats = pd.DataFrame(np.zeros((int(nFiles), 4)))

#		self.statFastQC()

#	def statFastQC(self):
#		self.logger.error(self.stats.index)
#		header = ['Encoding', 'Total Sequences', 'Sequence length', '%GC']
#		self.stats.columns = header
#		for k in header:
#			set(os.popen('cat %s/*_fastqc/fastqc_data.txt|grep "'+k+'"').read().splitlines())
#			self.stats[k] = [i.split("\t")[1] for i in os.popen('grep "'+k+'" %s' % (self.fastqc_data)).read().splitlines()]

#		self.stats.to_csv(self.out_stat, sep="\t")
