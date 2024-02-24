from setuptools import setup, find_packages

setup(
    name='mymark',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mymark=src.marker.mymark.mymark:main',
        ],
    },
)
