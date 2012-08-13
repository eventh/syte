# -*- coding: utf-8 -*-
from syte.context_processor import site_pages
from django.shortcuts import render
from django.template import Context, loader
from django.http import HttpResponseServerError
from django.views.decorators.cache import never_cache


@never_cache
def server_error(request, template_name='500.html'):
    t = loader.get_template(template_name)
    d = site_pages(request)
    return HttpResponseServerError(t.render(Context(d)))


@never_cache
def page_not_found_error(request, template_name='404.html'):
    t = loader.get_template(template_name)
    d = site_pages(request)
    return HttpResponseServerError(t.render(Context(d)))


def home(request):
    return render(request, 'index.html', {})
