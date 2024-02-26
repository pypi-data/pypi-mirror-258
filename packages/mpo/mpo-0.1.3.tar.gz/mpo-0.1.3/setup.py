# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import codecs
import os.path

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md") as f:
    long_description = f.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")
    
def get_author(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__author__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find author string.")


setup(
    name="mpo",
    version= get_version('mpo/version.py'),
    description="MPO is a library for Python to map models between PrestaShop and odoo .",
    license="GNU GPL-3",
    author=get_author('mpo/version.py'),
    author_email="jemiaymen@gmail.com",
    url="https://github.com/AISYSNEXT-Ltd/mpo",
    packages=find_packages(),
    install_requires=required,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Internet",
    ],
    keywords=['prestashop','e-com','e-commerce','prestashop api','api','webservice' , 'mapper' , 'odoo']
)
