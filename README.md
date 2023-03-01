
# ReadTrim
[![PyPI](https://shields.io/pypi/v/readtrim.svg)](https://pypi.org/project/readtrim)

## Introduction
**ReadTrim** is a workflow that I use for NGS reads trimming and QC.
The ReadTrim is open source and released under the [GNU General Public License (Version 3)](https://pypi.org/project/readtrim/).

## Documentation
Installation and usage refer to [document](docs/documentation.md)

## Installation
Install readtrim through pip3:
```
pip3 install readtrim
```

## Bugs
For any bugs or problems please use [Issue](https://github.com/jlli6t/ReadTrim/issues) portal.

## Copyright
Copyright 2018-2019 Jie Li. See [LICENSE](./LICENSE) for further details.
=======
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

