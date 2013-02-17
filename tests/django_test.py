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

from django.test.client import RequestFactory
from django.utils import unittest
from django.conf import settings
from django.http import HttpResponseNotFound, HttpResponseServerError


from jinja_kit.contrib.django import DjangoKit as Kit
from jinja_kit.contrib.django.defaults import (
    page_not_found, server_error)


class DjangoTestCase(unittest.TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_kit(self):
        kit = Kit(settings)
        request = self.factory.get('/customer/details')
        self.assertEquals(kit.render_to_string("base.html", {
            "myvar": "hello world"}, request), "<h1>hello world</h1>")

    def test_filters(self):
        kit = Kit(settings)
        request = self.factory.get('/customer/details')

        @kit.filter("test_filter_name")
        def test_filter(value):
            return "filter value"

        self.assertEquals(kit.render_to_string("filter.html", {
            "myvar": "hello world"}, request), test_filter(None))

    def test_globals(self):
        request = self.factory.get('/customer/details')

        kit = Kit(settings)

        @kit.tglobal()
        def test_global(value):
            return value

        self.assertEquals(kit.render_to_string("global.html", {
            "myvar": "hello world"}, request), test_global("hello world"))

    def test_errors_handlers(self):
        request = self.factory.get("/")

        response = page_not_found(request)
        self.assertTrue(isinstance(response, HttpResponseNotFound))
        self.assertEquals(response.content, "404")

        response = server_error(request)
        self.assertTrue(isinstance(response, HttpResponseServerError))
        self.assertEquals(response.content, "500")

