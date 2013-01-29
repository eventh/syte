# -*- coding: utf-8 -*-
import json

import requests
import django
import gunicorn
import rauth
from django.http import HttpResponse
from django.conf import settings


# List of packages used by Syte
# {name, description, version, url, license}
PACKAGES = [
    {'name': 'Django',
     'url': '//www.djangoproject.com/',
     'version': django.get_version(),
     'description': 'Copyright (c) Django Software '
     'Foundation and individual contributors.',
     'license': 'BSD'},

    {'name': 'Requests',
     'url': '//python-requests.org/',
     'version': requests.__version__,
     'description': 'Copyright (c) 2012 Kenneth Reitz',
     'license': 'ISC'},

    {'name': 'RequireJS',
     'url': '//github.com/jrburke/requirejs',
     'version': '2.1.2',
     'description': 'Copyright (c) 2010-2012, The Dojo Foundation '
     'All Rights Reserved',
     'license': 'MIT'},

    {'name': 'handlebars',
     'url': '//handlebarsjs.com/',
     'version': '1.0.rc.1',
     'description': 'Copyright (C) 2011 by Yehuda Katz',
     'license': 'MIT'},

    {'name': 'Moment.js',
     'url': '//momentjs.com/',
     'version': '1.7.2',
     'description': 'Copyright (c) 2011-2012 Tim Wood',
     'license': 'MIT'},

    {'name': 'spin.js',
     'url': '//fgnass.github.com/spin.js/',
     'version': '1.2.7',
     'description': 'Copyright (c) 2011 Felix Gnass [fgnass at neteye dot de]',
     'license': 'MIT'},

    {'name': 'bootstrap-transition.js',
     'url': '//twitter.github.com/bootstrap/javascript.html#transitions',
     'version': '2.2.2',
     'description': 'Copyright 2012 Twitter, Inc',
     'license': 'Apache Version 2.0'},

    {'name': 'bootstrap-modal.js',
     'url': '//twitter.github.com/bootstrap/javascript.html#modals',
     'version': '2.2.1',
     'description': 'Copyright 2012 Twitter, Inc',
     'license': 'Apache Version 2.0'},

    {'name': 'jQuery URL Parser',
     'url': '//github.com/allmarkedup/jQuery-URL-Parser',
     'description': 'Copyright (c) 2012 Mark Perkins, http://allmarkedup.com/',
     'license': 'MIT'},

    {'name': 'google-code-prettify',
     'url': '//code.google.com/p/google-code-prettify/',
     'description': 'Copyright (C) 2006 Google Inc',
     'license': 'Apache Version 2.0'},

    {'name': 'pybars',
     'url': '//launchpad.net/pybars',
     'version': '0.0.4',
     'description': 'Copyright (c) 2012, Canonical Ltd.',
     'license': 'LGPLv3'},

    {'name': 'gunicorn',
     'url': '//gunicorn.org/',
     'version': gunicorn.__version__,
     'description': '2009,2010 (c) Benoît Chesneau <benoitc@e-engura.org> '
     '2009,2010 (c) Paul J. Davis <paul.joseph.davis@gmail.com>.',
     'license': 'MIT'},
]


if settings.TWITTER_INTEGRATION_ENABLED:
    PACKAGES.append({
        'name': 'rauth', 'url': '//rauth.readthedocs.org/',
        'version': rauth.__version__, 'license': 'MIT',
        'description': 'Rauth is Copyright (c) 2012 litl, LLC',
    })


def about(request):
    context = {'count': len(PACKAGES), 'packages': PACKAGES}
    return HttpResponse(json.dumps(context),
                        'application/json; charset=utf-8')
