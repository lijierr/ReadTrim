#!/usr/bin/env python3
#===================================================
##
# cutadapt.py -- run cutadapt to remove adapter sequences from reads
##
#===================================================

import os
import sys
import re
import subprocess

from system import check_program,check_file_exist 

class cutadapt:
	"""
	Pile up cutadapt to remove dual adapters.
	"""
	_max_n = "0.1"
	_q = "20,15"

	def __init__(self):
		check_program('cutadapt')

	def run(self, adap3, adap5, phred, ncpu, fq1, fq2, outdir):
		outdir = os.path.realpath(outdir)
		check_file_exist([fq1, fq2])
		cmd = ['cutadapt', '-a', adap3, '-A', adap5, '-q', self._q, 
				'--quality-base', phred, '--trim-n',
				'--max-n', self._max_n, '-j', ncpu]
		
		prefix = re.sub('.\d.fastq.gz|.\d.fq.gz|.\d.fastq|.\d.fq', '', os.path.basename(fq1))
		prefix = outdir + '/' + prefix
		cmd += ['-o', prefix+'_cutadapt.1.fastq.gz', 
				'-p', prefix+'_cutadapt.2.fastq.gz', 
				fq1, fq2]

		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		proc.wait()

		if proc.returncode !=0:
			sys.exit('Error encountered while running cutadapt')

if __name__ == '__main__':	
	if len(sys.argv) == 1:
		sys.exit(sys.argv[0] + '[adap3] [adap5] [phred] [ncpu] [fq1] [fq2] [outdir]')

	a3 = sys.argv[1]
	a5 = sys.argv[2]
	phred = sys.argv[3]
	ncpu = sys.argv[4]
	fq1 = sys.argv[5]
	fq2 = sys.argv[6]
	outdir = sys.argv[7]

	run_cutadapt = cutadapt()
	run_cutadapt.run(a3, a5, phred, ncpu, fq1, fq2, outdir)



