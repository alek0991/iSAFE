#!/usr/bin/env python
# -*- coding: utf-8 -*-

from isafe import __version__

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = """A program for identifying a favored mutation in positive selective sweep. 
    It enables researchers to accurately pinpoint the favored mutation in a large region (∼5 Mbp) 
    by using a statistic derived solely from population genetics signals."""

requirements = [
    'numpy>=1.9.0',
    'pandas>=0.18.0',
    'pysam'
]

test_requirements = []

setup(
    name='isafe',
    version=__version__,
    description="A program for identifying a favored mutation in positive selective sweep.",
    long_description=readme + '\n\n',
    author="Ali Akbari et al",
    author_email='Ali_Akbari@hms.harvard.edu',
    url='https://github.com/alek0991/iSAFE',
    packages=['isafe'],
    include_package_data=True,
    install_requires=requirements,
    entry_points = {
        'console_scripts': ['isafe=isafe.isafe:run'],
    },
    license="BSD-3-Clause",
    zip_safe=False,
    keywords='isafe',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
