#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-fixturecollection',
    version='0.1.2',
    author='Jitendra Yejare',
    author_email='jyejare@redhat.com',
    maintainer='Jitendra Yejare',
    maintainer_email='jyejare@redhat.com',
    license='BSD-3',
    url='https://github.com/RedhatQE/pytest-fixturecollection',
    description='A pytest plugin to collect tests based on fixtures being'
                ' used by tests',
    long_description=read('README.rst'),
    py_modules=['pytest_fixturecollection'],
    python_requires='>=3.9',
    install_requires=['pytest>=3.5.0'],
    extras_require={'test': ['tox~=3.18', 'flake8']},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'fixturecollection = pytest_fixturecollection',
        ],
    },
)
