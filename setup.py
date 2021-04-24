from setuptools import setup

setup(
    name='timbit',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'timbit=timbit:timbit'
        ]
    }
)