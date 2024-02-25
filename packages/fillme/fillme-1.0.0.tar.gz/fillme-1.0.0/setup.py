#!/usr/bin/env python

from setuptools import setup

with open('README.md', 'r') as fh:
    readme = fh.read()

# with open('requirements.txt', 'r') as f:
#     requirements = f.read().splitlines()

VERSION = '1.0.0'

setup(
    name='fillme',
    version=VERSION,
    description='A lightweight library to generate dummy data for database using OpenAI',
    long_description=readme,
    author='Soheil Dolatabadi',
    author_email='soheildolat@gmail.com',
    packages=['fillme'],
    install_requires=[
        "openai==1.12.0",
        "sqlalchemy==2.0.27"
    ]
)
