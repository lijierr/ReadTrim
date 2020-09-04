"""
The :mod:`readtrim.remove_duplicates` remove duplicated reads.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2020

import re
from loguru import logger

from biosut import gt_file, gt_path, gt_exe

class remove_dup:
	self.dt = {}

	def __init__(self, fq1:str=None, fq2:str=None, \
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
		basename : str, default is Test.
			Basename for outputs.
		"""

		self.fq1 = fq1
		self.fq2 = fq2
		self.outdir = outdir
		self.basename = basename

		if not self.fq1:
			logger.error('Have to specify fq1 file, please check.')
			sys.exit()
		if not self.fq2:
			logger.error('Have to specify fq2 file, please check.')
			sys.exit()

		gt_file.check_file_exist(self.fq1, self.fq2)

		self.prefix = gt_file.get_seqfile_prefix(self.fq1)

		self.outfq1 = f'{self.prefix}.nodup.1.fq'
		self.outfq2 = f'{self.prefix}.nodup.2.fq'

	def fastuniq(self):

		fastuniq_outdir = gt_path.sure_path_exist(
							self.outdir,
							f'{self.outdir}/fastuniq',
							f'{self.outdir}/fastuniq/{self.basename}')[2]

		self.outfq1 = f'{self.outdir}/{self.outfq1}'
		self.outfq2 = f'{self.outdir}/{self.outfq2}'

		if '.gz' in self.fq1:
			cmd = f'gzip -fd {self.fq1} {self.fq2}'
			gt_exe.exe_cmd(cmd, shell=True)
			self.fq1 = gt_file.get_file_prefix(self.fq1, include_path=True)
			self.fq2 = gt_file.get_file_prefix(self.fq2, include_path=True)
			#print(self.fq1, self.fq2)

		cmd = f'echo "{self.fq1}\n{self.fq2}">{fastuniq_outdir}/fq.list'
		gt_exe.exe_cmd(cmd, shell=True)
		logger.info('Start to remove duplications using fastuniq, command is {cmd}.')
		cmd = f'fastuniq -i {fastuniq_outdir}/fq.list -t q \
				-o {self.outfq1} -p {self.outfq2}'
		gt_exe.exe_cmd(cmd, shell=True)

		gt_file.check_file_exist(self.outfq1, self.outfq2)

		# gzip file to save space
		cmd = f'gzip -f {self.fq1} {self.fq2} {self.outfq1} {self.outfq2}'
		gt_exe.exe_cmd(cmd, shell=True)
		logger.info('Finished remove duplications.')
		return self.outfq1+'.gz', self.outfq2+'.gz'
