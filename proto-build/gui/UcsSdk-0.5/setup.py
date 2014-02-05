#!/usr/bin/python

import sys
import os
from distutils.core import setup

name='UcsSdk'

def is_package(path):
	return (
			os.path.isdir(path) and
			os.path.isfile(os.path.join(path, '__init__.py'))
			)

def find_packages(path, base="" ):
	packages = {}
	for item in os.listdir(path):
		dir = os.path.join(path, item)
		if is_package( dir ):
			if base:
				module_name = "%(base)s.%(item)s" % vars()
			else:
				module_name = item
			packages[module_name] = dir
			packages.update(find_packages(dir, module_name))
	return packages

setup(
	name=name,
	version='0.5',
	description='Python SDK for Cisco UCS Manager',
	author='Cisco Systems',
	author_email='',
	long_description='Install Instructions: sudo python setup.py install',
	packages=find_packages('src'),
	package_dir = {'': 'src'},
	namespace_packages=['UcsSdk'],
	package_data={'': ['resources/*.xml']},
	include_package_data = True,
	zip_safe = False,
	)
