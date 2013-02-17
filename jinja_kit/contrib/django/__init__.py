#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import


from jinja_kit import Kit

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.utils import import_string
from django.conf import settings
from django.http import HttpResponse
from django.template.context import get_standard_processors

class DjangoKit(Kit):
    """Magic wrapper for jinja environment for django
    """

    def __init__(self, settings, loader=FileSystemLoader):
        self.settings = settings

        self.search_path = getattr(settings, 'TEMPLATE_DIRS', list())
        self.loader = import_string(getattr(settings, 'TEMPLATE_LOADER', 'jinja2.FileSystemLoader'))

        self.env = Environment(loader=self.loader(self.search_path),
                               auto_reload=getattr(settings, 'JINJA_AUTO_RELOAD', False),
                               cache_size=getattr(settings, 'JINJA_CHACHE_SIZE', 50),
                               extensions=getattr(settings, 'JINJA_EXTENSIONS', ()))

    def get_standard_processors(self):
        """Get django standart processors
        """
        return get_standard_processors()

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


jinja_kit_django = DjangoKit(settings)