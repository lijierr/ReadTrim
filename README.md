# Archive

This repo was archived, it has been integrated into [ReadTrim](https://github.com/jlli6t/ReadTrim.git).

# FastQC

## Introduction
**FastQC** is a module which used for Illumina raw sequencing data QC.

## Installation
No need to install, just clone and then use it.

## Help page
Use FastQC to process raw reads, do FastQC of sequencing reads

--fqlist	fqlist file, with header, sampleName<tab>q1<tab>q2, abs path
--adapters	adapters, format name<tab>adapter seq
--outdir	outdir to output result, default is ./
--qsubs	arguments for qsub system, [select=1:ncpus=2:mem=2GB]
--walltime	walltime of your task to run [00:60:00]
--run	set if you want to run all scripts directly.
--arguments	other arguments you want to use for FastQC
--rm	set to rm *.sh.* files

## Usage
This is a demo of usage
python3 fastQC-v1.0.py --fqlist fq.list --outdir ./test

## Copyright
Copyright 2017-2018 Jie Li. See LICENSE for further details.

