#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
jinja_kit.tests
~~~~~~~~~~~~~~~

Test for jinja_kit

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""
import os
import unittest
import test_settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'test_settings'

from django.conf import settings

if not settings.configured:
    settings.configure(**dict([(k, getattr(test_settings, k, None))
                               for k in dir(test_settings)
                               if (k.isupper() and not k.startswith('_'))]))


from .core import CoreTestCase
from .django_test import DjangoTestCase


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CoreTestCase))
    #suite.addTest(unittest.makeSuite(DjangoTestCase))
    return suite


def main():
    unittest.main(defaultTest="suite")

if __name__ == '__main__':
    main()
