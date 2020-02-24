
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
    name='foundations-orbit-rest-api',
    version=build_version,
    description='An API for Foundations Orbit',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'foundations-contrib=={}'.format(build_version),
        'foundations_core_rest_api_components=={}'.format(build_version),
        'foundations-local-docker-scheduler-plugin=={}'.format(build_version),
        'flask-restful==0.3.7',
        'Flask-Cors==3.0.8',
        'Flask==1.1.1',
        'Werkzeug==0.16.0',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        'foundations_orbit_rest_api': ['resources/*', 'licenses/*/*', 'licenses/*'],
    }
)