#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='hsync',
    version='1.0.5',
    description='a file sync tools based http',
    author='banixc',
    author_email='banixc@qq.com',
    url='https://github.com/banixc/hsync',
    py_modules=['hsync'],
    packages=find_packages(),
    install_requires=[
        'flask>=0.11.1',
        'requests>=2.11.0'
    ],
    entry_points={
        'console_scripts': [
            'hsync = hsync.__main__:local',
            'hsyncd = hsync.__main__:server',
        ],
    }
)
