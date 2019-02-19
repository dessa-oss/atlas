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

def list_files_recursively(root, start_directory):
    import os
    import os.path
    previous_directory = os.getcwd()
    os.chdir(root)
    for directory, _, files in os.walk(start_directory):
        for file in files:
            yield os.path.join(directory, file)
    os.chdir(previous_directory)

package_data = list(list_files_recursively('src/foundations_contrib', 'resources'))

setup(
    name='foundations_contrib',
    version=environ.get('build_version', '0.0.0'),
    description='A tool for machine learning development - files for contribution',
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
        'futures; python_version == "2.7"',
        'tabulate==0.8.3'
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'foundations_contrib': package_data,
    }
)
