# -*- coding:utf-8 -*-

from setuptools import setup, find_packages
import os
from readtrim.version import Version

setup(
	name = 'ReadTrim',
	description = 'Read trimming and qc workflow.',
	version = Version.get_version(),
	url = 'https://github.com/jlli6t/ReadTrim',
	author = 'Jie Li',
	author_email = 'mm.jlli6t@gmail.com',
	maintainer = 'Jie Li',
	maintainer_email = 'mm.jlli6t@gmail.com',

	long_description=Version.long_description(),
	long_description_content_type='markdown',

	classifiers = [
				'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
				'Programming Language :: Python :: 3 :: Only',
				'Operating System :: Unix',
		],
	keywords = 'biology bioinformatics',
	scripts=['bin/readtrim_wf'],
	packages = find_packages(),
	include_package_data=True,
	python_requires = '>=3.6',
	install_requires=['biosut>=2.1.0',],
)
