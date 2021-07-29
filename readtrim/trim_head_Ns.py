"""
The :mod:`readtrim.remove_head_Ns` remove head Ns from sequences.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GNU v3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

import re
import gzip
import sys
from loguru import logger

from biosut import gt_file, gt_path, gt_exe
from biosut import io_seq, alter_seq


class removeNs:

	def __init__(self, *seqin, outdir:str=None):
		"""
		Remove N(s) located head of each read.

		Parameter
		---------
		seqin : str
			Input sequence file (s).
		outf : str
			Directory to output files.
		fmt : str, default is fastq.
			Input sequence format, fastq/fasta.
		"""

		self.seqin = seqin
		self.outdir = gt_path.sure_path_exist(outdir,
										outdir + '/removeN')[1]

		if not self.outdir:
			logger.error('You have to specify an outdir!')
			sys.exit()

	def removeNs_seq(self):
		for idx, seq in enumerate(self.seqin, 1):
			logger.info('Start removing Ns from {seq}')
			gt_file.check_file_exist(seq, check_empty=True)
			fh = gt_file.perfect_open(seq)
			prefix = gt_file.get_seqfile_prefix(seq)
			out_seq_file = f'{self.outdir}/{prefix}.noN.{idx}.fq.gz'
			alter_seq.trim_headn(inseq=seq, outseq=out_seq_file, outqual=True)
			logger.info('End removing Ns from {seq}')
		return f'{self.outdir}/{prefix}.noN.1.fq.gz', \
				f'{self.outdir}/{prefix}.noN.2.fq.gz'
