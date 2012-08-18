# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.conf import settings


# List of documents to display
# {file, title, subtitle, description, date, url}
# Use url to give direct link to file, or file to host yourself.
ALL_DOCUMENTS = [
    {'file': 'filename.pdf',
     'title': 'TODO: document title',
     'subtitle': 'TODO: add document subtitle',
     'description': 'TODO: document description',
     'url': '',
     'date': 'June 2012'},
]


def documents(request):
    docs = ALL_DOCUMENTS

    # Add static_url to filenames to create url
    for doc in docs:
        if 'url' not in doc:
            doc['url'] = '%sfiles/%s' % (settings.MEDIA_URL, doc['file'])

    context = {'count': len(docs), 'docs': docs, 'url': ''}

    return HttpResponse(json.dumps(context),
                        'application/json; charset=utf-8')
