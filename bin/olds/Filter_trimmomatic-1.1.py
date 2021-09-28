#!/ifshk4/BC_PUB/biosoft/PIPE_RD/Package/Python-3.5.2/bin/python3
#coding:utf-8

###============================================================
#Contact: Jie Li (jeveylijie@gmail.com)
#v1.0	20170502	Use Trimmomatic to process raw reads
#					Use seqtk to stat and process clean reads
#					then you get high quality PE reads
#
#v1.1	20180420	Modified the input rawdata list format
#=============================================================


import os
import sys
import argparse as ap
try:
	import basictools as basic
except ImportError:
	sys.stderr.write("Error, basictools package not detected!")
	sys.exit(2)
from re import search

try:
	import pipelinetools as pipe
except ImportError:
	sys.stderr.write("Error, piplinetools package not detected!")
	sys.exit(1)
import pandas as pd


def read_params(args):
	p = ap.ArgumentParser(description=__doc__)
	g = p.add_argument_group("Required arguments")
	ars = g.add_argument
	ars("--rawData_list", dest="rawData_list", required=True,
		help="raw reads list file with header, SampleName<tab>FQ1<tab>FQ2, \
			 if you want to merge fq1s then SampleName<tab>fq1,fq1<tab>fq2,fq2")
	ars("--read_length", dest="readlength", default="100",
		help="raw read length, [100]")
	ars("--minlength", dest="minlength", default=75,
		help="minimum length of read to keep, [75]")
	ars("--sliding_window", dest="sliding_window", default="4:20",
		help="windowSize:average_quality_required, [4:20]")
	ars("--phred", dest="phred", default="33",
		help="phred, 33 or 64, [33]")
	ars("--adapters", dest="adapters", required=True,
		help="adapters sequences file")
	ars("--adapters_params", dest="adapters_params", default="2:30:10",
		help="params for adapters, seedMismatchs:palindromeClipThreshold:simpleClipThreshold [2:30:10]")

	g = p.add_argument_group("Optional arguments")
	ars = g.add_argument
	ars("--project", dest="project", default="mytest",
		help="project to qsub tasks [mytest]")
	ars("--queue", dest="queue", default="bc.q",
		help="queue to qsub tasks, [bc.q]")
	ars("--rm", dest="rm", action="store_true", default=False,
		help="set to rm *.sh.* files")
	ars("--outdir", dest="outdir", default=os.getcwd(),
		help="outdir to output files, [./]")
	ars("--threads", dest="threads", default="5",
		help="threads number to use, [5]")
	ars("--leading", dest="leading", default="25",
		help="Specifies the minimum quality required to keep a base, [25]")
	ars("--trailing", dest="trailing", default="20",
		help="Specifies the minimum quality required to keep a base, [20]")
	return vars(p.parse_args())


def stat_trimmomatic_filter_result(process, shell, lenth, rm):
	sl = "python3 " +os.path.dirname(sys.argv[0]) +"stat_trimmomatic_from_log.v0.10.py" + \
		 " --trimmomatic_log_list " + process + "trimmomatic.log.list" + \
		 " --trimmomatic_stat_list " + process + "trimmomatic.stat.list" + \
		 " --read_length " + str(lenth) + \
		 " --out_stat_file " + process + "All_filter_stat.xls && \\\n"
	pipe.creat_shell(sl, shell + "CleanData_stat.sh",rm)
	return  shell + "CleanData_stat.sh"

def parse_fqs(fqs):
	fq1 = fqs[0].split(",")
	fq2 = fqs[1].split(",") if len(fqs)==2 else []
	print(fq1)
	return fq1, fq2

