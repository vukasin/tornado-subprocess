#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="tornado_subprocess",
    version='0.1.2',
    author='Vukasin Toroman',
    author_email='vukasin@toroman.name',
    url='https://github.com/vukasin/tornado-subprocess',
    packages=[ "tornado_subprocess"],
    description= "A module which allows you to spawn subprocesses from a tornado web application in a non-blocking fashion.",
    install_requires=[
        'tornado'
    ],
    include_package_data=True,
    license='BSD',
    keywords="tornado subprocess nonblocking",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Topic :: Internet :: WWW/HTTP"
    ],
    platforms=["unix", "osx", "linux" ],
    long_description=read('README.md'),
    zip_safe=False
)
