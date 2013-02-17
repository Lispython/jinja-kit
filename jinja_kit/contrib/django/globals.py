#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
jinja_kit.contrib.django.globals
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Template functions

:copyright: (c) 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""

from django.conf import settings
from django.utils.safestring import mark_safe

from jinja2 import contextfunction


def _reverse(viewname, args=[], kwargs={}, fail=True):
    from django.core.urlresolvers import reverse, NoReverseMatch

    url = ''
    try:
        url = reverse(viewname, args=args, kwargs=kwargs)
    except NoReverseMatch:
        projectname = settings.SETTINGS_MODULE.split('.')[0]
        try:
            url = reverse(projectname + '.' + viewname, args=args, kwargs=kwargs)
        except NoReverseMatch:
            if fail:
                raise
            else:
                return ''
    return url


@contextfunction
def csrf_token(context):
    csrf_token = context.get('csrf_token', None)
    if csrf_token:
        if csrf_token == 'NOTPROVIDED':
            return mark_safe(u"")
        else:
            return mark_safe(u"<div style='display:none'><input type='hidden' name='csrfmiddlewaretoken' value='%s' /></div>" % (csrf_token))
    else:
        # It's very probable that the token is missing because of
        # misconfiguration, so we raise a warning
        from django.conf import settings
        if settings.DEBUG:
            import warnings
            warnings.warn("A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.")
            return u''


globals = {
    "url": _reverse,
    "dir": dir,
    'csrf_token': csrf_token
}
