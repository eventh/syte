# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.conf import settings


handler404 = 'syte.views.page_not_found_error'
handler500 = 'syte.views.server_error'

urlpatterns = patterns('',
    url(r'^post/(?P<post_id>\w+)/?$', 'syte.views_tumblr.blog_post'),
    url(r'^tags/(?P<tag_slug>[\s\w\d-]+)/?$', 'syte.views_tumblr.blog_tags'),
    url(r'^blog.json/?$', 'syte.views_tumblr.blog'),
    url(r'^about/?$', 'syte.views.home'),
    url(r'^/?$', 'syte.views.home'),
)

#Twitter Integration
if settings.TWITTER_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^twitter/(?P<username>\w+)/?$', 'syte.views_twitter.twitter'),
    )

#Github Integration
if settings.GITHUB_OAUTH_ENABLED:
    urlpatterns += patterns('',
        url(r'^github/auth/?$', 'syte.views_github.github_auth'),
    )

if settings.GITHUB_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^github/(?P<username>\w+)/?$', 'syte.views_github.github'),
    )

#Bitbucket Integration
if settings.BITBUCKET_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^bitbucket/(?P<username>\w+)/?$', 'syte.views_bitbucket.bitbucket'),
    )

#Dribbble Integration
if settings.DRIBBBLE_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^dribbble/(?P<username>\w+)/?$', 'syte.views_dribbble.dribbble'),
    )

#Instagram Integration
if settings.FOURSQUARE_OAUTH_ENABLED:
    urlpatterns += patterns('',
        url(r'^foursquare/auth/?$', 'syte.views_foursquare.foursquare_auth'),
    )

if settings.FOURSQUARE_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^foursquare/?$', 'syte.views_foursquare.foursquare'),
    )

#Foursquare Integration
if settings.INSTAGRAM_OAUTH_ENABLED:
    urlpatterns += patterns('',
        url(r'^instagram/auth/?$', 'syte.views_instagram.instagram_auth'),
    )

if settings.INSTAGRAM_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^instagram/(?P<max_id>\w+)/?$', 'syte.views_instagram.instagram_next'),
        url(r'^instagram/?$', 'syte.views_instagram.instagram'),
    )

#LastFM Integration
if settings.LASTFM_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^lastfm/(?P<username>\S+)/?$', 'syte.views_lastfm.lastfm'),
    )

#Soundcloud Integration
if settings.SOUNDCLOUD_INTEGRATION_ENABLED:
    urlpatterns += patterns('',
        url(r'^soundcloud/(?P<username>\S+)/?$', 'syte.views_soundcloud.soundcloud'),
    )

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
