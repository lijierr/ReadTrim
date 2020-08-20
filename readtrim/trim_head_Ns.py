"""
The :mod:`readtrim.remove_head_Ns` remove head Ns from sequences.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2019

import re
import gzip
import sys

from biosut import gt_file, gt_path, gt_exe
from biosut import io_seq

class removeNs:

	def __init__(self, *seqin, outdir:str=None, fmt:str='fastq'):
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
		self.fmt = fmt

		if not self.outdir:
			logger.error('You have to specify an outdir!')
			sys.exit()

	def removeNs_seq(self):
		for seq, idx in zip(self.seqin, list(range(1,len(self.seqin)+1))):
			gt_file.check_file_exist(seq, check_empty=True)
			fh = gt_file.perfect_open(seq)
			prefix = gt_file.get_seqfile_prefix(seq)
			out_handle = gzip.open('%s/%s.noN.%d.fastq.gz'% \
								(self.outdir, prefix, idx), 'wb')
			# split into if else loop, escape from judge every time.
			if self.fmt == 'fastq':
				for t, seq, qual in io_seq.iterator(fh):
					seq = self._remove_first_Ns(seq)
					line = '@%s\n%s\n+\n%s\n' % (t, seq, qual[:len(seq)])
					out_handle.write(line.encode())
			else:
				for t, seq, qual in io_seq.iterator(fh):
					seq = self._remove_first_Ns(seq)
					line = '>%s\n%s\n' % (t, seq)
					out_handle.write(line.encode())
			gt_file.close_file(fh, out_handle)
		return '%s/%s.noN.1.fastq.gz' % (self.outdir, prefix), \
				'%s/%s.noN.2.fastq.gz' % (self.outdir, prefix)
#	def removeNs_fasta(self, fasta, outf):
#		from Bio.SeqIO.FastaIO import SimpleFastaParser
#		fasta_handle = perfect_open(fasta)
		# use low-level parser to speed up
#		with gzip.open(outf, "wb") as out_hanble:
#			for title, seq in SimpleFastaParser(fasta_handle):
#				seq = self._remove_first_N(seq)
#				line = ">%s\n%s\n" %(title, seq)
#				out_handle.write(line.encode())

#	def removeNs_fastq(self, fastq, outf):
#		from Bio.SeqIO.QualityIO import FastqGeneralIterator
#		fastq_handle = perfect_open(fastq)
		# use low-level parser to speed up
#		with gzip.open(outf, "wb") as out_handle:
#			for title, seq, qual in FastqGeneralIterator(fastq_handle):
#				nseq = self._remove_first_N(seq)
#				qual = qual[len(seq)-len(nseq):]
#				line="@%s\n%s\n+\n%s\n" % (title, nseq, qual)
#				out_handle.write(line.encode())

	def _remove_first_Ns(self, string):
		while re.match('N', string, flags=re.I):
			string = string[1:]
		#	self._remove_first_N(string)
		return string
