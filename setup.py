#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='toolbox',
      version='v0.1',
      author='Johnny Greco',
      author_email='jgreco@astro.princeton.edu',
      packages=['toolbox'],
      url='https://github.com/johnnygreco/toolbox',
      description='random tools')
