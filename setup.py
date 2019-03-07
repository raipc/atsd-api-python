"""
Copyright 2018 Axibase Corporation or its affiliates. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

https://www.axibase.com/atsd/axibase-apache-2.0.pdf

or in the "license" file accompanying this file. This file is distributed
on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied. See the License for the specific language governing
permissions and limitations under the License.
"""
import os
import re
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))
with open('atsd_client/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

sys.stdout.write('atsd_client version: {}'.format(version))

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 5)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
========================== 
This version of atsd_client requires Python >= {}.{}, but you're trying to install it on Python {}.{}.
If you can't upgrade your pip (or Python), install an older version of atsd_client:

    python -m pip install "atsd_client<3.0.0"
    
""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ['python-dateutil', 'requests>=2.12.1', 'tzlocal']
long_description = '''The `ATSD API Client for Python <https://github.com/axibase/atsd-api-python>`__ simplifies the 
process of interacting with `Axibase Time Series Database <https://axibase.com/docs/atsd/>`__ through REST API and SQL 
endpoints.'''

setup(
    name='atsd_client',
    packages=['atsd_client', 'atsd_client.models'],
    version=version,
    python_requires='>={}.{}'.format(*REQUIRED_PYTHON),
    description='Axibase Time Series Database API Client for Python',
    url='https://github.com/axibase/atsd-api-python',
    author='Axibase Corporation',
    author_email='axibase-api@axibase.com',
    license='Apache 2.0',
    install_requires=install_requires,
    extras_require={
       'analysis': ['pandas']
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={'atsd_client': ['connection.properties']},
    keywords='axibase, atsd, axibase time-series database, python',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: OS Independent',
        'Topic :: Database',
        'Topic :: Database :: Database Engines/Servers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Monitoring'
    )
)
