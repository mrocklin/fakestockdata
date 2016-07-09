#!/usr/bin/env python

from glob import glob
from os.path import exists
from setuptools import setup

setup(name='fakestockdata',
      version='0.0.1',
      description='Generate CSV data for stocks',
      url='http://github.com/mrocklin/fakestockdata/',
      maintainer='Matthew Rocklin',
      maintainer_email='mrocklin@gmail.com',
      license='BSD',
      keywords='',
      packages=['fakestockdata'],
      package_data={'fakestockdata': ['data/daily/*.bz2']},
      data_files = [('fakestockdata/daily', glob('data/daily/*'))],
      long_description=(open('README.rst').read() if exists('README.rst')
                        else ''),
      zip_safe=False)
