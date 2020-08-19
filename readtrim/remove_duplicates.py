"""
The :mod:`readtrim.remove_duplicates` remove duplicated reads.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2020

import re

from biosut import gt_file, gt_path, gt_exe

class remove_dup:

	def __init__(self, fq1:str=None, fq2:str=None, \
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
		self.outdir = outdir
		self.sample_name = sample_name

		if not self.fq1:
			logger.error('Not found fastq 1 file, please check.')
		if not self.fq2:
			logger.error('Not found fastq 2 file, please check.')

		gt_file.check_file_exist(self.fq1, self.fq2)

		self.prefix = gt_file.get_seqfile_prefix(self.fq1)

		self.outfq1 = '%s_nodup.1.fq' % self.prefix
		self.outfq2 = '%s_nodup.2.fq' % self.prefix


	def fastuniq(self):

		outdir = gt_path.sure_path_exist(
							self.outdir, \
							'%s/fastuniq' % self.outdir,
							'%s/fastuniq/%s' % (self.outdir, self.sample_name)
							)[2]

		self.outfq1 = '%s/%s' % (outdir, self.outfq1)
		self.outfq2 = '%s/%s' % (outdir, self.outfq2)

		if '.gz' in self.fq1:
			cmd = 'gzip -fd %s %s' % (self.fq1, self.fq2)
			gt_exe.exe_cmd(cmd, shell=True)
			self.fq1 = gt_file.get_file_prefix(self.fq1, include_path=True)
			self.fq2 = gt_file.get_file_prefix(self.fq2, include_path=True)
			print(self.fq1, self.fq2)

		cmd = 'echo "%s\n%s">%s/fq.list' % (self.fq1, self.fq2, outdir)
		gt_exe.exe_cmd(cmd, shell=True)

		cmd = 'fastuniq -i %s/fq.list -t q -o %s -p %s' % \
				(outdir, self.outfq1, self.outfq2)
		gt_exe.exe_cmd(cmd, shell=True)

		gt_file.check_file_exist(self.outfq1, self.outfq2)

		# gzip file to save space
		cmd = 'gzip -f %s %s %s %s' % (self.fq1, self.fq2, self.outfq1, self.outfq2)
		gt_exe.exe_cmd(cmd, shell=True)
		return self.outfq1+'.gz', self.outfq2+'.gz'
