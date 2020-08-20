"""
The :mod:`readtrim.version` print and show version information.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2019

from os.path import join, isfile, split, dirname
from biosut.gt_path import abs_path

class Version:
	f_dir = dirname(abs_path(__file__))
	@classmethod
	def get_version(cls):
		ver1 = join(cls.f_dir, 'version')
		ver2 = join(cls.f_dir + '../version')
		if isfile(ver1):return open(ver1).readline().strip()
		if isfile(ver2):return open(ver2).readline().strip()
		return 'Unknown verion'

	@classmethod
	def show_version(cls):
		ver = cls.get_version()
		name = split(dirname(__file__))[1]
		print('\n\n{:^80} version * {ver} *\n\n'.format(name, ver))

	@classmethod
	def long_description(cls):
		readme1 = join(cls.f_dir, 'README.md')
		readme2 = join(cls.f_dir, '/../README.md')
		if isfile(readme1):return open(readme1).read()
		if isfile(readme2):return open(readme2).read()
		return "No detailed description"
