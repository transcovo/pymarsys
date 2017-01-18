#!/usr/bin/env python

import os
import re
import sys

from codecs import open

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest

        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


assert sys.version_info >= (3, 4, 2), "We only support Python 3.4.2+"

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'pymarsys',
]

requires = [
    'requests>=2.12.1',
    'aiohttp>=1.2.0',
]
test_requirements = [
    'pytest==3.0.4',
    'aioresponses==0.1.2',
    'responses==0.5.1',
    'pytest-cov',
]

with open('pymarsys/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', 'utf-8') as f:
    readme = f.read()

setup(
    name='pymarsys',
    version=version,
    description='A Python client for the Emarsys API',
    long_description=readme,
    author='Transcovo',
    author_email='tech-data@chauffeur-prive.com',
    url='http://github.com/transcovo/pymarsys/',
    packages=packages,
    package_data={'': ['LICENSE'], 'pymarsys': ['*.pem']},
    package_dir={'pymarsys': 'pymarsys'},
    include_package_data=True,
    install_requires=requires,
    license='Apache 2.0',
    zip_safe=False,
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
    cmdclass={'test': PyTest},
    tests_require=test_requirements,
)
