"""
The :mod:`readtrim.remove_adapter` remove adapters from read.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2020

import re

from biosut import gt_file, gt_path, gt_exe

class remove_adap:

	_max_n = "0.1"
	_q = "20,15"

	def __init__(self, fq1:str=None, fq2:str=None, \
				adap3:str=None, adap5:str=None,
				phred:int=33, ncpu:int=10, \
				outdir:str='./', sample_name:str="Test"):
		"""
		Wrapper of removing adapters.

		Parameter
		---------
		fq1 : str
			Pair fastq 1 file.
		fq2 : str
			Pair fastq 2 file.
		adap3 : str
			Adapter sequence from 3 end.
		adap5 : str
			Adapter sequence from 5 end.
		phred : int, default is 33.
			Phred value of base.
		ncpu : int, default 10
			Number of cpus to use.
		outdir : str, default is current directory.
			Output directory to output result.
		sample_name : str, default is Test.
			Sample name of this data, will create corresponding direcotry.
		"""

		self.fq1 = fq1
		self.fq2 = fq2
		self.adap3 = adap3
		self.adap5 = adap5
		self.phred = phred
		self.ncpu = ncpu
		self.outdir = outdir
		self.sample_name = sample_name

		if not self.fq1:
			logger.error('Not found fastq 1 file, please check.')
			sys.exit()
		if not self.fq2:
			logger.error('Not found fastq 2 file, please check.')
			sys.exit()

		if not self.adap3:
			logger.error('Please input adapter sequence from 3 end.')
			sys.exit()
		if not self.adap5:
			logger.error('Please input adapter sequence from 5 end.')
			sys.exit()

		gt_file.check_file_exist(self.fq1, self.fq2)

		self.prefix = gt_file.get_seqfile_prefix(self.fq1)

		self.outfq1 = '%s_noadap.1.fq.gz' % self.prefix
		self.outfq2 = '%s_noadap.2.fq.gz' % self.prefix

	def cutadapt(self):

		outdir = gt_path.sure_path_exist(
							self.outdir, \
							'%s/cutadapt' % self.outdir,
							'%s/cutadapt/%s' % (self.outdir, self.sample_name)
							)[2]

		self.outfq1 = '%s/%s' % (outdir, self.outfq1)
		self.outfq2 = '%s/%s' % (outdir, self.outfq2)

		cmd = 'cutadapt -a %s -A %s -q %s --quality-base %s --trim-n %s --max-n %s -j %d' % \
			(adap3, adap5, self._q, self.phred, self._max_n, self.ncpu)
		cmd += ' -o %s -p %s %s %s' % \
				(self.outfq1, self.outfq2, self.fq1, self.fq2)

		gt_exe.exe_cmd(cmd, shell=True)

		return self.outfq1, self.outfq2
