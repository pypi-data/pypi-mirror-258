from io import open
from setuptools import setup

from asyncj import __version__

"""
:authors: VengDevs
:licence: Apache License, Version 2.0
:copyright: (c) 2024 VengDevs
"""

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name="asyncj",
    version=__version__,
    author='VengDevs',
    description='Python module for fast asynchronous work with JSON files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/VengDevs/AsyncJ',
    license='Apache License, Version 2.0',
    packages=['asyncj'],
    install_requires=['aiofiles', 'ujson'],
    python_requires='>=3.8',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ]
)