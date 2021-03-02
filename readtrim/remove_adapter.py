"""
The :mod:`readtrim.remove_adapter` remove adapters from read.
"""

# Author: Jie Li <jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2020

import re
from loguru import logger

from biosut import gt_file, gt_path, gt_exe

class remove_adap:

	_max_n = "0.1"
	_q = "20,15"

	def __init__(self, fq1:str=None, fq2:str=None, \
				adap3:str=None, adap5:str=None,
				phred:int=33, ncpu:int=10, \
				outdir:str='./', basename:str="Test"):
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
		self.basename = basename

		if not self.fq1:
			logger.error(f'{self.fq1} not found, please check.')
			sys.exit()
		if not self.fq2:
			logger.error(f'{self.fq2} not found, please check.')
			sys.exit()

		if not self.adap3:
			logger.error('Please input adapter sequence from 3 end.')
			sys.exit()
		if not self.adap5:
			logger.error('Please input adapter sequence from 5 end.')
			sys.exit()

		gt_file.check_file_exist(self.fq1, self.fq2)

		self.prefix = gt_file.get_seqfile_prefix(self.fq1)

		self.outfq1 = f'{self.prefix}_noadap.1.fq.gz'
		self.outfq2 = f'{self.prefix}_noadap.2.fq.gz'

	def cutadapt(self):

		cutadapt_outdir = gt_path.sure_path_exist(
							self.outdir,
							f'{self.outdir}/cutadapt',
							f'{self.outdir}/cutadapt/{self.basename}'
							)[2]

		self.outfq1 = f'{cutadapt_outdir}/{self.outfq1}'
		self.outfq2 = f'{cutadapt_outdir}/{self.outfq2}'
		logger.info('Start to remove adapters using cutadapt.')
		cmd = f'cutadapt -a {self.adap3} -A {self.adap5} -q {self._q} \
				--quality-base {self.phred} --trim-n \
				--max-n {self._max_n} -j {self.ncpu} \
				-o {self.outfq1} -p {self.outfq2} {self.fq1} {self.fq2}'
		logger.info(f'Start to remove adapters using cutadapt, command is {cmd}.')
		gt_exe.exe_cmd(cmd, shell=True)
		gt_file.check_file_exist(self.outfq1, self.outfq2, check_exist=True)
		logger.info('Finished remove adapters.')

		return self.outfq1, self.outfq2
