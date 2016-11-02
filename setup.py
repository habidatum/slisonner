#!/usr/bin/env python3

from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements('./requirements.txt')

reqs = [str(ir.req) for ir in install_reqs]

setup(name='slisonner',
      version='0.7.0',
      description='Habidatum Platform Slison encode/decode utility',
      long_description='',
      author='Nikita Pestrov',
      author_email='nikita.pestrov@habidatum.com',
      maintainer='Nikita Pestrov',
      maintainer_email='nikita.pestrov@habidatum.com',
      packages=find_packages(),
      install_requires=reqs,
      platforms='any',
      classifiers=['Programming Language :: Python :: 3.4'])
