#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    README = f.read()

with open('LICENSE') as f:
    LICENSE = f.read()

if __name__ == '__main__':
    # build distribution package
    setup(
        name="pyzbx_tool",
        version="2021.05.30.01",
        py_modules=['ZabbixAPI', 'ZabbixSender'],
        description='pyzbx_tool',
        long_description=README,
        install_requires=['requests'],
        author='2bo',
        author_email='rheinbund@gmail.com',
        url='https://github.com/2bobo/pyzbx',
        license=LICENSE,
        packages=find_packages(exclude=('tests', 'docs')),
    )
