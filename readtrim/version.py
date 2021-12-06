"""
The :mod:`readtrim.version` print and show version information.
"""

__author__ = 'Jie Li'
__copyright__ = 'Copyright 2018'
__credits__ = 'Jie Li'
__license__ = 'GPLv3.0'
__maintainer__ = 'Jie Li'
__email__ = 'jlli6t near gmail.com'

from os.path import join, isfile, split, dirname, abspath


class Version:
	f_dir = dirname(abspath(__file__))

	@classmethod
	def get_version(cls):
		ver1 = join(cls.f_dir, 'version')
		ver2 = join(cls.f_dir, '../version')
		if isfile(ver1): return open(ver1).readline().strip()
		if isfile(ver2): return open(ver2).readline().strip()
		return 'Unknown version'

	@classmethod
	def show_version(cls):
		ver = cls.get_version()
		name = split(dirname(__file__))[1]
		print('\n{:^40} version * {} *\n\n'.format(name, ver))

	@classmethod
	def long_description(cls):
		readme1 = join(cls.f_dir, 'README.md')
		readme2 = join(cls.f_dir, '/../README.md')
		if isfile(readme1): return open(readme1).read()
		if isfile(readme2): return open(readme2).read()
		return 'No detailed description'
