# -*- coding: utf-8 -*-

import os
import urlparse

from django.conf import settings
from django.utils.http import urlquote
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.exceptions import TemplateSyntaxError


class URLExtension(Extension):

    tags = set(['url'])
 
    def parse(self, parser):
        stream = parser.stream
        tag = stream.next()
        # get view name
        if stream.current.test('string'):
            viewname = parser.parse_primary()
        else:
            # parse valid tokens and manually build a string from them
            bits = []
            name_allowed = True
            while True:
                if stream.current.test_any('dot', 'sub'):
                    bits.append(stream.next())
                    name_allowed = True
                elif stream.current.test('name') and name_allowed:
                    bits.append(stream.next())
                    name_allowed = False
                else:
                    break
            viewname = nodes.Const("".join([b.value for b in bits]))
            if not bits:
                raise TemplateSyntaxError("'%s' requires path to view" %
                    tag.value, tag.lineno)
 
        # get arguments
        args = []
        kwargs = []
        while not stream.current.test_any('block_end', 'name:as'):
            if args or kwargs:
                stream.expect('comma')
            if stream.current.test('name') and stream.look().test('assign'):
                key = nodes.Const(stream.next().value)
                stream.skip()
                value = parser.parse_expression()
                kwargs.append(nodes.Pair(key, value, lineno=key.lineno))
            else:
                args.append(parser.parse_expression())
 
        make_call_node = lambda *kw: \
            self.call_method('_reverse',
                             args=[viewname, nodes.List(args), nodes.Dict(kwargs)],
                             kwargs=kw)
 
        # if an as-clause is specified, write the result to context...
        if stream.next_if('name:as'):
            var = nodes.Name(stream.expect('name').value, 'store')
            call_node = make_call_node(nodes.Keyword('fail', nodes.Const(False)))
            return nodes.Assign(var, call_node)
        # ...otherwise print it out.
        else:
            return nodes.Output([make_call_node()]).set_lineno(tag.lineno)
 
    @classmethod
    def _reverse(self, viewname, args, kwargs, fail=True):
        from django.core.urlresolvers import reverse, NoReverseMatch
 
        # Try to look up the URL twice: once given the view name,
        # and again relative to what we guess is the "main" app.
        url = ''
        try:
            url = reverse(viewname, args=args, kwargs=kwargs)
        except NoReverseMatch:
            projectname = settings.SETTINGS_MODULE.split('.')[0]
            try:
                url = reverse(projectname + '.' + viewname,
                              args=args, kwargs=kwargs)
            except NoReverseMatch:
                if fail:
                    raise
                else:
                    return ''
  
        return url


class SpacelessExtension(Extension):
    """
        Removes whitespace between HTML tags, including tab and
        newline characters.
    
        Works exactly like Django's own tag.
    """
 
    tags = ['spaceless']
 
    def parse(self, parser):
        lineno = parser.stream.next().lineno
        body = parser.parse_statements(['name:endspaceless'], drop_needle=True)
        return nodes.CallBlock(
            self.call_method('_strip_spaces', [], [], None, None),
            [], [], body
        ).set_lineno(lineno)
 
    def _strip_spaces(self, caller=None):
        from django.utils.html import strip_spaces_between_tags
        return strip_spaces_between_tags(caller().strip())

class WithExtension(Extension):
    """Adds a value to the context (inside this block) for caching and
easy access, just like the Django-version does.
 
For example::
 
{% with person.some_sql_method as total %}
{{ total }} object{{ total|pluralize }}
{% endwith %}
 
TODO: The new Scope node introduced in Jinja2 6334c1eade73 (the 2.2
dev version) would help here, but we don't want to rely on that yet.
See also:
http://dev.pocoo.org/projects/jinja/browser/tests/test_ext.py
http://dev.pocoo.org/projects/jinja/ticket/331
http://dev.pocoo.org/projects/jinja/ticket/329
"""
 
    tags = set(['with'])
 
    def parse(self, parser):
        lineno = parser.stream.next().lineno
 
        value = parser.parse_expression()
        parser.stream.expect('name:as')
        name = parser.stream.expect('name')
 
        body = parser.parse_statements(['name:endwith'], drop_needle=True)
        return nodes.CallBlock(
                self.call_method('_render_block', args=[value]),
                [nodes.Name(name.value, 'store')], [], body).\
                    set_lineno(lineno)
 
    def _render_block(self, value, caller=None):
        return caller(value)

class MediaExtension(Extension):
    
    tags = ['media']
    
    def parse(self, parser):
        stream = parser.stream
        tag = stream.next()
        args=[]
        fpath = parser.parse_expression()
        if parser.stream.skip_if('comma'):
            flags = parser.parse_expression()
        else:
            flags = nodes.Const(None)
        lineno = stream.current.lineno
         
        url = self.build_path(fpath.value, flags.value)
        return nodes.Output([nodes.Const(url)])

    def build_path(self, filename, flags=''):
        return compile_path(filename, (settings.MEDIA_URL, settings.MEDIA_URL), flags)

class StaticExtension(MediaExtension):
    tags = ['static']

    def build_path(self, filename, flags=''):
        return compile_path(filename, (settings.STATIC_URL, settings.STATIC_URL), flags)

def _absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    domain = Site.objects.get_current().domain 
    return 'http://%s%s' % (domain, url)
        
def compile_path(filename, prefix=(settings.MEDIA_URL, settings.MEDIA_ROOT), flags=''):
    flags = set(f.strip() for f in flags.split(',')) if flags else u''
    url = urlparse.urljoin(prefix[0], filename)
    if 'absolute' in flags and getattr(settings, 'ABSOLUTE_URLS', True):
        url= _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
        'timestamp' in flags and getattr(settings, 'PRODUCTION', True) is not True:
        fullname = os.path.abspath(os.path.join(prefix[1], filename))
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url


_media = compile_path 
# nicer import names
url = URLExtension
spaceless = SpacelessExtension
media = MediaExtension
with_ = WithExtension
static = StaticExtension

extensions = (
    url,
    spaceless,
    media,
    with_, 
    static
)

