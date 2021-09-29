# Archive

This repo was archived, is has been integrated into [ReadTrim](https://github.com/jlli6t/ReadTrim.git).


# Filter_Trimmomatic

## Introduction
**Filter_Trimmomatic** is a module which used for Illumina raw sequencing data QC and trimming.

## Installation
No need to install, just clone and then use it.

## Help page
Use Trimmomatic to process raw reads, Use seqtk to stat and process clean reads, then you get high quality PE reads.

--rawData_list	raw reads list file with header,SampleName<tab>FQ1<tab>FQ2<tab>Adapter,if you want to merge fq1s then, SampleName<tab>fq1,fq1<tab>fq2,fq2<Tab>Adapter, if you have two adps, then name\tq1\tq2\ta1,a2
--read_length	raw read length, [100]
--sliding_window	windowSize:average_quality_required, [4:20]
--phred	phred, 33 or 64, [33]
--adapters	adapters sequences file
--adapters_paras	params for adapters, seedMismatchs:palindromeClipThreshold:simpleClipThreshold [2:30:10]
--duplicates	set if you want to remove duplicates

## Usage
This is a demo of usage
python3 Filter_trimmomatic-1.2.py --rawData_list fq_DNA.list --read_length 151 --minlength 75 --phred 33 --adapters adapters.txt --sliding_window 6:20 --outdir /home/1.Filter


## Copyright
Copyright 2017-2018 Jie Li. See LICENSE for further details.

