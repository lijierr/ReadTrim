#!/usr/bin/env python
#coding:utf-8

###============================================================
#Contact: Jie Li (jeveylijie@gmail.com)
#v1.0	20170502	Use Trimmomatic to process raw reads
#					Use seqtk to stat and process clean reads
#					then you get high quality PE reads
#
#v1.1	20180420	Modified the input rawdata list format
#v2.0	20180420	remove --adapters arguments, adding adapters to --rawData_list, add option of removing duplications
#		20181122	add fastqc result after trimmomatic
#		20190306	add unpaired fq files to the output list
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

def read_paras(args):
	p = ap.ArgumentParser(description=__doc__)
	g = p.add_argument_group("Required arguments")
	ars = g.add_argument
	ars("--rawData_list", dest="rawData_list", required=True,
		help="raw reads list file with header,SampleName<tab>FQ1<tab>FQ2<tab>Adapter, \
			 if you want to merge fq1s then \
			 SampleName<tab>fq1,fq1<tab>fq2,fq2<Tab>Adapter,\
			 if you have two adps, then name\tq1\tq2\ta1,a2\n")
	ars("--read_length", dest="readlength", default="100",
		help="raw read length, [100]")
	ars("--minlength", dest="minlength", default=75,
		help="minimum length of read to keep, [75]")
	ars("--sliding_window", dest="sliding_window", default="4:20",
		help="windowSize:average_quality_required, [4:20]")
	ars("--phred", dest="phred", default="33",
		help="phred, 33 or 64, [33]")
#	ars("--adapters", dest="adapters", required=True,
#		help="adapters sequences file")
	ars("--adapters_paras", dest="adapters_paras", default="2:30:10",
		help="params for adapters, seedMismatchs:palindromeClipThreshold:simpleClipThreshold [2:30:10]")
	ars("--duplicates", dest="duplicates", action="store_true",
		help="set if you want to remove duplicates")

	g = p.add_argument_group("Optional arguments")
	ars = g.add_argument
#	ars("--project", dest="project", default="mytest",
#		help="project to qsub tasks [mytest]")
#	ars("--queue", dest="queue", default="bc.q",
#		help="queue to qsub tasks, [bc.q]")
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
	ars("--qsubs", dest="qsubs", default="select=1:ncpus=2:mem=5GB",
		help="default is select=1:ncpus=2:mem=5GB")
	ars("--walltime", dest="walltime", default="00:60:00",
		help="walltime for mission to submmit [00:60:00]")
	return vars(p.parse_args())

