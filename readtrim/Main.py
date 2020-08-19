"""
The :mod:`readtrim.Main` Main workflow of readtrim.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2020

import os
import sys
import argparse as ap
import pandas as pd
import logging

logger = logging.getLogger(__name__)
from biosut import gt_file,gt_exe,gt_path

from readtrim.version import Version
from readtrim.qc_fastq import qc_fastq
from readtrim.trim_head_Ns import removeNs
from readtrim.remove_adapter import remove_adap
from readtrim.remove_duplicates import remove_dup
from readtrim.trim_lowqual import trim_lowqual

def read_arg(args):
    p = ap.ArgumentParser(description=Version.show_version())
    required_args = p.add_argument_group('Required arguments.')
    #required_args.add_argument('--fqlist', required=True,
    #                    help='fastq file list, with head, #sample\tfq1\tfq2,\
    #                    optional columns are adap3 and adap5, \
    #                    indicates adapters from 3 end and 5 end.')
    required_args.add_argument('-fq1', '--fq1', required=True,
                        help='Input FASTQ 1 file.')
    required_args.add_argument('-fq2', '--fq2', required=True,
                        help='Input FASTQ 2 file.')
    required_args.add_argument('-o', '--outdir', required=True,
                        help='Output directory.')
    required_args.add_argument('-sn', '--sample_name', required=True,
                        help='Sample name of this input data.')
    optional_args = p.add_argument_group('Optional arguments.')
    optional_args.add_argument('--remove_headN', action='store_true',
                        help='set to remove head Ns if they are exist.')
    optional_args.add_argument('--remove_dups', action='store_true',
                        help='set to remove duplications')
    optional_args.add_argument('--remove_adap', action='store_true',
                        help='set to remove adapters, need adap3 & 5 columns.')
    optional_args.add_argument('--adap3', default=None,
                        help='Adapter sequence from 3 end.')
    optional_args.add_argument('--adap5', default=None,
                        help='Adapter sequence from 5 end.')
    optional_args.add_argument('--slide_window', default='4:20',
                        help='slide_window for trimming low quality bases, default is 4:20')
    optional_args.add_argument('--minlen', default=75, type=int,
                        help='Minimum length of read to keep, default 75.')
    optional_args.add_argument('--phred', default=33, type=int,
                        help='Phred value of base, default 33.')
    optional_args.add_argument('--ncpu', default=10, type=int,
                        help='number of cpu to use, default 10')
    arg = p.parse_args()

    #fqlist = pd.read_csv(arg.fqlist, sep='\t', header=0, index_col=0)
    #if arg.remove_adap and fqlist.shape()[1] != 4:
    #    logger.error('Remove adapter parameter was setted, \
    #        but didt found adapter sequences in fqlist file, please check.')

    if arg.remove_adap:
        if not arg.adap3 or not arg.adap5:
            logger.error('Remove adapter sequence parameter has been set, \
                        but --adap3 and --adap5 havent been set, please check!')
            sys.exit()
    return arg

class stream:
    @classmethod
    def exe(cls, args):
        arg = read_arg(args)
        cls.check_dependency(arg)
        gt_file.check_file_exist()
        outdir = gt_path.sure_path_exist(arg.outdir)
        prefix = gt_file.get_seqfile_prefix(arg.fq1)
        adapter = None
        if arg.remove_adap:
            adapter = '%s/adapter.list' % outdir
            cmd = 'echo "adap3\t%s\nadap5\t%s">%s' % \
                (arg.adap3, arg.adap5, adapter)
            gt_exe.exe_cmd(cmd)

        qc = qc_fastq(fq1=arg.fq1, fq2=arg.fq2, adapter=adapter, \
    				outdir=outdir, sample_name=arg.sample_name)
        qc.fastqc()
        if arg.remove_headN:
            removens = removeNs(arg.fq1, arg.fq2, outdir=outdir)
            arg.fq1, arg.fq2 = removens.removeNs_seq()
        if arg.remove_dups:
            rm_dup = remove_dup(fq1=arg.fq1, fq2=arg.fq2, outdir=outdir, sample_name=arg.sample_name)
            arg.fq1, arg.fq2 = rm_dup.fastuniq()
        if arg.remove_adap:
            rm_adap = remove_adap(fq1=arg.fq1, fq2=arg.fq2,
                                adap3=arg.adap3, adap5=arg.adap5,
        				        phred=arg.phred, ncpu=arg.ncpu,
        				        outdir=outdir, sample_name=arg.sample_name)
            arg.fq1, arg.fq2 = rm_adap.cutadapt()
        trim_lq = trim_lowqual(infq1=arg.fq1, infq2=arg.fq2,
                    slide_wd=arg.slide_window, minlen=arg.minlen,
                    outdir=outdir, phred=arg.phred, ncpu=arg.ncpu,
                    sample_name=arg.sample_name)
        arg.fq1, arg.fq2 = trim_lq.trimmomatic()
        qc = qc_fastq(fq1=arg.fq1, fq2=arg.fq2, adapter=adapter, \
                    outdir=outdir, sample_name=arg.sample_name+'.filter')
        qc.fastqc()

    def check_dependency(arg):
        gt_exe.is_executable('fastqc')
        if arg.remove_dups:gt_exe.is_executable('fastuniq')
        if arg.remove_adap:gt_exe.is_executable('cutadapt')
