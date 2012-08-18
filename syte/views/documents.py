# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.conf import settings


def documents(request):
    # List of documents to display.
    # Each entry consist of {file, title, sub, desc, date}
    docs = [
        {'file': 'filename.pdf',
         'title': 'TODO: add document title',
         'description': 'TODO: add a description of the document',
         'date': 'June 2012'},
    ]

    # Add static_url to filenames to create url
    for doc in docs:
        doc['url'] = '%sfiles/%s' % (settings.MEDIA_URL, doc['file'])

    return HttpResponse(json.dumps({'docs': docs, 'count': len(docs)}),
                        'application/json; charset=utf-8')
