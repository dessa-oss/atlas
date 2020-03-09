
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='foundations-spec',
    version=environ.get('build_version', '0.0.0'),
    description='A testing library, inspired by ruby.',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'mock==2.0.0',
        'Faker==1.0.0',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'foundations_spec': ['resources/*', 'licenses/*/*', 'licenses/*'],
    }
)
