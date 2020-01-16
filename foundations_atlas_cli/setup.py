"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__))
build_version = environ.get('build_version', '0.0.0')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='foundations-atlas-cli',
    version=build_version,
    description='Access foundations-sdk features through the command line interface',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'foundations-contrib=={}'.format(build_version),
        'foundations-internal=={}'.format(build_version),
        'foundations-events=={}'.format(build_version)
    ],
    packages=find_packages('src'),
    package_dir={'':'src'},
)