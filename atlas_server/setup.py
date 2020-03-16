# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="foundations-atlas",
    use_scm_version = { 
        "root": "..",
        "relative_to": __file__,
        'local_scheme': 'dirty-tag' 
    },
    description='A tool for machine learning development',
    long_description=long_description,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    scripts=['atlas-server', 'atlas-server.cmd'],
    python_requires='>=3.6'
)
