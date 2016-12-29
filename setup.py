from __future__ import print_function
from setuptools import setup
from setuptools.command.test import test as TestCommand
from pip.req import parse_requirements
import io
import os
import pymarsys
import sys

here = os.path.abspath(os.path.dirname(__file__))

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


setup(
    name='pymarsys',
    version=pymarsys.__version__,
    url='http://github.com/transcovo/pymarsys/',
    license='',
    author='Transcovo',
    tests_require=['pytest'],
    install_requires=reqs,
    cmdclass={'test': PyTest},
    author_email='tech-data@chauffeur-prive.com',
    description='A Python client for the Emarsys API',
    long_description=long_description,
    packages=['pymarsys'],
    packge_dir={'pymarsys': 'pymarsys'},
    include_package_data=True,
    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    extras_require={
        'testing': ['pytest'],
    }
)
