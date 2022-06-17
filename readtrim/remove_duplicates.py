"""
The :mod:`readtrim.remove_duplicates` remove duplicated reads.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

from loguru import logger
from biosut import biosys as bs


class RemoveDup:
    def __init__(self, fq1: str = None, fq2: str = None,
                 outdir: str = './', basename: str = 'test'):
        """
        Wrapper of removing adapters.
        Args:
            fq1: FILE
                input fq1 file.
            fq2: FILE
                input fq2 file.
            outdir: str, default `./`
                output directory.
            basename: str, default `test`
                basename for outputs.
        """
        self.fq1 = fq1
        self.fq2 = fq2
        self.outdir = bs.sure_path_exist(outdir)
        self.basename = basename

        bs.check_file_exist(self.fq1, self.fq2, check_empty=True)
        self.prefix = bs.remove_suffix(self.fq1, seq=True, include_path=False)

    def fastuniq(self):
        sub_outdir = bs.sure_path_exist(f'{self.outdir}/fastuniq/')

        outfq = f'{sub_outdir}/{self.prefix}.nodup'
        outfq1 = f'{outfq}.1.fastq'
        outfq2 = f'{outfq}.2.fastq'
        fqlist = f'{sub_outdir}/fastq.list'

        if '.gz' in self.fq1:
            cmd = f'gzip -fd {self.fq1} {self.fq2}'
            bs.exe_cmd(cmd, shell=True)
            self.fq1 = bs.remove_suffix(self.fq1, include_path=True)
            self.fq2 = bs.remove_suffix(self.fq2, include_path=True)

        # print(self.infq1, self.infq2)

        cmd = f'echo -e "{self.fq1}\n{self.fq2}">{fqlist}'
        bs.exe_cmd(cmd, shell=True)
        logger.info(f'Removing duplications with fastuniq')
        cmd = f'fastuniq -i {fqlist} -t q -o {outfq1} -p {outfq2}'
        bs.exe_cmd(cmd, shell=True)

        bs.check_file_exist(outfq1, outfq2)

        # gzip file to save space
        cmd = f'gzip -f {self.fq1} {self.fq2} {outfq1} {outfq2}'
        bs.exe_cmd(cmd, shell=True)
        logger.info('Finished remove duplications.')
        return outfq1 + '.gz', outfq2 + '.gz'
