#!/usr/bin/env python
from __future__ import print_function

import os
import re
import setuptools

from pythontail import pythontail as module

# project long description
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(BASE_PATH, 'README.md'), "r") as file:
    long_description = file.read()

setuptools.setup(
    name=module.__project__,
    version=module.__version__,
    author=module.__author__,
    author_email=module.__authoremail__,
    description=module.short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=module.__source__,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)