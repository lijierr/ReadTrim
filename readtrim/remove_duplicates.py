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


<<<<<<< HEAD
class remove_dup:
    self.dt = {}

    def __init__(self, fq1:str=None, fq2:str=None, \
                 outdir:str='./', basename:str="Test"):
        """
        Wrapper of removing adapters.

        Parameter
        ---------
        fq1 : str
            Pair fastq 1 file.
        fq2 : str
            Pair fastq 2 file.
        adap3 : str
            Adapter sequence from 3 end.
        adap5 : str
            Adapter sequence from 5 end.
        phred : int, default is 33.
            Phred value of base.
        ncpu : int, default 10
            Number of cpus to use.
        outdir : str, default is current directory.
            Output directory to output result.
        basename : str, default is Test.
            Basename for outputs.
        """

        self.fq1 = fq1
        self.fq2 = fq2
        self.outdir = outdir
        self.basename = basename

        if not self.fq1:
            logger.error('Have to specify fq1 file, please check.')
            sys.exit()
        if not self.fq2:
            logger.error('Have to specify fq2 file, please check.')
            sys.exit()

        gt_file.check_file_exist(self.fq1, self.fq2)

        self.prefix = gt_file.get_seqfile_prefix(self.fq1)

        self.outfq1 = f'{self.prefix}.nodup.1.fq'
        self.outfq2 = f'{self.prefix}.nodup.2.fq'

    def fastuniq(self):

        fastuniq_outdir = gt_path.sure_path_exist(
            self.outdir,
            f'{self.outdir}/fastuniq',
            f'{self.outdir}/fastuniq/{self.basename}')[2]

        self.outfq1 = f'{self.outdir}/{self.outfq1}'
        self.outfq2 = f'{self.outdir}/{self.outfq2}'

        if '.gz' in self.fq1:
            cmd = f'gzip -fd {self.fq1} {self.fq2}'
            gt_exe.exe_cmd(cmd, shell=True)
            self.fq1 = gt_file.get_file_prefix(self.fq1, include_path=True)
            self.fq2 = gt_file.get_file_prefix(self.fq2, include_path=True)
        #print(self.fq1, self.fq2)

        cmd = f'echo "{self.fq1}\n{self.fq2}">{fastuniq_outdir}/fq.list'
        gt_exe.exe_cmd(cmd, shell=True)
        logger.info('Start to remove duplications using fastuniq, command is {cmd}.')
        cmd = f'fastuniq -i {fastuniq_outdir}/fq.list -t q \
				-o {self.outfq1} -p {self.outfq2}'
        gt_exe.exe_cmd(cmd, shell=True)

        gt_file.check_file_exist(self.outfq1, self.outfq2)

        # gzip file to save space
        cmd = f'gzip -f {self.fq1} {self.fq2} {self.outfq1} {self.outfq2}'
        gt_exe.exe_cmd(cmd, shell=True)
        logger.info('Finished remove duplications.')
        return self.outfq1+'.gz', self.outfq2+'.gz'
=======
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
>>>>>>> dev