class Trimmomatic_filter:
	def __init__(self, sample, softwares, process, shell, result, fqs_info,
				 threads, phred, adapters_paras, leading, trailing,
				 sliding_window, minlength, rm, qsubs, walltime, dup):
		self.sample = sample
		self.softwares = softwares
		self.seqtk = self.softwares['seqtk']
		self.trimmomatic = self.softwares['trimmomatic']
		self.java = self.softwares['java']
		self.uniq = self.softwares['fastuniq']
		self.fastqc = self.softwares['fastqc']
		self.process = process
		self.shell = shell + "/Filter_"+self.sample + ".sh"
		self.result = result
		self.fqs_info = fqs_info
		self.threads = threads
		self.phred = phred
		self.adapters_paras = adapters_paras
		self.leading = leading
		self.trailing = trailing
		self.sliding_window = sliding_window
		self.minlength = minlength
		self.rm = rm
		self.qsubs = qsubs
		self.walltime = walltime
		self.dup = dup
		

	def filter(self):
		self.parse_fqs_info()
		self.q1 = self.process + "raw_" + self.sample + "_1.fastq.gz"
		if len(self.fqs[0]) == 1:
			sl = "ln -sf " + self.fqs[0][0] + " " + self.q1 + " &&\n"
		else:
			sl = "zcat " + " ".join(self.fqs[0])+"|gzip>" + self.q1+" &&\n"

		sl += self.seqtk + " fqchk " + \
			  self.q1 + ">" + \
		 	  self.process + "raw_reads_seqtk_position_qual_fq1.txt &&\n"
		self.all_fqs = [self.q1, self.process + self.sample+"_Clean.fastq.gz"]
		self.seq_type = " SE"
		if len(self.fqs) == 2:
			self.q2=self.process+"raw_"+self.sample+"_2.fastq.gz"
			if len(self.fqs[1]) == 1:
				sl += "ln -sf " + self.fqs[1][0] + " " + self.q2+" &&\n"
			else:
				sl += "zcat " + " ".join(self.fqs[1]) +"|gzip>"+self.q2+" &&\n"
			if self.dup:
				sl += "gzip -fd " + self.q1 + " &&\n"
				sl += "gzip -fd " + self.q2 + " &&\n"
				with open(self.process + "fq.list", "w") as fq_list_out:
					fq_list_out.write(self.process + "raw_"+self.sample+"_1.fastq\n"+
									  self.process + "raw_"+self.sample+"_2.fastq\n")
					#fq_list_out.write(self.q1 + "\n" + self.q2 + "\n")
				self.q1 = self.process + self.sample + "_rm_dup_1.fastq"
				self.q2 = self.process + self.sample + "_rm_dup_2.fastq"
				sl += self.uniq + \
					  " -i " + self.process + "fq.list" +\
					  " -t q" +\
					  " -o " + self.q1 + \
					  " -p " + self.q2 + " &&\n"
				self.remove_dup_log = self.process + self.sample + "remove_duplicates.log"
				sl += "gzip " + self.process + "raw_"+self.sample+"_1.fastq &&\n"
				sl += "gzip " + self.process + "raw_"+self.sample +"_2.fastq &&\n"
				sl += "gzip " + self.q1 + " &&\n"
				sl += "gzip " + self.q2 + " &&\n"
				self.q1 = self.q1 + ".gz"
				self.q2 = self.q2 + ".gz"
				sl += "num2=`zcat " + self.q1 + "|wc -l`\n"
				sl += "num1=`zcat " + self.process +"raw_"+self.sample+"_1.fastq.gz|wc -l`\n"
				sl += "((num1=$num1/2))\n"
				sl += "((num2=$num2/2))\n"
				sl += "echo \"raw_data_size:$num1\">"+self.remove_dup_log + " &&\n"
				sl += "echo \"data_size_after_rm_dup:$num2\">>"+self.remove_dup_log + " &&\n"
				sl += "((dup_num=$num1-$num2))\n"
				sl += "((dup_ratio=100*$dup_num/$num1))\n"
				sl += "echo \"duplicated_num:$dup_num\">>" +self.remove_dup_log + " &&\n"
				sl += "echo \"duplicated_ratio:$dup_ratio\">>" +self.remove_dup_log + " &&\n"
			sl += self.seqtk + " fqchk " + \
				  self.q2 + ">" +\
				  self.process + "raw_reads_seqtk_position_qual_fq2.txt &&\n"
			self.all_fqs = [self.q1, self.q2, 
							self.process + self.sample+"_Clean_Pair_1.fastq.gz",
							self.process + self.sample+"_Clean_Unpair_1.fastq.gz",
							self.process + self.sample+"_Clean_Pair_2.fastq.gz",
							self.process + self.sample+"_Clean_Unpair_2.fastq.gz"]
			self.seq_type = " PE"
		ILLUMINACLIP = " ILLUMINACLIP:" + self.process + "adapter.txt:" +self.adapters_paras if self.adapter else " "
		sl += self.java + " -jar " + self.trimmomatic + \
			  self.seq_type + \
			  " -threads " + self.threads + \
			  " -phred" + self.phred +\
			  " -trimlog " + self.process + self.sample + "_trimmomatic.log" + \
			  " " + " ".join(self.all_fqs) + \
			  ILLUMINACLIP + \
			  " LEADING:" + self.leading +\
			  " TRAILING:" + self.trailing +\
			  " SLIDINGWINDOW:" + self.sliding_window +\
			  " MINLEN:" + self.minlength + \
			  " 2>" +self.process + self.sample+"_trimmomatic.stat &&\n"
		for fq in self.all_fqs:
			sl += self.seqtk + " fqchk " + fq + \
				  ">"+fq +"_seqtk_position_qual.fq1.txt &&\n"
		sl += "mv " + self.process + "*.fastq.gz " + self.result + " &&\n"
		a_ = " -a " + self.process + "adapter.txt" if self.adapter else " "
		sl += self.fastqc + \
			  a_ + \
			  " -o " + self.process + " " +\
			  self.result + self.sample + "_Clean_Pair_1.fastq.gz " + \
			  self.result + self.sample + "_Clean_Pair_2.fastq.gz &&\n"
		for i in ['_1_', '_2_']:
			sl += "unzip -u -d " + self.process + \
				  " "+self.process + self.sample + "_Clean_Pair"+i +"fastqc.zip &&\n"
			sl += "cp " + self.process +self.sample+"_Clean_Pair"+i+"fastqc/Images/per_base_quality.png " + self.result + self.sample + i+"per_base_quality.png &&\n"
			sl += "cp " + self.process +self.sample+"_Clean_Pair"+i+"fastqc/Images/duplication_levels.png " + self.result+self.sample + i+"duplication_levels.png &&\n"
			sl += "cp "+self.process+self.sample+"_Clean_Pair"+i+"fastqc/Images/per_base_sequence_content.png "+self.result +self.sample+i+"per_base_sequence_content.png &&\n"		  
		pipe.creat_shell(sl, self.shell, self.rm,self.qsubs, self.walltime)


	def parse_fqs_info(self):
		self.fqs = [self.fqs_info[0].split(",")]
		if len(self.fqs_info)>1:self.fqs.append(self.fqs_info[1].split(","))
		if len(self.fqs_info)>=3:
			self.adapter = self.fqs_info[2].split(",")
			with open(self.process + "adapter.txt", "w") as adp:
				if len(self.adapter) == 1:
					adp.write(">Adapter_1\n"+self.adapter[0]+"\n")
				else:
					adp.write(">PrefixPE/1\n" + self.adapter[0]+"\n"+
							  ">PrefixPE/2\n" + self.adapter[1]+"\n")
		else:
			self.adapter = None
	#def remove_duplication(self):
		

