#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import os
import requests
from setuptools import setup, find_packages
import fincookie

# Package meta-data.
NAME = 'fincookie'
DESCRIPTION = '大智慧远程获取Cookies集群API'
URL = 'https://gitee.com/yl153977/finchina-remote-cookies'
EMAIL = 'huyl3@finchina.com'
AUTHOR = '胡永乐'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = fincookie.__version__

# What packages are required for this module to be executed?
REQUIRED = [
    'requests'
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with open('README.md', 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(include=['fincookie']),
    package_dir={'fincookie': 'fincookie'},
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='Apache 2.0',
    classifiers=[
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
