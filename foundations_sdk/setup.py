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
    name='dessa_foundations',
    version=build_version,
    description='A tool for machine learning development',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'dill==0.2.8.2',
        'redis==2.10.6',
        'pandas==0.23.3',
        'PyYAML==3.13',
        'promise==2.2.1',
        'pyarmor==5.2.3',
        'foundations_contrib=={}'.format(build_version)
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'foundations': ['resources/*'],
    },
    scripts=['foundations']
)
