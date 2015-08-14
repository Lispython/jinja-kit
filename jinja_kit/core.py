# -*- coding: utf-8 -*-
"""
jinja_kit.core
~~~~~~~~~~~~~~

Core jinja_kit wrapper class

:copyright: (c) 2009 by the Jinja Team.
:copyright: (c) 2012 - 2013 by Alexandr Lispython (alex@obout.ru).
:license: BSD, see LICENSE for more details.
:github: http://github.com/Lispython/jinja-kit
"""

from itertools import chain

try:
    from cProfile import Profile
except ImportError:
    from profile import Profile

from jinja2 import Environment, FileSystemLoader
from jinja2.utils import import_string
from jinja2.environment import Template

from jinja_kit.exceptions import TemplateNotFound


class Kit(object):
    """Magic wrapper for jinja environment
    """
    def __init__(self, search_path, loader=FileSystemLoader,
                 auto_reload=False, cache_size=50, extensions=(),
                 filters={}, globals={}):
        """Construct wrapper
        """
        self.search_path = search_path
        self.env = Environment(loader=loader(self.search_path),
                               auto_reload=auto_reload,
                               cache_size=cache_size,
                               extensions=extensions)
        self.filters = filters
        self.globals = globals

    def filter(self, name=None):
        def wrapper(func):
            return self.add_filter(func, name)
        return wrapper

    def tglobal(self, name=None):
        def wrapper(func):
            return self.add_global(func, name)
        return wrapper

    def add_filter(self, func, name=None):
        """Add filter to environment
        :param func:
        :param name:
        """
        self.env.filters.update({name or func.func_name: func})
        return func

    def add_global(self, func, name=None):
        """Add global function to context

        :param func:
        :param name:
        """
        self.env.globals.update({name or func.func_name: func})
        return func

    def load_filters(self, paths=None):
        """Load filter to environment
        """
        result = {}
        paths = paths or self.filters
        for m in paths:
            f = __import__(m, fromlist=['filters'])
            result.update(f.filters)
        return result

    def load_globals(self, paths=None, key='globals'):
        """Load global function to environment
        """
        result = {}
        paths = paths or self.globals
        for m in paths:
            f = __import__(m, fromlist=[key])
            result.update(f.globals)
            for name, func in f.globals.iteritems():
                self.add_global(func, name)
        return result

    def load_extensions(self, extensions):
        """Load extensions
        """
        for extension in extensions:
            if isinstance(extension, basestring):
                extension = import_string(extension)
            self.add_extension(extension)

    def add_extension(self, ext):
        """Load extension to environment

        :param ext: extension object
        """
        self.env.add_extension(ext)

    def get_template(self, template_name, global_functions={}):
        """Get template
        """
        return self.env.get_template(template_name, globals=global_functions)

    def select_template(self, templates):
        """Search templates
        """
        if isinstance(templates, (list, tuple)):
            for template in templates:
                try:
                    return self.get_template(template,
                                             global_functions=globals())
                except TemplateNotFound:
                    continue
        elif isinstance(templates, (str, unicode, Template)):
            return self.get_template(templates, globals())


        raise TemplateNotFound

    def render_to_string(self, template_name, context=None,
                         processors=None, processor_arg=None):
        """Render template into string

        :param template_name:
        :param context:
        :param processors:
        :param proccessor_arg:
        """
        created_context = self.get_context(context=context, processors=processors,
                                           processor_arg=processor_arg)
        return self.select_template(template_name).render(created_context)

    def get_standard_processors(self):
        return ()

    def get_context(self, context=None, processors=None, processor_arg=None):
        context = dict(context or {})
        context['processor_arg'] = processor_arg
        standard_processors = self.get_standard_processors()

        for processor in chain(standard_processors, processors or ()):
            try:
                context.update(processor(processor_arg))
            except Exception, e:
                print(e)

        return context


    def from_source(self, source, context=None, processors=None, processor_arg=None):
        created_context = self.get_context(context=context, processors=processors,
                                           processor_arg=processor_arg)
        return self.env.from_string(source).render(created_context)
