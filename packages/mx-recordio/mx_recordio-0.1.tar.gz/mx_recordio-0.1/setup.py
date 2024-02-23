"""
Project Name: MXNet-RecordIO-Standalone
File Created: 2024/2/23 上午9:46
Author: Ying.Jiang
File Name: setup.py
"""

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='mx_recordio',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
)

entry_points = {
    'console_scripts': [
        'my_command=package_name.module:function',
    ],
},

author = 'JY',
author_email = 'yingjiang.jy@gmail.com',
url = 'https://github.com/terancejiang/MXNet-RecordIO-Standalone'
description = 'standalone version of mxnet-recordio functions, without mxnet dependency',

long_description = open('README.md').read(),
long_description_content_type = 'text/markdown',

license = 'MIT',
classifiers = [
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
],
