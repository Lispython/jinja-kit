#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jinja_kit.exceptions
~~~~~~~~~~~~~~~~~~~~

Base jinja_kit exceptions

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""

from jinja2.exceptions import (
    TemplateError, FilterArgumentError, SecurityError,
    TemplateAssertionError, TemplateError,
    TemplateNotFound, TemplateRuntimeError,
    TemplateSyntaxError, UndefinedError)


class JinjaKitTemplateError(TemplateError):
    """Baseclass for all template errors."""


class JinjaKitTemplateSyntaxError(TemplateSyntaxError):
    """Raised to tell the user that there is a problem with the template."""
