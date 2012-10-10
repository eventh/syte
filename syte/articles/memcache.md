Add memcache to Syte hosted on Heroku

[Syte](http://rigoneri.github.com/syte/) is a simple but powerful packaged
personal site with social integrations. Memcache is a key/value store used for
caching. There are two Heroku memcache addons:
[Memcache](https://devcenter.heroku.com/articles/memcache) and
[MemCachier](https://devcenter.heroku.com/articles/memcachier). Both have a
free to use level which is sufficient for Syte.


Start by adding the addon to your Heroku app:
> heroku addons:add memcachier:dev


Then either A, pull the necessary changes from
[my Syte fork](https://github.com/eventh/syte/tree/heroku-memcache):
> git pull git://github.com/eventh/syte.git heroku-memcache


Or B, follow these three simple steps to modify your Syte installation:

1. Add *pylibmc==1.2.3* and *django-pylibmc-sasl==0.2.4* to *requirements.txt*
2. Add the following configuration to the bottom of the syte/settings.py file:

        # Heroku memcachier addon, cache configuration
        os.environ['MEMCACHE_SERVERS'] = os.environ.get('MEMCACHIER_SERVERS', '')
        os.environ['MEMCACHE_USERNAME'] = os.environ.get('MEMCACHIER_USERNAME', '')
        os.environ['MEMCACHE_PASSWORD'] = os.environ.get('MEMCACHIER_PASSWORD', '')
        
        if DEPLOYMENT_MODE == 'dev':
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

3. Add cache middlewares to *MIDDLEWARE_CLASSES* in syte/settings.py, such
    that 'django.middleware.cache.UpdateCacheMiddleware' comes first, and
    'django.middleware.cache.FetchFromCacheMiddleware' comes last. Your
    MIDDLEWARE_CLASSES should now look like this:

        MIDDLEWARE_CLASSES = (
            'django.middleware.cache.UpdateCacheMiddleware',
            'django.middleware.gzip.GZipMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.cache.FetchFromCacheMiddleware',
        )


After you push these changes to Heroku, all Syte pages will be cached for 10
minutes by memcache. The cache time can be changed with the
CACHE_MIDDLEWARE_SECONDS setting.


In my heroku-memcache branch I've also added never_cache decorator to error
pages see:  
https://github.com/eventh/syte/blob/heroku-memcache/syte/views/home.py
