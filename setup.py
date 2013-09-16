#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
jinja_kit
~~~~~~~~~

Collection of utilities and extenstion for jinja2

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""


import sys
import os
try:
    import subprocess
    has_subprocess = True
except:
    has_subprocess = False

from setuptools import setup, find_packages

try:
    readme_content = open(os.path.join(os.path.abspath(
        os.path.dirname(__file__)), "README.rst")).read()
except Exception, e:
    print(e)
    readme_content = __doc__

VERSION = "0.0.12"

def run_tests():
    from tests.run_tests import suite
    return suite

py_ver = sys.version_info

#: Python 2.x?
is_py2 = (py_ver[0] == 2)

#: Python 3.x?
is_py3 = (py_ver[0] == 3)

tests_require = [
    'nose',
    'unittest2',
    'html5lib',
    'django==1.4.4']

install_requires = [
    "Jinja2==2.6"]


setup(
    name="jinja_kit",
    version=VERSION,
    description="Collection of utilities and extenstion for jinja2",
    long_description=readme_content,
    author="Alex Lispython",
    author_email="alex@obout.ru",
    maintainer="Alexandr Lispython",
    maintainer_email="alex@obout.ru",
    url="https://github.com/lispython/jinja-kit",
    packages=find_packages(exclude=("tests",)),
    install_requires=install_requires,
    tests_require=tests_require,
    license="BSD",
    platforms = ['Linux', 'Mac'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML"
        ],
    test_suite = 'tests.runtests.suite'
    )
