from io import open
from setuptools import setup

"""
:authors: VengDevs
:licence: Apache License, Version 2.0
:copyright: (c) 2024 VengDevs
"""

version = '0.1.1'

setup(
    name="AsyncJ",
    version=version,
    author='VengDevs',
    description='Python module for fast asynchronous work with JSON files',
    url='https://github.com/Vengryyy/AsyncJ',
    license='Apache License, Version 2.0',
    packages=['AsyncJ'],
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