from setuptools import setup
setup(
    name='foundations-init',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'foundations-init=index:initialize'
        ]
    }
)