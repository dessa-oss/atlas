
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
    name='foundations-core-rest-api-components',
    version=build_version,
    description='Core modules for Foundations REST APIs',
    classifiers=[ 
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'foundations-contrib=={}'.format(build_version),
        'flask-restful==0.3.7',
        'Flask-Cors==3.0.8',
        'Flask==1.1.1',
        'Werkzeug==0.16.0',
    ],
    packages=find_packages(package_source),
    package_dir={'': package_source},
    package_data={
        'foundations_core_rest_api_components': ['resources/*', "**/*pytransform*", "**/license.lic", "*pytransform*", "license.lic", "pytransform.py", "*", "**/*", 'licenses/*/*', 'licenses/*'],
    },
    include_package_data=True
)