"""
Copyright 2015 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='atsd_client',
    packages=['atsd_client', 'atsd_client.models'],
    version='1.0',
    description='Python client for ATSD REST API',
    author='Axibase Corporation',
    author_email='axibase-api@axibase.com',
    license='Apache 2.0',
    install_requires=['requests'],
    package_data={'atsd_client': ['connection.properties']}
)