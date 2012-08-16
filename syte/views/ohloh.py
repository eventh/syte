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
    error = root.find('error')
    if error is not None:
        print "Ohloh error:", error.text
        return server_error(requests)

    # Basic account information
    account = root.find('result/account')
    context = {node.tag: node.text for node in account}
    context['position'] = account.find('kudo_score/position').text
    context['kudo_score'] = account.find('kudo_score/kudo_rank').text
    context['monthly_commits'] = 0
    context['total_commits'] = 0
    ratio = 0.0
    ratio_count = 0

    # Accounts language experiences
    context['languages'] = []
    for node in account.find('languages'):
        values = {i.tag: i.text for i in node}

        years = int(values['experience_months']) // 12
        months = int(values['experience_months']) % 12
        if years:
            values['experience'] = '%iy %im' % (years, months)
        else:
            values['experience'] = '%im' % months

        values['name'] = values['name'].capitalize()
        context['languages'].append(values)

        context['monthly_commits'] += int(values['median_monthly_commits'])
        #context['total_commits'] += int(values['total_commits'])

        # Average comment ratio stat
        if values['comment_ratio'] != '-':
            ratio += float(values['comment_ratio'].replace('%', ''))
            ratio_count += 1

    context['total_languages'] = len(context['languages'])
    context['comment_ratio'] = '%.1f%%' % (ratio / ratio_count)

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

        if not project.get('homepage_url', False):
            project['homepage_url'] = project['html_url']

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

    # Sort projects by 'last_commit_time'
    context['projects'] = list(projects.values())
    context['total_projects'] = len(context['projects'])
    context['projects'].sort(key=itemgetter('last_commit_time'), reverse=True)

    # Cache content
    content = json.dumps(context)
    if not (r.error or man_r.error):
        cache.set('ohloh', content, 7200)  # 2 hours

    return HttpResponse(content, 'application/json; charset=utf-8',
                        r.status_code)
