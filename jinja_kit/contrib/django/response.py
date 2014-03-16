#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateResponseMixin as DjangoTemplateResponseMixin

from jinja_kit.contrib.django import jinja_kit_django

class JinjaTemplateResponse(TemplateResponse):
    kit = jinja_kit_django

    rendering_attrs = ['template_name', 'context_data', '_post_render_callbacks']

    def __init__(self, request, template, context=None, mimetype=None,
                 status=None, content_type=None, current_app=None, **kwargs):

        self.processors = []

        super(JinjaTemplateResponse, self).__init__(
            request=request, template=template, context=context,
            content_type=content_type, status=status, mimetype = mimetype,
            current_app=current_app)


    def resolve_template(self, template):
        return self.kit.select_template(template)

    def resolve_context(self, context):
        return context

    @property
    def rendered_content(self):
        return self.kit.render_to_string(template_name=self.template_name,
                                         context=self.resolve_context(self.context_data),
                                         request=self._request, processors=self.processors)


class TemplateResponseMixin(DjangoTemplateResponseMixin):
    response_class = JinjaTemplateResponse

    def render_to_response(self, context, template_name = None, **response_kwargs):
        """
        Returns a response with a template rendered with the given context.
        """
        return self.response_class(
            request=self.request,
            template=template_name or self.get_template_names(),
            context=context,
            **response_kwargs)
