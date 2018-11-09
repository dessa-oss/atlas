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

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='foundations_gcp',
    version=environ.get('build_version', '0.0.0'),
    description='A tool for machine learning development',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'foundations',
        'google-api-python-client==1.7.3',
        'google-auth-httplib2==0.0.3',
        'google-cloud-storage==1.10.0',
    ],
    packages=find_packages('src'),
    package_dir={'':'src'},
    package_data={
        'foundations_gcp': ['resources/*'],
    }
)