#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(name='slisonner',
      version='0.7.9',
      description='Habidatum Platform Slison encode/decode utility',
      long_description='',
      author='Nikita Pestrov',
      author_email='nikita.pestrov@habidatum.com',
      maintainer='Nikita Pestrov',
      maintainer_email='nikita.pestrov@habidatum.com',
      packages=find_packages(),
      install_requires=requirements,
      platforms='any',
      classifiers=['Programming Language :: Python :: 3.4'])
