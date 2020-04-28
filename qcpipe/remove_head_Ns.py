#!/30days/s4506266/softwares/anaconda3/bin/python
#===================================================
##
# remove_head_Ns.py -- remove head Ns from sequences
##
#===================================================

import Bio
import re
import gzip
from sequtils import perfect_open
import sys

class removeNs:

	def __init__(self):
		pass
	
	def removeNs_fasta(self, fasta, outf):
		from Bio.SeqIO.FastaIO import SimpleFastaParser
		fasta_handle = perfect_open(fasta)
		# use low-level parser to speed up
		with gzip.open(outf, "wb") as out_hanble:
			for title, seq in SimpleFastaParser(fasta_handle):
				seq = self._remove_first_N(seq)
				line = ">%s\n%s\n" %(title, seq)
				out_handle.write(line.encode())


	def removeNs_fastq(self, fastq, outf):
		from Bio.SeqIO.QualityIO import FastqGeneralIterator
		fastq_handle = perfect_open(fastq)
		# use low-level parser to speed up
		with gzip.open(outf, "wb") as out_handle:
			for title, seq, qual in FastqGeneralIterator(fastq_handle):
				nseq = self._remove_first_N(seq)
				qual = qual[len(seq)-len(nseq):]
				line="@%s\n%s\n+\n%s\n" % (title, nseq, qual)
				out_handle.write(line.encode())

	def _remove_first_N(self, string):
		'''
		Remove the first N from a string
		'''
		while re.match('N', string, flags=re.I):
			string = string[1:]
		#	self._remove_first_N(string)

		return string


if len(sys.argv) == 1:
	sys.exit(sys.argv[0] + "[fq] [outfq]")

fq = sys.argv[1]
outfq = sys.argv[2]

remove = removeNs()
remove.removeNs_fastq(fq, outfq)


