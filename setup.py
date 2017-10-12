#!/usr/bin/env python3

from setuptools import setup, find_packages


requirements = ['lz4tools==1.3.1.2',
'numpy',
'py==1.4.31',
'pytest==3.0.3']

setup(name='slisonner',
      version='0.7.9',
      description='Habidatum Chronotope Slison encode/decode utility',
      long_description='',
      author='Nikita Pestrov',
      author_email='nikita.pestrov@habidatum.com',
      maintainer='Nikita Pestrov',
      maintainer_email='nikita.pestrov@habidatum.com',
      packages=find_packages(),
      install_requires=requirements,
      platforms='any',
      classifiers=['Programming Language :: Python :: 3.4'])
