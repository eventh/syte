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
    total_commits = 0
    total_lines = 0
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
        context['languages'].append(values)

        #total_commits += int(values['total_commits'].replace(',', ''))
        total_lines += int(values['total_lines_changed'].replace(',', ''))

    context['total_languages'] = len(context['languages'])
    context['total_commits'] = total_commits
    context['total_lines_changed'] = total_lines

    # Project managed by 'username'
    man_r = requests.get('{0}accounts/{1}/projects.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, username, settings.OHLOH_API_KEY))
    root = ElementTree.fromstring(man_r.text)
    tmp = [{i.tag: i.text for i in node} for node in root.find('result')]
    projects = {}
    for project in tmp:
        project['manager'] = True
        project_id = int(project['id'])
        if project_id in (k for k, v in settings.OHLOH_CONTRIB_IDS):  # XXX
            projects[project_id] = project
    context['managed_projects'] = len(projects)

    # Other projects 'username' has contributed to
    for project_id, contrib in settings.OHLOH_CONTRIB_IDS:
        if project_id not in projects:
            pro_r = requests.get('{0}projects/{1}.xml?api_key={2}'.format(
                settings.OHLOH_API_URL, project_id, settings.OHLOH_API_KEY))
            root = ElementTree.fromstring(pro_r.text)
            tmp = {i.tag: i.text for i in root.find('result/project')}
            projects[int(tmp['id'])] = tmp

    # Contributions to each project and commits
    for project_id, contrib_id in settings.OHLOH_CONTRIB_IDS:
        project = projects[project_id]

        # Find contributions tied to our account id
        pro_r = requests.get(
            '{0}projects/{1}/contributors/{2}.xml?api_key={3}'.format(
                settings.OHLOH_API_URL, project_id,
                contrib_id, settings.OHLOH_API_KEY))
        root = ElementTree.fromstring(pro_r.text)

        result = root.find('result/contributor_fact')
        project['contributor_id'] = str(contrib_id)
        project['language'] = result.find('primary_language_nice_name').text
        project['last_commit_time'] = result.find('last_commit_time').text
        project['commits'] = int(result.find('commits').text)
        context['total_commits'] += project['commits']

    # Remove logo if src is 'no_logo.png'
    for values in projects.values():
        if ('small_logo_url' in values and
            values['small_logo_url'] == 'no_logo.png'):
            del values['small_logo_url']

    # Sort projects by 'last_commit_time'
    context['projects'] = list(projects.values())
    context['total_projects'] = len(context['projects'])
    context['projects'].sort(key=itemgetter('last_commit_time'), reverse=True)

    # Cache content
    content = json.dumps(context)
    if not (r.error or man_r.error):
        cache.set('ohloh', content, 7200)  # 2 hours

    return HttpResponse(content,
                        'application/json; charset=utf-8', r.status_code)
