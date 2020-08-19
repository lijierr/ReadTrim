"""
The :mod:`readtrim.trim_lowqual` trim low quality bases from reads.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2019

import logging

logger = logging.getLogger(__name__)

from biosut import gt_exe, gt_file, gt_path

class trim_lowqual:

	def __init__(self, infq1:str=None, infq2:str=None, \
				slide_wd:str='4:20', minlen:int=75, outdir='./', \
				phred:int=33, ncpu:int=20, sample_name:str='Test'):
		"""
		Wrapper of trim low quality reads.

		Parameter
		---------
		infq1 : str
            Input pair end fastq 1 file.
        infq2 : str
            Input pair end fastq 2 file.
        slide_wd : str, default is 4:20
            Sliding window, former is window size, latter is base quality cutoff.
        minlen : int, default is 75.
            Minimum length, read with length below this will be discarded.
        outdir : str, default is current working directory.
            Output directory to output all results.
        phred : int, default is 33.
            Phred value of read base.
        ncpu : int, default is 20.
            Number of cpus to use.
        sample_name : str, default is Test.
            Sample name of this data.
        """

		self.infq1 = infq1
		self.infq2 = infq2
		self.slide_wd = slide_wd
		self.minlen = minlen
		self.outdir = outdir
		self.phred = phred
		self.ncpu = ncpu
		self.sample_name = sample_name

		gt_file.check_file_exist(self.infq1, self.infq2, check_empty=True)

		self.prefix = gt_file.get_seqfile_prefix(self.infq1)

        # init these variable here, to escape that each tool init once.
		self.outfq1 = '%s.trim.1.fq.gz' % self.prefix
		self.outfq2 = '%s.trim.2.fq.gz' % self.prefix
		self.outfq1_un = '%s.trim.unpair.1.fq.gz' % self.prefix
		self.outfq2_un = '%s.trim.unpair.2.fq.gz' % self.prefix
		self.outfq_un = '%s.trim.unpair.fq.gz' % self.prefix
        ######

		#if 'TRIM_JAR' not in os.environ:
		#	sys.exit('trimmomatic is not found, please make sure you have TRIM_JAR=/path/to/trimmomatic_jar/trimmomatic-xxx.jar')

	def trimmomatic(self):
        ## don't know how to add jar
		trim_jar = '/90days/s4506266/softwares/Trimmomatic-0.39/trimmomatic-0.39.jar'
		outdir = gt_path.sure_path_exist( \
                        self.outdir, \
                        '%s/trimmomatic' % self.outdir,\
                        '%s/trimmomatic/%s' % (self.outdir, self.sample_name) \
                        )[2]

		self.outfq1 = '%s/%s' % (outdir, self.outfq1)
		self.outfq2 = '%s/%s' % (outdir, self.outfq2)
		self.outfq1_un = '%s/%s' % (outdir, self.outfq1_un)
		self.outfq2_un = '%s/%s' % (outdir, self.outfq2_un)
		self.outfq_un = '%s/%s' % (outdir, self.outfq_un)

		cmd = 'java -jar %s PE -threads %d -phred%s -trimlog %s/trimmomatic.log \
			%s %s %s %s %s %s LEADING:25 TRAILING:20 \
			SLIDINGWINDOW:%s MINLEN:%d 2>%s/trimmomatic.stat' % \
			(trim_jar, self.ncpu, self.phred, outdir, \
			self.infq1, self.infq2, self.outfq1, self.outfq1_un, self.outfq2, self.outfq2_un, \
			self.slide_wd, self.minlen, outdir)
		gt_exe.exe_cmd(cmd, shell=True)

		gt_file.check_file_exist('%s/trimmomatic.stat' % outdir, check_empty=True)

        ## zcat unpaired together
		cmd = 'zcat %s %s|gzip>%s' % (self.outfq1_un, self.outfq2_un, self.outfq_un)
		gt_exe.exe_cmd(cmd, shell=True)

		return self.outfq1, self.outfq2,
