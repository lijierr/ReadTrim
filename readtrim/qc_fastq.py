"""
The :mod:`readtrim.qc_fastq` printing version information.
"""

__author__ = "Jie Li"
__copyright__ = "Copyright 2018"
__credits__ = "Jie Li"
__license__ = "GNU v3.0"
__maintainer__ = "Jie Li"
__email__ = "jlli6t near gmail.com"

import sys
from loguru import logger

import numpy as np
import pandas as pd

from biosut import gt_file, gt_path, gt_exe


class QCFastq:

    def __init__(self, fq1: str = None, fq2: str = None,
                 adapter: str = None, out_dir: str = "./",
                 basename: str = "test", Continue: bool = False):
#	def __init__(self, fq1: str = None, fq2: str = None, adapter: str = None,
  #               outdir: str = "./", basename: str = 'Test', contin=False):
        """Wrapper for running fastsq qc.


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
		basename : str, default is 'Test'
			Basename for outputs.
		continue : bool, default is False.
			Set True to continue from last check point.

		Result
		------
			Output qc result to outdir.
		"""

        # self.logger = logging.getLogger(__name__)
        # use loguru to set up the logger system
        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.out_dir = out_dir
        self.basename = basename
        self.Continue = Continue

        if not self.fq1 and not self.fq2:
            logger.error(f"Both {self.fq1} and {self.fq2} are not found!")
            sys.exit()

    def fastqc(self):

        self.fastqc_outdir = gt_path.sure_path_exist(
            self.out_dir,
            f"{self.out_dir}/fastqc",
            f"{self.out_dir}/fastqc/{self.basename}"
        )[2]

        cmd = f'fastqc -o {self.fastqc_outdir}'
        if self.adapter: cmd += f' -a {self.adapter}'
        if self.fq1: cmd += f' {self.fq1}'
        if self.fq2: cmd += f' {self.fq2}'

        cmd += ' 2>/dev/null'
        logger.info(f'Start run FastQC, command is {cmd}.')
        gt_exe.exe_cmd(cmd, shell=True)
        cmd = f'ls {self.fastqc_outdir}/*_fastqc.zip|xargs -t -i unzip -o -d {self.fastqc_outdir} {{}}'
        logger.info(f'Start to unzip FastQC results, command is {cmd}.')
        # .format(outdir=self.fastqc_outdir)
        gt_exe.exe_cmd(cmd, shell=True)
        logger.info('Finished run FastQC.')
        self._stat_fastqc_result()

    def _stat_fastqc_result(self):
        self.fastqc_data = f'{self.fastqc_outdir}/*_fastqc/fastqc_data.txt'

        self.out_stat = f'{self.fastqc_outdir}/{self.basename}.fastqc.stat.xls'

        header = ['Encoding', 'Total Sequences', 'Sequence length', '%GC']

        out, _ = gt_exe.exe_cmd('grep Filename {}'.format(self.fastqc_data),
                                shell=True)
        index = [gt_file.get_file_prefix(i.split('\t')[1]) for i in
                 out.decode().splitlines()]

        nfiles, _ = gt_exe.exe_cmd(f'ls {self.fastqc_data}|wc -l', shell=True)
        self.stat = pd.DataFrame(np.zeros((int(nfiles.decode().strip()), 4)), \
                                 columns=header, index=index)
        for t in header:
            # set(os.popen('cat %s/*_fastqc/fastqc_data.txt|grep "'+k+'"').read().splitlines())
            out, _ = gt_exe.exe_cmd(f'grep "{t}" {self.fastqc_data}')
            self.stat[t] = [i.split('\t')[1] for i in out.decode().splitlines()]
        self.stat.to_csv(self.out_stat, sep='\t')

# class statFastQCResult:
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
