# -*- coding: utf-8 -*-
import json

import requests
import django
from django.http import HttpResponse


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
     'description': 'Copyright (c) 2012 Kenneth Reitz',
     'license': 'ISC'},

    {'name': 'RequireJS',
     'url': '//github.com/jrburke/requirejs',
     'version': '1.0.8',
     'description': 'Copyright (c) 2010-2012, The Dojo Foundation '
     'All Rights Reserved',
     'license': 'MIT'},

    {'name': 'handlebars',
     'url': '//handlebarsjs.com/',
     'version': '1.0.beta.6',
     'description': 'Copyright (C) 2011 by Yehuda Katz',
     'license': 'MIT'},

    {'name': 'Moment.js',
     'url': '//momentjs.com/',
     'version': '1.6.2',
     'description': 'Copyright (c) 2011-2012 Tim Wood',
     'license': 'MIT'},

    {'name': 'spin.js',
     'url': '//fgnass.github.com/spin.js/',
     'version': '1.2.5',
     'description': 'Copyright (c) 2011 Felix Gnass [fgnass at neteye dot de]',
     'license': 'MIT'},

    {'name': 'bootstrap-modal.js',
     'url': '//twitter.github.com/bootstrap/javascript.html#modals',
     'version': '2.0.3',
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
]


def about(request):
    packages = BASE_PACKAGES[:]

    context = {'count': len(packages), 'packages': packages}
    return HttpResponse(json.dumps(context),
                        'application/json; charset=utf-8')
