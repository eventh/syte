# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.conf import settings


def documents(request):
    # List of documents to display.
    # Each entry consist of {file, title, sub, desc, date}
    docs = [
        {'file': 'pyhaskell.pdf',
         'title': 'Implementing Haskell in RPython',
         'desc': 'PyHaskell is an Haskell VM written in RPython, to '
         'investigate how Haskell can benefit from JIT compilation '
         'techniques. Report from specialization project at NTNU.',
         'date': 'June 8, 2012'},

        {'file': 'pypy_evaluation.pdf',
         'title': 'Evaluation of the PyPy Project',
         'sub': 'Past, Present and the Future',
         'desc': '',
         'date': 'February 12, 2012'},
    ]

    # Add static_url to filenames to create url
    for doc in docs:
        doc['url'] = settings.STATIC_URL + 'files/' + doc['file']

    return HttpResponse(json.dumps({'docs': docs}),
                        'application/json; charset=utf-8')
