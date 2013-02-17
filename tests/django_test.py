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

from .base import BaseTestCase
from jinja_kit.contrib.django import DjangoKit


class DjangoTestCase(BaseTestCase):

    def test_kit(self):

        filters = ['jinja_kit.contrib.django.fitlers']
        global_func = ['jinja_kit.contrib.django.globals']

        extensions = ['jinja_kit.contrib.ext']

        kit = DjangoKit({})


        self.assertEquals(kit.render_to_string(
            "base.html",
            {"myvar": "hello world"}), "<h1>hello world</h1>")
