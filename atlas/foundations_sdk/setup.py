
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

setup(
    name='dessa-foundations',
    version=build_version,
    description='A tool for machine learning development',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'pandas==0.23.3',
        f'foundations-contrib=={build_version}',
        f'foundations-core-cli=={build_version}'
    ],
    packages=find_packages(package_source),
    package_dir={'': package_source},
    package_data={
        'foundations': ['resources/*', "**/*pytransform*", "**/license.lic", "*pytransform*", "license.lic", "pytransform.py", "*", "**/*", 'licenses/*/*', 'licenses/*']
    },
    scripts=['foundations', 'foundations.cmd'],
    include_package_data=True
)
