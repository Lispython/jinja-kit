#!/usr/bin/env python
# -*- coding:  utf-8 -*-
"""
jinja_kit.tests.test_settings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Test for jinja_kit

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""

import os.path

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), 'templates')

DATABASES =  {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME": 'jinja_kit',
        "USER": '',
        "PASSWORD": '',
        "HOST": '',
        "PORT": '',
        }
    }


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.sites',

    'jinja_kit.contrib.django'
    ]

ROOT_URLCONF='urls',
DEBUG=True,
DATE_INPUT_FORMATS=('%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y', '%b %d %Y',
                    '%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
                    '%B %d, %Y', '%d %B %Y', '%d %B, %Y'),
SITE_ID=1

TEMPLATE_DIRS = [TEMPLATES_DIR]