def trimmomatic_filter(sampleShell, sampleProcess, sample, fqs, pars, softwares):
	fq1, fq2 = parse_fqs(fqs)
	q1 = sampleProcess + "raw_" + sample + "_1.fq.gz"
	q2 = sampleProcess + "raw_" + sample + "_2.fq.gz"
	seqtk = softwares['seqtk']
	if len(fq1) == 1:
		sl = "ln -sf " + " ".join(fq1) + " " + q1 + " && \n"
		sl += "ln -sf " + " ".join(fq2) + " " + q2 + " && \n"
	else:	
		sl = "zcat " + " ".join(fq1) + "|gzip >" + q1 + " && \n"
		sl += "zcat " + " ".join(fq2) + "|gzip >" + q2 + " && \n"
	sl += seqtk + " fqchk" + \
		  " " + q1 + \
		  ">" + sampleProcess + sample + "_raw_reads_seqtk_position_qual.fq1.txt && \n"
	sl += seqtk + " fqchk" + \
		  " " + q2 + \
		  ">" + sampleProcess + sample + "_raw_reads_seqtk_position_qual.fq2.txt && \n"
		#type = "PE" if search(",", Samples[sample]) else "SE"
		#Samples[sample].replace(",", " ")
	sl += "java -jar " + softwares['trimmomatic'] + \
		  " PE" + \
		  " -threads " + pars['threads'] + \
		  " -phred" + pars['phred'] + \
		  " -trimlog " + sampleProcess + sample + "_trimmomatic.log" + \
		  " " + q1 + \
		  " " + q2 + \
		  " " + sampleProcess + sample + "_clean_pair.fq1.gz" + \
		  " " + sampleProcess + sample + "_clean_unpair.fq1.gz" + \
		  " " + sampleProcess + sample + "_clean_pair.fq2.gz" + \
		  " " + sampleProcess + sample + "_clean_unpair.fq2.gz" + \
		  " ILLUMINACLIP:" + pars['adapters'] + ":" + pars['adapters_params'] + \
		  " LEADING:" + pars['leading'] + \
		  " TRAILING:" + pars['trailing'] + \
		  " SLIDINGWINDOW:" + pars['sliding_window'] + \
		  " MINLEN:" + str(pars['minlength']) + \
		  " 2>" + sampleProcess + sample + "_trimmomatic.stat && \\\n"

	sl += seqtk + " fqchk " + sampleProcess + sample + "_clean_pair.fq1.gz>" + \
	 	  sampleProcess + sample + "_clean_pair_reads_seqtk_position_qual.fq1.txt && \n"
	sl += seqtk + " fqchk " + sampleProcess + sample + "_clean_pair.fq2.gz>" + \
		  sampleProcess + sample + "_clean_pair_reads_seqtk_position_qual.fq2.txt && \n"
	sl += seqtk + " fqchk " + sampleProcess + sample + "_clean_unpair.fq1.gz>" + \
 		  sampleProcess + sample + "_clean_unpair_reads_seqtk_position_qual.fq1.txt && \n"
	sl += seqtk + " fqchk " + sampleProcess + sample + "_clean_unpair.fq2.gz>" + \
		  sampleProcess + sample + "_clean_unpair_reads_seqtk_position_qual.fq2.txt && \n"
	pipe.creat_shell(sl, sampleShell + "FilterData_"+sample + ".sh", pars['rm'])
	return sampleShell + "FilterData_" + sample + ".sh"


if __name__ == "__main__":
	pars = read_params(sys.argv)
	outdir = basic.outdir(pars['outdir'])
	basic.mkdir([outdir])
	samples = pd.read_csv(pars['rawData_list'], sep="\t", header=0, index_col=0)
	samples.index = [str(i) for i in samples.index]
#	samples = basic.parse_data(pars['rawData_list'])
	basic.mkdir([outdir + "/shell", outdir + "/process", outdir + "/list",
				outdir + "/shell/Filter_trimmomatic",outdir+"/process/Filter_trimmomatic"])
	softwares = basic.parse_config(os.path.dirname(sys.argv[0]) + "/softwares.txt")
	process = outdir + "/process/Filter_trimmomatic/"
	filterStat_script = stat_trimmomatic_filter_result(process,
													   outdir + "/shell/Filter_trimmomatic/", 
													   pars['readlength'], pars['rm'])
	with open(outdir + "/list/Filter_trimmomatic_dependancy.list", "w") as dep, open(process+"trimmomatic.log.list","w") as log, open(process+"trimmomatic.stat.list", "w") as stat, open(process + "CleanReads.list", "w") as fqslist:
		fqslist.write("#Sample\tFQ1\tFQ2\n")
		for sample in samples.index:
			sampleProcess = outdir + "/process/Filter_trimmomatic/" + sample + "/"
			sampleShell = outdir + "/shell/Filter_trimmomatic/" + sample + "/"
			basic.mkdir([sampleShell, sampleProcess])
			log.write(sample + "\t" + sampleProcess + sample + "_trimmomatic.log\n")
			stat.write(sample + "\t" + sampleProcess + sample + "_trimmomatic.stat\n")
			fqslist.write(sample + "\t" +sampleProcess+sample + "_clean_pair.fq1.gz\t" +
						  sampleProcess + sample + "_clean_pair.fq2.gz\n")
			fqFilter_script = trimmomatic_filter(
												 sampleShell, sampleProcess, sample, 
												 samples.loc[sample], pars, softwares)
			dep.write(fqFilter_script + ":2G\t"+filterStat_script+":10G\n")
		
	with open(outdir + "/list/Filter_trimmomatic_qsub.sh", "w") as qsub:
		qsub.write("/ifshk4/BC_PUB/biosoft/PIPE_RD/Package/pymonitor/monitor taskmonitor" +
				   " -P " + pars['project'] +
				   " -q " + pars['queue'] +
				   " -p " + pars['project'] + "_Filter_trimmomatic" +
				   " -i " + outdir + "/list/Filter_trimmomatic_dependancy.list\n")


