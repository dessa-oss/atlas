"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vcat',
    version='0.0.1',
    description='A tool for machine learning development',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    packages=find_packages('src'),
    package_dir={'':'src'},
    include_package_data=True
)