# -*- coding: utf-8 -*-
import requests
import json
from operator import itemgetter

from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache


def bitbucket(request, username, refresh=False):
    content = cache.get('bitbucket')
    if content is not None and not refresh:
        return HttpResponse(content, 'application/json; charset=utf-8')

    r = requests.get('{0}users/{1}/'.format(
        settings.BITBUCKET_API_URL, username))

    data = r.json

    # Number of followers
    r_followers = requests.get('{0}users/{1}/followers/'.format(
        settings.BITBUCKET_API_URL, username))
    data['user']['followers'] = r_followers.json['count']

    # Count public repositories
    data['user']['public_repos'] = len(data['repositories'])

    for repo in data['repositories']:
        repo['language'] = repo['language'].capitalize()

        # Get number of forks
        if settings.BITBUCKET_SHOW_FORKS:
            r_forks = requests.get('{0}repositories/{1}/{2}'.format(
                settings.BITBUCKET_API_URL, username, repo['slug']))
            repo['forks_count'] = r_forks.json['forks_count']

    # Sort the repositories on utc_last_updated
    data['repositories'].sort(key=itemgetter('utc_last_updated'), reverse=True)

    content = json.dumps(data)
    if not (r.error or r_followers.error):
        cache.set('bitbucket', content, 7200)  # 2 hours

    return HttpResponse(content, r.headers['content-type'], r.status_code)
