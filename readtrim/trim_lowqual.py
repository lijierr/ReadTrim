"""
The :mod:`readtrim.trim_lowqual` trim low quality bases from reads.
"""

<<<<<<< HEAD
# Author: Jie Li <jlli6t@gmail.com>
# License: GNU v3.0
# Copyright: 2019
=======
__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'
>>>>>>> dev

import os
import sys
from loguru import logger



class TrimLowQual:

    def __init__(self, infq1: str = None, infq2: str = None,
                 slide_wd: str = '4:20', minlen: int = 75, croplen=None,
                 outdir='./', phred: int = 33, ncpu: int = 10):

        """
        A collection of tools for trimming.
        Args:
            infq1: FILE
                input fq1 file.
            infq2: FILE
                input fq2 file.
            slide_wd: str, default `4:20`
                sliding window, WindowSize:QCutoff.
            minlen: int, default `75`
                minimal length of read to keep.
            croplen: int, default `75`
                crop read to specified length.
            outdir: str, default `./`
                output directory.
            phred: int, default `33`
                phred value of bases.
            ncpu: int, default `10`
                number of cpu to use.
        """

        if 'TRIM_JAR' not in os.environ:
            logger.error('TRIM_JAR variable,'
                         'which indicating the jar file of trimmomatic, '
                         'is not found, please specify it in .bashrc file.')
            sys.exit()

        self.trim_jar = os.environ['TRIM_JAR']
        bs.check_file_exist(self.trim_jar)

        self.infq1 = infq1
        self.infq2 = infq2
        self.slide_wd = slide_wd
        self.minlen = minlen
        self.croplen = croplen
        self.outdir = bs.sure_path_exist(outdir)
        self.phred = phred
        self.ncpu = ncpu

        bs.check_file_exist(self.infq1, self.infq2, check_empty=True)
        self.prefix = bs.remove_suffix(self.infq1, seq=True, include_path=False)

    def trimmomatic(self):
        sub_outdir = bs.sure_path_exist(f'{self.outdir}/trimmomatic')

        outfq = f'{sub_outdir}/{self.prefix}.trim'
        outfq1 = f'{outfq}.1.fastq.gz'
        outfq2 = f'{outfq}.2.fastq.gz'
        outfq1_un = f'{outfq}.unpair.1.fastq.gz'
        outfq2_un = f'{outfq}.unpair.2.fastq.gz'
        outfq_un = f'{outfq}.unpair.fastq.gz'
        crop = self.croplen and f'CROP:{self.croplen}' or ''
        print(f'crop: {crop}')

        cmd = f'java -jar {self.trim_jar} PE -threads {self.ncpu} ' \
              f'-phred{self.phred} -trimlog {sub_outdir}/trimmomatic.log ' \
              f'{self.infq1} {self.infq2} ' \
              f'{outfq1} {outfq1_un} {outfq2} {outfq2_un} ' \
              f'LEADING:25 TRAILING:20 SLIDINGWINDOW:{self.slide_wd} ' \
              f'MINLEN:{self.minlen} {crop} 2>{sub_outdir}/trimmomatic.stat'

        logger.info('Trimming reads using trimmomatic.')
        bs.exe_cmd(cmd, shell=True)
        bs.check_file_exist(f'{sub_outdir}/trimmomatic.stat', check_empty=True)

        # zcat unpaired together
        cmd = f'zcat {outfq1_un} {outfq2_un}|gzip>{outfq_un}'
        bs.exe_cmd(cmd, shell=True)
        logger.info('Finished trim reads.')
        return outfq1, outfq2,
