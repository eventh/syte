# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings


handler404 = 'syte.views.page_not_found_error'
handler500 = 'syte.views.server_error'


urlpatterns = patterns('syte.views',
    (r'^post/(?P<post_id>\w+)/?$', 'blog_post'),
    (r'^tags/(?P<tag_slug>[\s\w\d-]+)/?$', 'blog_tags'),
    (r'^blog.json/?$', 'blog'),
    (r'^about/?$', 'home'),
    (r'^/?$', 'home'),


#Twitter Integration
if settings.TWITTER_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^twitter/(?P<username>\w+)/?$', 'syte.views.twitter'),)


#Github Integration
if settings.GITHUB_OAUTH_ENABLED:
    urlpatterns += patterns('',
        (r'^github/auth/?$', 'syte.views.github_auth'),)

if settings.GITHUB_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^github/(?P<username>\w+)/?$', 'syte.views.github'),)


#Bitbucket Integration
if settings.BITBUCKET_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^bitbucket/(?P<username>\w+)/?$', 'syte.views.bitbucket'),)


#Dribbble Integration
if settings.DRIBBBLE_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^dribbble/(?P<username>\w+)/?$', 'syte.views.dribbble'),)


#Instagram Integration
if settings.INSTAGRAM_OAUTH_ENABLED:
    urlpatterns += patterns('',
        (r'^instagram/auth/?$', 'syte.views.instagram_auth'),)

if settings.INSTAGRAM_INTEGRATION_ENABLED:
    urlpatterns += patterns('syte.views',
        (r'^instagram/(?P<max_id>\w+)/?$', 'instagram_next'),
        (r'^instagram/?$', 'instagram'),)


#LastFM Integration
if settings.LASTFM_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^lastfm/(?P<username>\S+)/?$', 'syte.views.lastfm'),)


#Soundcloud Integration
if settings.SOUNDCLOUD_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^soundcloud/(?P<username>\S+)/?$', 'syte.views.soundcloud'),)


#Ohloh Integration
if settings.OHLOH_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        (r'^ohloh/(?P<username>\w+)/?$', 'syte.views.ohloh'),)


#Static files
urlpatterns += patterns('django.views.generic.simple',
    url(r'^favicon\.ico$', 'redirect_to',
        {'url': settings.STATIC_URL + 'imgs/favicon.ico'}),)
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        (r'^static/(?P<path>.*)$', 'serve'),)
