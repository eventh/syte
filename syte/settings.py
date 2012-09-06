# -*- coding: utf-8 -*-
# Django settings for syte project.
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Even Wiik Thomassen', 'eventh@gmail.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = True

SECRET_KEY = '5c^pml#7e3d$zor%*_7y098(l0i=d3$+y_((11-_j0&amp;f9rw9%)'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'syte.urls'

WSGI_APPLICATION = 'syte.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "syte.context_processor.site_pages",
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'gunicorn',
)

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

try:
    from personal_syte_settings import *
except ImportError:
    from syte_settings import *


# Heroku memcachier addon, cache configuration
os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '')
os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')

if os.environ.get('DISABLE_CACHE', False):
    pass
elif DEPLOYMENT_MODE == 'dev':
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
            'LOCATION': os.environ.get('MEMCACHIER_SERVERS', ''),
            'BINARY': True,
        }
    }