def stat_trimmomatic_filter_result(process, shell, result, 
								   lenth, rm, softwares, bin_):
	shell = shell + "Stat_trimmomatic_filter_result.sh"
	sl = softwares['python36']+" "+bin_ +"stat_trimmomatic_from_log-v1.0.py" + \
		 " --trimmomatic_log_list " + process + "trimmomatic.log.list" + \
		 " --trimmomatic_stat_list " + process + "trimmomatic.stat.list" + \
		 " --read_length " + str(lenth) + \
		 " --out_stat_file " + process + "All_filter_stat.xls &&\n"
	sl += "cp " +process + "All_filter_stat.xls " + result + " &&\n"
	pipe.creat_shell(sl, shell, rm, "select=1:ncpus=2:mem=3GB", "00:30:00")

if __name__ == "__main__":
	pars = read_paras(sys.argv)
	outdir = basic.outdir(pars['outdir']) + "/"
	process = outdir + "process/Filter_Trimmomatic/"
	shell = outdir + "shell/Filter_Trimmomatic/"
	result = outdir + "result/Filter_Trimmomatic/"
	basic.mkdir([outdir, outdir + "process", outdir + "shell",
				outdir +"result", process, shell, result])
	samples = pd.read_csv(pars['rawData_list'], sep="\t", header=0, index_col=0)
	samples.index = [str(i) for i in samples.index] ## incase samplenames are nums
	bin_ = os.path.dirname(sys.argv[0]) + "/"
	softwares = basic.parse_config(bin_ + "/softwares.txt")
	with open(process+"trimmomatic.log.list","w") as log, open(process+"trimmomatic.stat.list", "w") as stat, open(process + "CleanReads.list", "w") as fqslist:
#	with open(process + "CleanReads.list", "w") as fqslist:
		fqslist.write("#Sample\tFQ1\tFQ2\tUnpairReads\n")
		for sample in samples.index:
			samProcess = process + sample + "/"
			samResult = result + sample + "/"
			basic.mkdir([samProcess, samResult])
			log.write(sample + "\t"+samProcess + sample+"_trimmomatic.log\n")
			stat.write(sample + "\t" +samProcess +sample+ "_trimmomatic.stat\n")
			fqslist.write(sample+"\t"+samResult+sample+"_Clean_Pair_1.fastq.gz\t" +
						  samResult + sample + "_Clean_Pair_2.fastq.gz\t" +
						  samResult + sample + "_Clean_Unpair_1.fastq.gz," +
						  samResult + sample + "_Clean_Unpair_2.fastq.gz\n")
			trimm_filter =Trimmomatic_filter(sample, softwares, samProcess, shell,
											 samResult, samples.loc[sample], 
											 pars['threads'], pars['phred'],
											 pars['adapters_paras'], 
											 pars['leading'], pars['trailing'],
											 pars['sliding_window'], pars['minlength'],
											 pars['rm'], pars['qsubs'], pars['walltime'],
											 pars['duplicates'])
			trimm_filter.filter()
	stat_trimmomatic_filter_result(process, shell, 
								   result, pars['readlength'],
								   pars['rm'], softwares, bin_)

