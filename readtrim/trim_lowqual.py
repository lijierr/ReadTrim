"""
The :mod:`readtrim.trim_lowqual` trim low quality bases from reads.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GNU v3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

from loguru import logger

from biosut import gt_exe, gt_file, gt_path

class trim_lowqual:

	def __init__(self, infq1:str=None, infq2:str=None, \
				slide_wd:str='4:20', minlen:int=75, croplen=None, \
				outdir='./', phred:int=33, ncpu:int=20, basename:str='Test'):
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
        basename : str, default is Test.
            basename of this data.
        """

		self.infq1 = infq1
		self.infq2 = infq2
		self.slide_wd = slide_wd
		self.minlen = minlen
		self.croplen = croplen
		self.outdir = outdir
		self.phred = phred
		self.ncpu = ncpu
		self.basename = basename

		gt_file.check_file_exist(self.infq1, self.infq2, check_empty=True)

		self.prefix = gt_file.get_seqfile_prefix(self.infq1)

        # init these variable here, to escape that each tool init once.
		#self.outfq1 = f'{self.prefix}.trim.1.fq.gz'
		#self.outfq2 = f'{self.prefix}.trim.2.fq.gz'
		#self.outfq1_un = f'{self.prefix}.trim.unpair.1.fq.gz'
		#self.outfq2_un = f'{self.prefix}.trim.unpair.2.fq.gz'
		#self.outfq_un = f'{self.prefix}.trim.unpair.fq.gz'
        ######

		#if 'TRIM_JAR' not in os.environ:
		#	sys.exit('trimmomatic is not found, please make sure you have TRIM_JAR=/path/to/trimmomatic_jar/trimmomatic-xxx.jar')

	def trimmomatic(self):
        ## don't know how to add jar
		trim_jar = '/90days/s4506266/softwares/Trimmomatic-0.39/trimmomatic-0.39.jar'
		outdir = gt_path.sure_path_exist( \
                        self.outdir, \
                        f'{self.outdir}/trimmomatic',\
                        f'{self.outdir}/trimmomatic/{self.basename}' \
                        )[2]

		self.outfq1 = f'{outdir}/{self.prefix}.trim.1.fq.gz'
		self.outfq2 = f'{outdir}/{self.prefix}.trim.2.fq.gz'
		self.outfq1_un = f'{outdir}/{self.prefix}.trim.unpair.1.fq.gz'
		self.outfq2_un = f'{outdir}/{self.prefix}.trim.unpair.2.fq.gz'
		self.outfq_un = f'{outdir}/{self.prefix}.trim.unpair.fq.gz'
		crop = self.croplen and f'CROP:{self.croplen}' or ''
		#f'CROP:{self.croplen}' if self.croplen else ''
		print(f'crop: {crop}')
		cmd = f'java -jar {trim_jar} PE -threads {self.ncpu} -phred{self.phred} \
			-trimlog {outdir}/trimmomatic.log {self.infq1} {self.infq2} \
			{self.outfq1} {self.outfq1_un} {self.outfq2} {self.outfq2_un} \
			LEADING:25 TRAILING:20 SLIDINGWINDOW:{self.slide_wd} \
			MINLEN:{self.minlen} {crop} 2>{outdir}/trimmomatic.stat'

		logger.info(f'Start to trim reads using trimmomatic, command is {cmd}.')
		gt_exe.exe_cmd(cmd, shell=True)

		gt_file.check_file_exist(f'{outdir}/trimmomatic.stat', check_empty=True)

        ## zcat unpaired together
		cmd = f'zcat {self.outfq1_un} {self.outfq2_un}|gzip>{self.outfq_un}'
		gt_exe.exe_cmd(cmd, shell=True)
		logger.info('Finished trim reads.')
		return self.outfq1, self.outfq2,
