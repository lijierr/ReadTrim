"""
The :mod:`readtrim.trim_head_Ns` remove head Ns from sequences.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

from loguru import logger

from biosut import biosys as bs
from biosut import bioseq as bq


class TrimNs:
	def __init__(self, *inseq, outdir: str = None, fmt: str = 'fastq'):
		"""
		Remove N(s) located at the start of each read.
		Args:
			*inseq: FILE (s)
				input sequence file (s).
			outdir: str, default `None`
				output directory.
			fmt: str, default `fastq`
				format of input sequence file, fastq/fasta.
		"""
		self.inseq = inseq
		self.outdir = bs.sure_path_exist(outdir, f'{outdir}/TrimNs')[1]
		self.fmt = fmt

		self.prefix = f'{bs.remove_suffix(inseq[0], seq=True, include_path=False)}'

	def trim_ns(self):
		outfq = f'{self.outdir}/{self.prefix}.noN'
		for idx, seq in enumerate(self.inseq, 1):
			logger.info('Trimming head Ns.')
			bs.check_file_exist(seq, check_empty=True)
			out_seq_file = f'{outfq}.{idx}.fastq.gz'
			qual = self.fmt == 'fastq' and True or False
			bq.trim_headn(inseq=seq, outseq=out_seq_file, outqual=qual)
			logger.info('Finished trimming head Ns')
		return f'{outfq}.1.fastq.gz', f'{outfq}.2.fastq.gz'
