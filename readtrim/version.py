"""
The :mod:`readtrim.version` printing version information.
"""

# Author: Jie Li <mm.jlli6t@gmail.com>
# License: GNU v3.0
# Copyrigth: 2020

import os
from biosut.gt_path import abs_path

class Version:

    def get_version():
        ver1 = os.path.dirname(abs_path(__file__)) + '/version'
        ver2 = os.path.dirname(abs_path(__file__)) + '/../version'
        if os.path.isfile(ver1):return open(ver1).readline().strip()
        if os.path.isfile(ver2):return open(ver2).readline().strip()
        return 'Unknow version'

    @classmethod
    def show_version(cls):
        ver = cls.get_version()
        name = os.path.split(os.path.dirname(__file__))[1]
        print('\n\n\t\t%s version * %s *\n\n' % (name, ver))

    def long_description():
		readme1 = join(f_dir, 'README.md')
		readme2 = join(f_dir, '/../README.md')
		if isfile(readme1):return open(readme1).read()
		if isfile(readme2):return open(readme2).read()
		return "No detailed description"
