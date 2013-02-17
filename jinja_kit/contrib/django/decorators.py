# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
jinja_kit.contrib.django.decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Decorators helpers

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""

from jinja_kit.contrib.django import jinja_kit_django


def render_to(template):
    def renderer(func):
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return jinja_kit_django.render_to_response(output[1], output[0], request)
            elif isinstance(output, dict):
                return jinja_kit_django.render_to_response(template, output, request)
            return output
        return wrapper
    return renderer
