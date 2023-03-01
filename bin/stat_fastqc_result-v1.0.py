#coding:utf-8

import sys
import argparse
import pandas as pd
import os
import re

def read_pars(args):
	p = argparse.ArgumentParser(description="stat of FastQC result\n")
	ars = p.add_argument
	ars("--fqlist", dest="fqlist", required=True,
		help="fqlist file, with header, sampleName<tab>q1<tab>q2")
	ars("--FastQC_dir", dest="FastQC_dir", required=True,
		help="process FastQC dir of your project")
	ars("--outfile", dest="outfile", required=True,
		help="output stat file")
	return vars(p.parse_args())

def grep_key(stats, sample, key, fastqc_datas):
	tmp = []
	for i in fastqc_datas:
		print(i)
		print(key)
		#sys.exit()
		grep_result = os.popen('grep "'+key+'" '+i).read().split("\n")[0].split("\t")[1]
		tmp.append(grep_result)
	if len(set(tmp)) == 1:
		return tmp[0]
	else:
		return ",".join(tmp)
	


def stat_fastqc(samples, FastQC_dir, outfile):
	stats = {}
	for sample in samples.index:
		stats[sample] = {}
		fqs = list(samples.loc[sample])
		oriname1 = ".".join(os.path.basename(fqs[0]).split(".")[:-2])
		oriname2 = ".".join(os.path.basename(fqs[1]).split(".")[:-2])
		sample_dir = FastQC_dir + "/" + sample + "/"
		r1_fastqc_data = sample_dir + oriname1 + "_fastqc/fastqc_data.txt"
		r2_fastqc_data = sample_dir + oriname2 + "_fastqc/fastqc_data.txt"
		fastqc_datas = [r1_fastqc_data, r2_fastqc_data]
		for i in ["Encoding", "Total Sequences", "Sequence length", "%GC"]:
			stats[sample][i] = grep_key(stats,sample,i,[r1_fastqc_data,r2_fastqc_data])
	stats = pd.DataFrame.from_dict(stats, orient="index")
	print(stats)
	read_lengths = stats['Sequence length'].apply(lambda x: int(x.split("-")[1]) if re.search('-', x) else int(x))
	stats['Total Sequences'] = 2*stats['Total Sequences'].apply(int)
	stats['TotalBase(G)'] = stats['Total Sequences']*read_lengths/1000000000
	stats.to_csv(outfile, sep="\t")


if __name__ == "__main__":
	pars = read_pars(sys.argv)
	samples = pd.read_csv(pars['fqlist'], sep="\t", header=0, index_col=0)
	stat_fastqc(samples, pars['FastQC_dir'], pars['outfile'])


