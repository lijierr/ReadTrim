"""
The :mod:`readtrim.Main` Main workflow of readtrim.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'


import sys
import argparse as ap

from loguru import logger

from biosut import gt_exe, gt_path

from readtrim.version import Version
from readtrim.qc_fastq import QCFastq
from readtrim.trim_Ns import TrimNs
from readtrim.trim_adapter import TrimAdap
from readtrim.remove_duplicates import RemoveDup
from readtrim.trim_lowqual import TrimLowQual


def read_args():
    p = ap.ArgumentParser(description=Version.show_version())
    required_arg = p.add_argument_group("Required parameters.")
    # required_args.add_argument('--fqlist', required=True,
    #                    help='fastq file list, with head, #sample\tfq1\tfq2,\
    #                    optional columns are adap3 and adap5, \
    #                    indicates adapters from 3 end and 5 end.')
    required_arg.add_argument('-infq1', '--infq1', required=True,
                              help='Input FASTQ 1 file.')
    required_arg.add_argument('-infq2', '--infq2', required=True,
                              help='Input FASTQ 2 file.')
    required_arg.add_argument('-o', '--outdir', required=True,
                              help='Output directory.')
    required_arg.add_argument('-bs', '--basename', required=True,
                              help='Basename for outputs.')
    optional_arg = p.add_argument_group('Optional parameters.')
    optional_arg.add_argument('--continue', action='store_true',
                              help='set to continue from last check point.')
    optional_arg.add_argument('--trim_ns', action='store_true',
                              help='set to remove head Ns if they are exist.')
    optional_arg.add_argument('--remove_dups', action='store_true',
                              help='set to remove duplications')
    optional_arg.add_argument('--trim_adap', action="store_true",
                              help='set to trim adapters, ' \
                                   'must set --adap3 & --adap5.')
    optional_arg.add_argument('--adap3', default=None,
                              help='Adapter sequence from 3 end.')
    optional_arg.add_argument('--adap5', default=None,
                              help='Adapter sequence from 5 end.')
    optional_arg.add_argument('--slide_window', default='4:20',
                              help='sliding window for bad quality ends trim,'
                                   'default is 4:20')
    optional_arg.add_argument('--minlen', default=75, type=int,
                              help='Minimum length of read to keep, default 75.')
    optional_arg.add_argument('--croplen', default=None,
                              help="Crop reads into specific lengths, "
                                   "default not crop.")
    optional_arg.add_argument('--phred', default=33, type=int,
                              help='Phred value of base, default 33.')
    optional_arg.add_argument('--ncpu', default=10, type=int,
                              help='number of cpu to use, default 10')
    arg = p.parse_args()

    # fqlist = pd.read_csv(arg.fqlist, sep='\t', header=0, index_col=0)
    # if arg.remove_adap and fqlist.shape()[1] != 4:
    #    logger.error('Remove adapter parameter was set, \
    #        but did not found adapter sequences in fqlist file, please check.')

    if arg.trim_adap:
        if not arg.adap3 or not arg.adap5:
            logger.error('--adap3 and --adap5 must set to enable --trim_adap.')
            sys.exit()
    return arg


class ReadTrim:
    @classmethod
    def readtrim(cls):
        arg = cls.check_dependency()
        outdir = gt_path.sure_path_exist(arg.outdir)

        if arg.trim_adap:
            adapter = f'{outdir}/adapter.list'
            cmd = f'echo "adap3\t{arg.adap3}\nadap5\t{arg.adap5}">{adapter}'
            gt_exe.exe_cmd(cmd)
        else:
            adapter = None

        qc = QCFastq(infq1=arg.infq1, infq2=arg.infq2, adapter=adapter,
                     outdir=outdir, basename=arg.basename
                     )
        qc.fastqc()

        if arg.trim_ns:
            trimns = TrimNs(arg.infq1, arg.infq2, outdir=outdir)
            arg.fq1, arg.fq2 = trimns.trim_ns()

        if arg.remove_dups:
            rm_dup = RemoveDup(infq1=arg.fq1, infq2=arg.fq2,
                               outdir=outdir, basename=arg.basename
                               )
            arg.fq1, arg.fq2 = rm_dup.fastuniq()

        if arg.trim_adap:
            trim_adap = TrimAdap(infq1=arg.fq1, infq2=arg.fq2,
                                 adap3=arg.adap3, adap5=arg.adap5,
                                 phred=arg.phred, ncpu=arg.ncpu,
                                 outdir=outdir, basename=arg.basename
                                 )
            arg.fq1, arg.fq2 = trim_adap.cutadapt()

        trim_lq = TrimLowQual(infq1=arg.fq1, infq2=arg.fq2,
                              slide_wd=arg.slide_window, minlen=arg.minlen,
                              outdir=outdir, phred=arg.phred, ncpu=arg.ncpu,
                              basename=arg.basename, croplen=arg.croplen
                              )
        arg.fq1, arg.fq2 = trim_lq.trimming()

        qc = QCFastq(infq1=arg.fq1, infq2=arg.fq2, adapter=adapter,
                     outdir=outdir, basename=arg.basename + '.filter'
                     )
        qc.fastqc()

    @staticmethod
    def check_dependency():
        gt_exe.is_executable('fastqc')
        arg = read_args()
        if arg.remove_dups: gt_exe.is_executable('fastuniq')
        if arg.trim_adap: gt_exe.is_executable('cutadapt')
        return arg
