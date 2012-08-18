# -*- coding: utf-8 -*-
import json

import requests
import django
import boto
import rauth
import storages
import gunicorn
import greenlet
import gevent
import pylibmc
import django_pylibmc
from django.http import HttpResponse
from django.conf import settings


# List of packages used by Syte
# {name, description, version, url, license}
BASE_PACKAGES = [
    {'name': 'Django',
     'url': '//www.djangoproject.com/',
     'version': django.get_version(),
     'description': 'Copyright (c) Django Software '
     'Foundation and individual contributors.',
     'license': 'BSD'},

    {'name': 'Requests',
     'url': '//python-requests.org/',
     'version': requests.__version__,
     'description': 'Copyright (c) 2012 Kenneth Reitz.',
     'license': 'ISC'},

    {'name': 'jQuery',
     'url': '//jquery.com/',
     'version': '1.8.0',
     'description': 'Copyright 2012 jQuery Foundation and other contributors.',
     'license': 'MIT'},

    {'name': 'RequireJS',
     'url': '//github.com/jrburke/requirejs',
     'version': '1.0.8',
     'description': 'Copyright (c) 2010-2012, The Dojo Foundation.',
     'license': 'MIT'},

    {'name': 'RequireJS JSON plugin',
     'url': '//github.com/millermedeiros/requirejs-plugins',
     'version': '0.2.1',
     'description': 'Author: Miller Medeiros.',
     'license': 'MIT'},

    {'name': 'handlebars',
     'url': '//handlebarsjs.com/',
     'version': '1.0.beta.6',
     'description': 'Copyright (C) 2011 by Yehuda Katz.',
     'license': 'MIT'},

    {'name': 'Moment.js',
     'url': '//momentjs.com/',
     'version': '1.6.2',
     'description': 'Copyright (c) 2011-2012 Tim Wood.',
     'license': 'MIT'},

    {'name': 'spin.js',
     'url': '//fgnass.github.com/spin.js/',
     'version': '1.2.5',
     'description': 'Copyright (c) 2011 Felix Gnass.',
     'license': 'MIT'},

    {'name': 'bootstrap-modal.js',
     'url': '//twitter.github.com/bootstrap/javascript.html#modals',
     'version': '2.0.3',
     'description': 'Copyright 2012 Twitter, Inc.',
     'license': 'Apache Version 2.0'},

    {'name': 'jQuery URL Parser',
     'url': '//github.com/allmarkedup/jQuery-URL-Parser',
     'description': 'Copyright (c) 2012 Mark Perkins, '
     'http://allmarkedup.com/.',
     'license': 'MIT'},

    {'name': 'google-code-prettify',
     'url': '//code.google.com/p/google-code-prettify/',
     'description': 'Copyright (C) 2006 Google Inc.',
     'license': 'Apache Version 2.0'},

    {'name': 'pybars',
     'url': '//launchpad.net/pybars',
     'version': '0.0.2',
     'description': 'Copyright (c) 2012, Canonical Ltd.',
     'license': 'LGPLv3'},

    {'name': 'boto',
     'url': '//github.com/boto/boto',
     'version': boto.__version__,
     'license': 'MIT'},

    {'name': 'django-storages',
     'url': '//django-storages.readthedocs.org/',
     'version': storages.__version__,
     'license': 'BSD'},

    {'name': 'gunicorn',
     'url': '//gunicorn.org/',
     'version': gunicorn.__version__,
     'description': '2009,2010 (c) Benoît Chesneau <benoitc@e-engura.org>\n'
     '2009,2010 (c) Paul J. Davis <paul.joseph.davis@gmail.com>.',
     'license': 'MIT'},

    {'name': 'greenlet',
     'url': '//pypi.python.org/pypi/greenlet',
     'version': greenlet.__version__,
     'description': 'Copyright (c) Armin Rigo, Christian Tismer and '
     'contributors.',
     'license': 'MIT'},

    {'name': 'gevent',
     'url': '//www.gevent.org/',
     'version': gevent.__version__,
     'description': 'Copyrighted by Denis Bilenko and the contributor.',
     'license': 'MIT'},

    {'name': 'pylibmc',
     'url': '//sendapatch.se/projects/pylibmc/',
     'version': pylibmc.__version__,
     'description': 'Copyright (c) 2008, Ludvig Ericson.',
     'license': 'BSD'},

    {'name': 'django-pylibmc-sasl',
     'url': '//pypi.python.org/pypi/django-pylibmc-sasl',
     'version': django_pylibmc.__version__,
     'description': 'Copyright (c) 2010, Jeff Balogh.',
     'license': 'BSD'},
]


def about(request):
    packages = BASE_PACKAGES[:]

    if settings.TWITTER_INTEGRATION_ENABLED:
        packages.append({
            'name': 'rauth', 'url': '//rauth.readthedocs.org/',
            'version': rauth.__version__, 'license': 'MIT',
            'description': 'Rauth is Copyright (c) 2012 litl, LLC',
        })

    context = {'count': len(packages), 'packages': packages}
    return HttpResponse(json.dumps(context),
                        'application/json; charset=utf-8')
