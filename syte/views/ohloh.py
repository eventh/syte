# -*- coding: utf-8 -*-
import json
from operator import itemgetter
from xml.etree import ElementTree

import requests
from django.conf import settings
from django.http import HttpResponse
from django.core.cache import cache


def ohloh(request, username, refresh=False):
    content = cache.get('ohloh')
    if content is not None and not refresh:
        return HttpResponse(content, 'application/json; charset=utf-8')

    r = requests.get('{0}accounts/{1}.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, username, settings.OHLOH_API_KEY))

    # Basic account information
    root = ElementTree.fromstring(r.text)
    account = root.find('result/account')
    context = {node.tag: node.text for node in account}
    context['login'] = username
    context['kudo_score'] = account.find('kudo_score/kudo_rank').text

    # Project managed by 'username'
    man_r = requests.get('{0}accounts/{1}/projects.xml?api_key={2}'.format(
        settings.OHLOH_API_URL, username, settings.OHLOH_API_KEY))
    root = ElementTree.fromstring(man_r.text)
    projects = [{i.tag: i.text for i in node} for node in root.find('result')]
    context['managed_projects'] = len(projects)

    # Other projects 'username' has contributed to
    for name in settings.OHLOH_PROJECT_URL_NAMES:
        pro_r = requests.get('{0}p/{1}.xml?api_key={2}'.format(
            settings.OHLOH_API_URL, name, settings.OHLOH_API_KEY))
        root = ElementTree.fromstring(pro_r.text)
        projects.append({i.tag: i.text for i in root.find('result/project')})

    context['projects'] = projects
    context['total_projects'] = len(projects)
    context['total_commits'] = 0

    # Contributions to each project and total commits
    user_id = context['id']
    for project in projects:
        project['commits'] = 0
        project['man_months'] = 0
        project['last_commit_time'] = ''

        if not project.get('homepage_url', False):
            project['homepage_url'] = 'http://www.ohloh.net/p/' + \
                    project['url_name']

        # Find contributions tied to our account id
        pro_r = requests.get('{0}p/{1}/contributors.xml?api_key={2}'.format(
            settings.OHLOH_API_URL, project['id'], settings.OHLOH_API_KEY))
        root = ElementTree.fromstring(pro_r.text)
        for node in root.find('result'):
            values = {n.tag: n.text for n in node}
            if values.get('account_id', None) == user_id:

                # Store commits, primary language and man months
                if not project.get('language'):
                    project['language'] = values['primary_language_nice_name']
                    project['last_commit_time'] = values['last_commit_time']
                project['man_months'] += int(values['man_months'])
                project['commits'] += int(values['commits'])

        context['total_commits'] += project['commits']

    # Sort projects by 'last_commit_time'
    context['projects'].sort(key=itemgetter('last_commit_time'), reverse=True)

    content = json.dumps(context)
    if not (r.error or man_r.error):
        cache.set('ohloh', content, 7200)  # 2 hours

    return HttpResponse(content, 'application/json; charset=utf-8',
                        r.status_code)
