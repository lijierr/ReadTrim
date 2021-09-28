#!/usr/bin/env python
#coding:utf-8

#================================================================
#Contact: Jie Li (jeveylijie@gmail.com)
#Description:
#v1.0	20180418	do FastQC of sequencing reads
#
#================================================================

import os
import sys
import argparse as ap
import basictools as basic
import pipelinetools as pipe
import pandas as pd 

def read_paras( args ):
	p = ap.ArgumentParser(description=__doc__)
	g = p.add_argument_group("Required arguments")
	ars = g.add_argument
	ars("--fqlist", dest="fqlist", required=True,
		help="fqlist file, with header, sampleName<tab>q1<tab>q2, abs path")

	g = p.add_argument_group("Optional arguments")
	ars = g.add_argument
	ars("--adapters", dest="adapters", 
		default=os.path.dirname(sys.argv[0])+"/adapters.txt",
		help="adapters, format name<tab>adapter seq")
	ars("--outdir", dest="outdir", default=os.getcwd(),
		help="outdir to output result, default is ./")
	ars("--qsubs", dest="qsubs", default="select=1:ncpus=2:mem=2GB",
		help="arguments for qsub system, [select=1:ncpus=2:mem=2GB]")
	ars("--walltime", dest="walltime", default="00:60:00",
		help="walltime of your task to run [00:60:00]")
	ars("--run", dest="run", action="store_true",
		help="set if you want to run all scripts directly.")
	ars("--arguments", dest="arguments", default="",
		help="other arguments you want to use for FastQC")
	ars("--rm", dest="rm", action="store_true",
		help="set to rm *.sh.* files")
	return vars(p.parse_args())


def FastQC(adapters, process, shell, result, sample, orinames, 
		   fqs, arguments, fastqc, rm, qsubs, walltime):
	process = process + sample + "/"
	result = result + sample + "/"
	basic.mkdir([process, result])
	sl = fastqc + \
		 " -a " + adapters + \
		 " -o " + process + \
		 " " + arguments + \
		 " " + fqs[0] + \
		 " " + fqs[1] + " &&\n"
	sl += "ls " + process + "*_fastqc.zip|xargs -t -i unzip -u -d " + process +" {} &&\n"
	for oriname in orinames:
		read = str(orinames.index(oriname) + 1)
		oriname = process + oriname +"_fastqc/Images/"
		sl += "cp " + oriname + "per_base_quality.png " + \
			  result + sample + "_R"+read+"_per_base_quality.png &&\n"
		sl += "cp " + oriname + "duplication_levels.png " + \
			  result + sample + "_R"+read+"_duplication_levels.png &&\n"
		sl += "cp " + oriname + "per_base_sequence_content.png " + \
			  result + sample + "_R"+read+"_per_base_sequence_content.png &&\n"
	#	sl += "cp " + oriname + "per_tile_quality.png " + \
	#		  result + sample + "_R"+read+"_per_tile_quality.png &&\n"
	pipe.creat_shell(sl, shell+"FastQC_"+sample+".sh", rm, qsubs, walltime)
	
if __name__ == "__main__":
	pars = read_paras(sys.argv)
	#print(pars)
	outdir = basic.outdir(pars['outdir']) + "/"
	basic.mkdir([outdir, outdir+"process", outdir+"shell", outdir+"result",
				outdir+"process/FastQC", outdir+"/shell/FastQC",
				outdir+"result/FastQC"])

	all_fqs = pd.read_csv(pars['fqlist'], sep="\t", header=0, index_col=0)
	all_fqs.index = [str(i) for i in all_fqs.index]  ## add to avoid if sample name is just a number
	##FastQC output as original file name,
#	original_file_name = {}
	softwares = basic.parse_config(os.path.dirname(sys.argv[0])+"/softwares.txt")
	for sample in all_fqs.index:
		##FastQC output as original file name, $name is the original file name
		fqs = list(all_fqs.loc[sample])
		name1 = ".".join(os.path.basename(fqs[0]).split(".")[:-2])
		name2 = ".".join(os.path.basename(fqs[1]).split(".")[:-2]) 
		sl = FastQC(pars['adapters'], outdir+"process/FastQC/", 
					outdir+"shell/FastQC/", outdir+"result/FastQC/", 
					sample, [name1, name2], all_fqs.loc[sample], 
					pars['arguments'], softwares['fastqc'], 
					pars['rm'], pars['qsubs'], pars['walltime'])
	sl = softwares['python36'] + \
		 " " + os.path.dirname(sys.argv[0]) + "/stat_fastqc_result-v1.0.py" + \
		 " --fqlist " + pars['fqlist'] + \
		 " --FastQC_dir " + outdir + "process/FastQC/" + \
		 " --outfile " + outdir + "result/FastQC/stats_of_FastQC_result.xls &&\n"
	#print(sl)
	pipe.creat_shell(sl, outdir+"shell/FastQC/stat_FastQC.sh", pars['rm'], pars['qsubs'], pars['walltime'])


