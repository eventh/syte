# -*- coding: utf-8 -*-
import json
from operator import itemgetter

import requests
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache
from django.views.decorators.cache import never_cache


def github(request, username, refresh=False):
    content = cache.get('github')
    if content is not None and not refresh:
        return HttpResponse(content, 'application/json; charset=utf-8')

    user_r = requests.get('{0}users/{1}?access_token={2}'.format(
        settings.GITHUB_API_URL,
        username,
        settings.GITHUB_ACCESS_TOKEN))

    repos_r = requests.get('{0}users/{1}/repos?access_token={2}'.format(
        settings.GITHUB_API_URL,
        username,
        settings.GITHUB_ACCESS_TOKEN))

    context = {'user': user_r.json}
    context['repos'] = repos_r.json

    # Get parent repo if it is a fork
    for repo in context['repos']:
        if repo['fork']:
            fork_r = requests.get('{0}repos/{1}/{2}?access_token={3}'.format(
                settings.GITHUB_API_URL,
                username,
                repo['name'],
                settings.GITHUB_ACCESS_TOKEN))
            repo['parent'] = fork_r.json['parent']

    context['repos'].sort(key=itemgetter('updated_at'), reverse=True)

    content = json.dumps(context)
    if not (user_r.error or repos_r.error):
        cache.set('github', content, 7200)  # 2 hours

    return HttpResponse(content, repos_r.headers['content-type'],
                        repos_r.status_code)


@never_cache
def github_auth(request):
    context = dict()
    code = request.GET.get('code', None)
    error = request.GET.get('error_description', None)

    if not code and not error:
        return redirect('{0}?client_id={1}&redirect_uri={2}'
                        'github/auth/&response_type=code'.format(
            settings.GITHUB_OAUTH_AUTHORIZE_URL,
            settings.GITHUB_CLIENT_ID,
            settings.SITE_ROOT_URI))

    if code:
        r = requests.post(settings.GITHUB_OAUTH_ACCESS_TOKEN_URL, data={
            'client_id': settings.GITHUB_CLIENT_ID,
            'client_secret': settings.GITHUB_CLIENT_SECRET,
            'redirect_uri': '{0}github/auth/'.format(settings.SITE_ROOT_URI),
            'code': code,
        }, headers={'Accept': 'application/json'})

        try:
            data = r.json
            error = data.get('error', None)
        except:
            error = r.text

        if not error:
            context['token'] = data['access_token']

    if error:
        context['error'] = error

    return render(request, 'github_auth.html', context)
