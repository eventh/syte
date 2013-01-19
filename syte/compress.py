#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import shlex

PATH_TO_HERE = os.path.abspath(os.path.dirname(__file__))
OUT_PATH = os.path.join(PATH_TO_HERE, 'static/js/min/')
sys.path.append(os.path.join(PATH_TO_HERE, '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'syte.settings'

from django.conf import settings


def compress_statics():
    try:
        for path in (os.path.join(PATH_TO_HERE, 'static/css'), OUT_PATH):
            if not os.path.exists(path):
                os.mkdir(path)
    except OSError:
        print 'Make sure to create "syte > static > css" and "syte > static > js > min" before compressing statics.'

    compress_styles()
    compress_js()


def compress_styles():
    less_path = os.path.join(PATH_TO_HERE, 'static/less/styles.less')
    css_path = os.path.join(PATH_TO_HERE, 'static/css/')

    subprocess.check_call(shlex.split('lessc {0} {1}styles-{2}.min.css -yui-compress'
        .format(less_path, css_path, settings.COMPRESS_REVISION_NUMBER)))
    print 'CSS Styles Generated: {0}styles-{1}.min.css'.format(
        css_path, settings.COMPRESS_REVISION_NUMBER)


def compress_js():
    js_files = (
        ('libs/handlebars', True),
        ('libs/jquery.url', True),
        ('libs/moment', True),
        ('libs/bootstrap-modal', True),
        ('libs/spin', True),
        ('libs/prettify', True),

        ('components/mobile', True),
        ('components/blog-posts', True),
        ('components/links', True),
        ('components/twitter', settings.TWITTER_INTEGRATION_ENABLED),
        ('components/github', settings.GITHUB_INTEGRATION_ENABLED),
        ('components/dribbble', settings.DRIBBBLE_INTEGRATION_ENABLED),
        ('components/instagram', settings.INSTAGRAM_INTEGRATION_ENABLED),
        ('components/disqus', settings.DISQUS_INTEGRATION_ENABLED),
        ('components/lastfm', settings.LASTFM_INTEGRATION_ENABLED),
        ('components/soundcloud', settings.SOUNDCLOUD_INTEGRATION_ENABLED),
        ('components/bitbucket', settings.BITBUCKET_INTEGRATION_ENABLED),
        ('components/foursquare', settings.FOURSQUARE_INTEGRATION_ENABLED),
        ('components/tent', settings.TENT_INTEGRATION_ENABLED),
        ('components/steam', settings.STEAM_INTEGRATION_ENABLED),
        ('components/stackoverflow', settings.STACKOVERFLOW_INTEGRATION_ENABLED),
    )
    # jquery.url???

    includes = ','.join('js/' + path for path, include in js_files if include)

    subprocess.check_call(shlex.split(
        'r.js -o baseUrl={0}/static/ name=js/components/base include={1}'
        ' mainConfigFile={0}/static/js/components/base.js paths.jquery=empty:'
        ' out={2}scripts-{3}.min.js'.format(
            PATH_TO_HERE, includes, OUT_PATH,
            settings.COMPRESS_REVISION_NUMBER)))

    print 'JavaScript Combined and Minified: {0}scripts-{1}.min.js'.format(
        OUT_PATH, settings.COMPRESS_REVISION_NUMBER)


if __name__ == "__main__":
    compress_statics()
