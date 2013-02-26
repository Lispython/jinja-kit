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

from jinja_kit import Kit

from base import BaseTestCase
from test_settings import TEMPLATES_DIR

class CoreTestCase(BaseTestCase):

    def test_kit(self):
        kit = Kit(TEMPLATES_DIR)

        self.assertEquals(kit.render_to_string("base.html", {
            "myvar": "hello world"}), "<h1>hello world</h1>")

    def test_filters(self):
        kit = Kit(TEMPLATES_DIR)

        @kit.filter("test_filter_name")
        def test_filter(value):
            return "filter value"

        self.assertEquals(kit.render_to_string("filter.html", {
            "myvar": "hello world"}), test_filter(None))

    def test_globals(self):
        kit = Kit(TEMPLATES_DIR)

        @kit.tglobal()
        def test_global(value):
            return value

        self.assertEquals(kit.render_to_string("global.html", {
            "myvar": "hello world"}), test_global("hello world"))


