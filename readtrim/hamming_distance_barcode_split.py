import sys
import gzip
from Bio import SeqIO
import itertools

def hamming(str1, str2):
  return sum(itertools.imap(str.__ne__, str1, str2))

# print hamming("ATCTG","ATTGC")

def deal_dna_file(a,):
	dna_dict = {}
	for record in SeqIO.parse(a,"fasta"):
		dna_dict[record.id] = record.seq
	return dna_dict

A_DNA_file = sys.argv[1]

B_fastq_file = gzip.open(sys.argv[2],"r")
# B_fastq_file = open(sys.argv[2],"r")
dna_dict = deal_dna_file(A_DNA_file)
# print dna_dict

for record in SeqIO.parse(B_fastq_file, "fastq"):
	a = 0
	b = 0
	for k,v in dna_dict.items():
		if a >1:
			break
		if hamming(v,record.seq[:len(v)]) == 0:
			print record.seq
		elif hamming(v,record.seq[:len(v)]) == 1:
			a +=1
		elif hamming(v,record.seq[:len(v)]) ==2:
			b +=1
	print a,b
	if a == 1 and b > 1: # one barcode distance is 1 and more than one barcode distance are 2
		print record.seq
	if a == 1 and b == 0: # only barcode distance is 1. 
		print record.seq
	if a == 0 and b == 1: # only barcode distance are 2.
		print record.seq
