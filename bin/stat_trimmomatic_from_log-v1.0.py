#!
#coding:utf-8

#==============================================================
#Contact: Jie Li (jeveyliji@gmail.com)
#v1.0	20170405	Use this script to stat result of trimmomatic

#==============================================================


from __future__ import division
import sys
import argparse as ap
import pandas as pd
#from contextlib import nested
import re

def read_params(args):
	p = ap.ArgumentParser(description=__doc__)
	g = p.add_argument_group("Required arguments")
	ars = g.add_argument
	ars("--trimmomatic_log_list", dest="trimmomatic_log_list", required=True,
		help="trimmomatic output log file list, Name\tlog")
	ars("--trimmomatic_stat_list", dest="trimmomatic_stat_list", required=True,
		help="trimmomatic stat info file list, Name\tstat, same order as log list")
	ars("--read_length", dest="read_length", required=True, type=int,
		help="read length")
	ars("--out_stat_file", dest="out_stat_file", required=True,
		help="output stat file name")
	ars("--chunk_size", dest="chunk_size", default=10000000, type=int,
		help="chunk size for python to read.[10000000]")
	return vars(p.parse_args())


if __name__ == "__main__":
	pars = read_params(sys.argv)
	log_list, stat_list = pars['trimmomatic_log_list'], pars['trimmomatic_stat_list']
	log_dict, stats_dict = {}, {}
	with open(pars['out_stat_file'], "w") as ot, open(pars['out_stat_file']+'_simple.xls', "w") as ots: # Jie, add simple output 20200301
		ot.write("SampleName\tRawDataSize(Gb)\tRawReadPair\tCleanDataSize(Gb)\tCleanReadPair\tCleanForwardRead\tCleanReverseRead\t"
				 "CleanReadPair/RawReadPair(%)\tTotalCleanRead/RawRead(%)\tCleanBP/RawBP(%)\t#TotalReads\n")
		ots.write("SampleName\tRawDataSize(Gb)\tCleanDataSize(Gb)\tCleanReadPair/RawReadPair(%)\tCleanBP/RawBP(%)\t#TotalReads\n")
		with open(log_list) as logs, open(stat_list) as stats:
#		with nested(open(log_list), open(stat_list)) as (logs, stats):
			for log in logs:
				log = log.strip().split("\t")
				stat = stats.readline()
				reader = pd.read_csv(log[1], index_col=0, header=None, sep=" ", iterator=True)
				chunks = []
				loop = True
				while loop:
					try:
						chunk = reader.get_chunk(pars['chunk_size'])
						chunks.append(chunk)
					except StopIteration:
						loop = False
						sys.stderr.write("Finished reading matrix!\n")
				bp_info = pd.concat(chunks, ignore_index=True)
				clean_bp = int(sum(bp_info.iloc[:,len(bp_info.columns)-3]))
				total_bp = int(pars['read_length']) * len(bp_info)
#				log_dict[log[0]] = clean_bp * 100/float(total_bp)
#				stats_dict[stat[0]] = re.findall('[0-9]{1,2}.[0-9]{2}', stat[1].readlines()[-2])
				stat = re.findall('(\d+) \(?', open(stat.strip().split("\t")[1]).readlines()[-2])
#				print(stat)
				ot.write(log[0] + "\t" + str(round(total_bp/float(1000000000),2))+"\t" + stat[0] + "\t" + str(round(clean_bp/float(1000000000), 2))+"\t" +stat[1] + "\t" + stat[2] + "\t" + stat[3] + "\t" + 
						 str(round(int(stat[1])*100/float(stat[0]), 2)) + "\t" + 
						 str(round((int(stat[1])*2+int(stat[2])+int(stat[3]))*100/(int(stat[0])*2), 2)) + "\t" + 
						 str(round(clean_bp*100/total_bp, 2)) + "\t" + str(int(stat[1])*2+int(stat[2])+int(stat[3]))+"\n")
				ots.write(log[0] + "\t" + str(round(total_bp/float(1000000000),2))+"\t" + str(round(clean_bp/float(1000000000), 2))+ "\t" + str(round(int(stat[1])*100/float(stat[0]), 2)) + "\t" +str(round(clean_bp*100/total_bp, 2)) + "\t" + str(int(stat[1])*2+int(stat[2])+int(stat[3]))+"\n")
			

