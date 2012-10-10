# -*- coding: utf-8 -*-
import json
from operator import itemgetter
from xml.etree import ElementTree

import requests
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache

from syte.views.home import server_error


def ohloh(request, username, refresh=False):
    """http://www.ohloh.net integration."""
    content = cache.get('ohloh')
    if content is not None and not refresh:
        return HttpResponse(content, 'application/json; charset=utf-8')

    r = requests.get('{0}accounts/{1}.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, username, settings.OHLOH_API_KEY))

    root = ElementTree.fromstring(r.text)

    # Error handling
    error = root.find('error')
    if error is not None:
        print "Ohloh error:", error.text
        return server_error(requests)

    # Basic account information
    account = root.find('result/account')
    context = {node.tag: node.text for node in account}
    context['position'] = account.find('kudo_score/position').text
    context['kudo_score'] = account.find('kudo_score/kudo_rank').text

    # Accounts language experiences
    context['total_lines_changed'] = 0
    context['languages'] = []
    for node in account.find('languages'):
        values = {i.tag: i.text for i in node}

        # Language experience prettify output
        years = int(values['experience_months']) // 12
        months = int(values['experience_months']) % 12
        if years:
            values['experience'] = '%iy %im' % (years, months)
        else:
            values['experience'] = '%im' % months

        values['name'] = values['name'].capitalize()
        changed = int(values['total_lines_changed'].replace(',', ''))
        context['total_lines_changed'] += changed
        context['languages'].append(values)

    context['total_languages'] = len(context['languages'])

    # Project managed by 'username'
    man_r = requests.get('{0}accounts/{1}/projects.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, username, settings.OHLOH_API_KEY))
    results = ElementTree.fromstring(man_r.text).find('result')
    managed_ids = {node.find('id').text for node in results}
    context['managed_projects'] = len(managed_ids)

    # Projects contributed to
    context['projects'] = []
    context['total_commits'] = 0
    pro_r = requests.get('{0}accounts/{1}/positions.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, username, settings.OHLOH_API_KEY))
    for project in ElementTree.fromstring(pro_r.text).find('result'):
        values = {i.tag: i.text for i in project}
        values['contribution_url'] = values['html_url']
        values.update({i.tag: i.text for i in project.find('project')})

        if not values['title'] and values['id'] in managed_ids:
            values['title'] = 'Manager'

        if ('small_logo_url' in values and
            values['small_logo_url'] == 'no_logo.png'):
            del values['small_logo_url']

        context['total_commits'] += int(values['commits'])
        context['projects'].append(values)

    context['total_projects'] = len(context['projects'])

    # Contributions to each project and commits
    for project in context['projects']:
        con_r = requests.get('{0}.xml?api_key={1}'.format(
            project['contribution_url'], settings.OHLOH_API_KEY))
        root = ElementTree.fromstring(con_r.text)
        result = root.find('result/contributor_fact')
        project['language'] = result.find('primary_language_nice_name').text
        project['last_commit_time'] = result.find('last_commit_time').text

    context['projects'].sort(key=itemgetter('last_commit_time'), reverse=True)

    # Cache content
    content = json.dumps(context)
    if not (r.error or man_r.error):
        cache.set('ohloh', content, 7200)  # 2 hours

    return HttpResponse(content,
                        'application/json; charset=utf-8', r.status_code)
