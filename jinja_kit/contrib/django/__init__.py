#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
import gettext

from jinja_kit import Kit

from django.utils import translation
from django.utils.functional import SimpleLazyObject
from django.http import HttpResponse

from jinja2 import Environment, FileSystemLoader
from jinja2.utils import import_string


class DjangoKit(Kit):
    """Magic wrapper for jinja environment for django
    """

    def __init__(self, settings, loader=FileSystemLoader):
        self.settings = settings

        self.search_path = getattr(settings, 'TEMPLATE_DIRS', list())
        self.loader = import_string(getattr(settings, 'TEMPLATE_LOADER',
                                            'jinja2.FileSystemLoader'))
        if getattr(settings, "JINJA2_BYTECODE_CACHE", False):
            self.bytecode_cache = import_string(getattr(settings, 'JINJA2_BYTECODE_CACHE'))
        else:
            self.bytecode_cache = None

        self.env = Environment(loader=self.loader(self.search_path),
                               auto_reload=getattr(settings, 'JINJA2_AUTO_RELOAD', False),
                               cache_size=getattr(settings, 'JINJA2_CHACHE_SIZE', 50),
                               extensions=getattr(settings, 'JINJA2_EXTENSIONS', ()),
                               bytecode_cache=self.bytecode_cache)
        self.filters = getattr(settings, 'JINJA2_FILTERS', [])
        self.globals = getattr(settings, 'JINJA2_GLOBALS', [])

        # Not good :-(
        for name, f in self.load_filters(self.filters).iteritems():
            self.add_filter(f, name)

        for name, f in self.load_globals(self.globals).iteritems():
            self.add_global(f, name)

        if getattr(settings, 'USE_I18N'):
            try:
                self.env.install_gettext_translations(translation)
            except Exception:
                self.env.install_null_translations()

    def get_standard_processors(self):
        """Get django standart processors
        """
        try:
            from django.template.context import get_standard_processors
            return get_standard_processors()
        except Exception:
            return []

    def render_to_string(self, template_name, context=None, request=None,
                         processors=None):
        return super(DjangoKit, self).render_to_string(
            template_name, context=context, processors=processors,
            processor_arg=request)

    def render_to_response(self, template_name, context=None, request=None,
                           processors=None, mimetype=None,
                           response_class=HttpResponse):
        """Return http response
        """
        if 'request' not in context:
            context['request'] = request
        return response_class(self.render_to_string(
            template_name, context=context,
            processors=processors, request=request),
                              mimetype=mimetype)


def configure_django_kit():
    from django.conf import settings

    return DjangoKit(settings)

jinja_kit_django = SimpleLazyObject(configure_django_kit)
