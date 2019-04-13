# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""

setup(
    name="locklog",
    version="0.1.0",
    description="Record on-screen time to daily log files",
    license="gpl v3",
    author="Michaël Dierick",
    packages=find_packages(),
    install_requires=['pydbus'],
    dependency_links=['https://github.com/LEW21/pydbus/tarball/master#egg=repo-0.6.0'],
    long_description=long_description,
    entry_points={
        'console_scripts': ['locklog=locklog.__main__:main'],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
