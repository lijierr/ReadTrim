#!/usr/bin/env python3
#coding:utf-8

"""
Use this to plot distribution of seqtk fqchk result.
quality distribution of each position on the read
"""

import os
import sys
import argparse as ap

def read_params(args):
	p = ap.ArgumentParser(description=__doc__)
	g = p.add_argument_group("Required arguments")
	ars = g.add_argument
	ars("--seqtk_fqchk_result", dest="seqtk_fqchk_result", required=True,
		help="seqtk fqchk result, that quality conditon of each position")
	ars("--out")

if __name__ == "__main__":
	pars = read_params(sys.argv)

