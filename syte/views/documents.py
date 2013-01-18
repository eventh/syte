# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse
from django.conf import settings


# List of documents to display
# {file, title, subtitle, description, date, url}
# Use url to give direct link to file, or file to host yourself.
ALL_DOCUMENTS = [
    {'title': 'Trace-based just-in-time compiler for Haskell with RPython',
     'description': "My Master's thesis.",
     'url': 'http://bitbucket.org/eventh/courses/downloads/Trace-based%20just-in-time%20compiler%20for%20Haskell%20with%20RPython.pdf',
     'date': 'January 2013'},

    {'title': 'Implementing Haskell in RPython',
     'description': 'PyHaskell is an Haskell VM written in RPython, '
     'to investigate how Haskell can benefit from JIT compilation '
     'techniques. Report from specialization project at NTNU.',
     'url': 'http://bitbucket.org/eventh/courses/downloads/Implementing%20Haskell%20in%20RPython.pdf',
     'date': 'June 2012'},

    {'title': 'Evaluation of the PyPy Project',
     'subtitle': 'Past, Present and the Future',
     'description': 'An evaluation of the PyPy project --- the Python intepreter and the RPython translation toolchain.',
     'url': 'http://bitbucket.org/eventh/courses/downloads/Evaluation%20of%20PyPy%20Project%20-%20Past,%20Present%20and%20Future.pdf',
     'date': 'February 2012'},

    {'title': 'CSjark',
     'subtitle': 'Automated Generation of Protocol Dissectors for Wireshark',
     'description': 'Report from TDT4290 Customer Driven Project at Norwegian at NTNU.',
     'url': 'http://bitbucket.org/eventh/courses/downloads/Automated%20Generation%20of%20Protocol%20Dissectors%20for%20Wireshark.pdf',
     'date': 'November 2011'},

    {'title': 'Topic 5: Evaluating OSS projects',
     'description': 'Presentation given in TDT10 New Software Technology: COTS and Open Source Software at NTNU.',
     'url': 'http://bitbucket.org/eventh/courses/downloads/Evaluating_OSS_projects_presentation.pdf',
     'date': 'September 2011'},

    {'title': 'Project Report: Web-intelligence',
     'description': 'Project report from mandatory assignment in TDT4215 Web-intelligence at NTNU.',
     'url': 'http://bitbucket.org/eventh/courses/downloads/TDT4215_report.pdf',
     'date': 'March 2012'},

    {'title': 'Project Presentation: Web-intelligence',
     'description': 'Presentation given about project in TDT4215 Web-intelligence at NTNU.',
     'url': 'http://bitbucket.org/eventh/courses/downloads/TDT4215_presentation.pdf',
     'date': 'April 2012'},
]


def documents(request):
    docs = ALL_DOCUMENTS

    # Add static_url to filenames to create url
    for doc in docs:
        if 'url' not in doc:
            doc['url'] = '%sfiles/%s' % (settings.STATIC_URL, doc['file'])

    context = {'count': len(docs), 'docs': docs,
               'url': 'http://bitbucket.org/eventh/courses/downloads'}

    return HttpResponse(json.dumps(context),
                        'application/json; charset=utf-8')
