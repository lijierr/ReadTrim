"""
The :mod:`readtrim.remove_adapter` trim adapters from read.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

import sys

from loguru import logger
from biosut import biosys as bs


class TrimAdap:
    _max_n = '0.1'
    _q = '20,15'

    def __init__(self, infq1: str = None, infq2: str = None,
                 adap3: str = None, adap5: str = None,
                 phred: int = 33, ncpu: int = 10,
                 outdir: str = './'):
        """
        A collection of tools for removing adapters.
        Args:
            infq1: FILE
                input fq1 file.
            infq2: FILE
                input fq2 file.
            adap3: str, default `None`
                adapter sequence from 3 end.
            adap5: str, default `None`
                adapter sequence from 5 end.
            phred: int, default `33`
                phred value of bases.
            ncpu: int, default `10`
                number of cpu to use.
            outdir: str, default `./`
                output directory
        """

        self.infq1 = infq1
        self.infq2 = infq2
        self.adap3 = adap3
        self.adap5 = adap5
        self.phred = phred
        self.ncpu = ncpu
        self.outdir = bs.sure_path_exist(outdir)

        bs.check_file_exist(self.infq1, self.infq2)

        if not self.adap3:
            logger.error('Please input adapter sequence from 3 end.')
            sys.exit()
        if not self.adap5:
            logger.error('Please input adapter sequence from 5 end.')
            sys.exit()

        self.prefix = bs.remove_suffix(self.infq1, seq=True, include_path=False)

    def cutadapt(self):
        sub_outdir = bs.sure_path_exist(f'{self.outdir}/cutadapt')

        outfq = f'{sub_outdir}/{self.prefix}.noadap'
        outfq1 = f'{outfq}.1.fastq.gz'
        outfq2 = f'{outfq}.2.fastq.gz'

        logger.info('Removing adapters using cutadapt.')
        cmd = f'cutadapt -a {self.adap3} -A {self.adap5} -q {self._q} ' \
              f'--quality-base {self.phred} --trim-n ' \
              f'--max-n {self._max_n} -j {self.ncpu} ' \
              f'-o {outfq1} -p {outfq2} {self.infq1} {self.infq2}'

        logger.info(f'Start to remove adapters using cutadapt.')
        bs.exe_cmd(cmd, shell=True)
        bs.check_file_exist(outfq1, outfq2, check_empty=True)
        logger.info('Finished remove adapters.')
        return outfq1, outfq2
