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

package_source = "src"
if environ.get("BUILD_FOUNDATIONS_OBFUSCATED", False):
    package_source = "obfuscated_dist"

setup(
    name='foundations-internal',
    version=build_version,
    description='A tool for machine learning development - core modules',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'dill==0.2.8.2',
        'redis==3.3.11',
        'PyYAML==5.1.2',
        'promise==2.2.1'
    ],
    packages=find_packages(package_source),
    package_dir={'': package_source},
    package_data={
        'foundations_internal': ['resources/*', "**/*pytransform*", "**/license.lic", "*pytransform*", "license.lic", "pytransform.py", "*", "**/*", 'licenses/*/*', 'licenses/*'],
    },
    include_package_data=True
)
