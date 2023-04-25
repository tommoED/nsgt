#! /usr/bin/env python
# -*- coding: utf-8

"""
Python implementation of Non-Stationary Gabor Transform (NSGT)
derived from MATLAB code by NUHAG, University of Vienna, Austria

Thomas Grill, 2011-2017
http://grrrr.org/nsgt

Austrian Research Institute for Artificial Intelligence (OFAI)
AudioMiner project, supported by Vienna Science and Technology Fund (WWTF)

covered by the Artistic License 2.0
http://www.perlfoundation.org/artistic_license_2_0

--

Installation:

In the console (terminal application) change to the folder containing this readme.txt file.

To build the package run the following command:
python setup.py build

To install the package (with administrator rights):
sudo python setup.py install

--

Attention: some Cython versions also need the Pyrex module installed!

"""

import warnings
import os

from setuptools import setup
from setuptools import Extension

import numpy


setup_options = {}
setup_options['test_suite'] = 'tests'

ext_modules = [
    Extension(
        "nsgt._nsgtf_loop",
        sources=["nsgt/nsgtf_loop.pyx"],
        include_dirs=[numpy.get_include()],
    ),
    Extension(
        "nsgt._nsigtf_loop",
        sources=["nsgt/nsigtf_loop.pyx"],
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    ext_modules = ext_modules,
    **setup_options
)
