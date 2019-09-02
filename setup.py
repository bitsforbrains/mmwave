#!/usr/bin/env python

from os.path import exists
from setuptools import setup

packages = ['mmwave']

tests = [p + '.tests' for p in packages]


setup(name='mmwave',
      version='0.1.1',
      description='Module for capturing/processing MMWave data from the TI DCA1000EVM Data Capture Card',
      url='https://github.com/bitsforbrains/mmwave.git',
      maintainer='Aaron Finney',
      maintainer_email='20goto10@bitsforbrains.io',
      packages=packages + tests,
      python_requires='>=2.7',
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      install_requires=list(open('requirements.txt').read().strip().split('\n')),
      zip_safe=False)
