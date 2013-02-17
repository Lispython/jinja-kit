#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
jinja_kit.contrib.django.default
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Shortcuts for error handlers

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""

from django.http import HttpResponseNotFound, HttpResponseServerError

from jinja_kit.contrib.django import jinja_kit_django as kit


def page_not_found(request):
    return kit.render_to_response('404.html',
                                  {'request_path': request.path},
                                  request, response_class=HttpResponseNotFound)


def server_error(request):
    return kit.render_to_response('500.html', {},
                                  request, response_class=HttpResponseServerError)
