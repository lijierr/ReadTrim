"""
The :mod:`readtrim.qc_fastq` qc the fastq files.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

import sys

import numpy as np
import pandas as pd
from loguru import logger

from biosut import biosys as bs


class QCFastq:
    def __init__(self, fq1: str = None, fq2: str = None,
                 adapter: str = None, outdir: str = './',
                 basename: str = 'test', contin: bool = False
                 ):
        """
        Wrapper for running fastq qc.
        Args:
            infq1: FILE
                input fq1 file.
            infq2: FILE
                input fq2 file.
            adapter: str, default `None`
                adapter sequence file in FASTA format.
            outdir: str, default `./`
                directory to output result.
            basename: str, default `test`
                basename for outputs.
            contin: boolean, default `False`
                set to continue from last check point.
        """

        self.fq1 = fq1
        self.fq2 = fq2
        self.adapter = adapter
        self.outdir = bs.sure_path_exist(outdir)
        self.basename = basename
        self.contin = contin

        bs.check_file_exist(self.fq1, self.fq2, self.adapter, check_tmpty=True)

    def fastqc(self):
        sub_outdir = bs.sure_path_exist(f'{self.outdir}/fastqc')

        cmd = f'fastqc -o {sub_outdir}'
        if self.adapter: cmd += f' -a {self.adapter}'
        if self.fq1: cmd += f' {self.fq1}'
        if self.fq2: cmd += f' {self.fq2}'

        cmd += ' 2>/dev/null'
        logger.info(f'Running fastqc. {cmd}.')
        bs.exe_cmd(cmd, shell=True)
        cmd = f'ls {sub_outdir}/*_fastqc.zip|' \
              f'xargs -t -i unzip -o -d {sub_outdir} {{}}'
        logger.info(f'Start to unzip FastQC results, command is {cmd}.')
        # .format(outdir=self.fastqc_outdir)
        bs.exe_cmd(cmd, shell=True)
        logger.info('Finished run FastQC.')
        self._stat_fastqc_result(sub_outdir)

    def _stat_fastqc_result(self, fastqc_outdir):
        fastqc_data = f'{fastqc_outdir}/*_fastqc/fastqc_data.txt'

        out_stat = f'{fastqc_outdir}/fastqc.stat.xls'

        header = ['Encoding', 'Total Sequences', 'Sequence length', '%GC']

        out, _ = bs.exe_cmd('grep Filename {}'.format(fastqc_data), shell=True)
        # index = [bs.remove_suffix(i.split('\t')[1]) for i in out.splitlines()]
        index = [i.split('\t')[1] for i in out.decode().splitlines()]

        nfiles, _ = bs.exe_cmd(f'ls {fastqc_data}|wc -l', shell=True)
        stat = pd.DataFrame(np.zeros((int(nfiles.decode().strip()), 4)),
                            columns=header, index=index)
        for t in header:
            # cmd = 'cat %s/*_fastqc/fastqc_data.txt|grep "'+k+'"'
            # set(os.Popen(cmd).read().splitlines())
            out, _ = bs.exe_cmd(f'grep "{t}" {fastqc_data}')
            stat[t] = [i.split('\t')[1] for i in out.decode().splitlines()]
        stat.to_csv(out_stat, sep='\t')
