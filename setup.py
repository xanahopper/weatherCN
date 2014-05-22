#!/usr/bin/env python
# encoding: utf-8

from distutils.core import setup

setup(
    name='WeatherCN',
    version='0.1.1',
    description='获取国内城市天气',
    author='Xana Hopper',
    author_email='xanahopper@163.com',
    packages=['weatherCN',],
    url='https://github.com/xanahopper/weatherCN/',
    license='LGPL',
    install_requires=[],
    long_description=open("README.md").read()
)
