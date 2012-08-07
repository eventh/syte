import os
import sys
import subprocess
import shlex


PATH = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(PATH, 'static/js/min/')
sys.path.append(os.path.join(PATH, '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'syte.settings'


from django.conf import settings


def compress_statics():
    """Compress both CSS and JavaScript files."""
    try:
        for path in (os.path.join(PATH, 'static/css'), OUT_PATH):
            if not os.path.exists(path):
                os.mkdir(path)
    except OSError:
        print 'Make sure to create "syte > static > css" and ' \
                '"syte > static > js > min" before compressing statics.'

    compress_styles()
    compress_js()


def compress_styles():
    less_path = os.path.join(PATH, 'static/less/styles.less')
    css_path = os.path.join(PATH, 'static/css/')

    subprocess.check_call(
        shlex.split('lessc {0} {1}styles-{2}.min.css -yui-compress'.format(
            less_path, css_path, settings.COMPRESS_REVISION_NUMBER)))

    print 'CSS Styles Generated: {0}styles-{1}.min.css'.format(
        css_path, settings.COMPRESS_REVISION_NUMBER)


def compress_js():
    js_files = (
        ('js/libs/handlebars', True),
        ('js/libs/moment', True),
        ('js/libs/bootstrap-modal', True),
        ('js/libs/spin', True),
        ('js/libs/prettify', True),
        ('js/components/blog-posts', True),
        ('js/components/mobile', True),
        ('js/components/links', True),
        ('js/components/twitter', settings.TWITTER_INTEGRATION_ENABLED),
        ('js/components/dribbble', settings.DRIBBBLE_INTEGRATION_ENABLED),
        ('js/components/github', settings.GITHUB_INTEGRATION_ENABLED),
        ('js/components/instagram', settings.INSTAGRAM_INTEGRATION_ENABLED),
        ('js/components/disqus', settings.DISQUS_INTEGRATION_ENABLED),
        ('js/components/lastfm', settings.LASTFM_INTEGRATION_ENABLED),
        ('js/components/bitbucket', settings.BITBUCKET_INTEGRATION_ENABLED),
        ('js/components/soundcloud', settings.SOUNDCLOUD_INTEGRATION_ENABLED),
        ('js/components/ohloh', settings.OHLOH_INTEGRATION_ENABLED),
    )

    includes = ','.join(path for path, include in js_files if include)

    subprocess.check_call(shlex.split(
        'r.js -o baseUrl={0}/static/ name=js/components/base include={1}'
        ' mainConfigFile={0}/static/js/components/base.js paths.jquery=empty:'
        ' out={2}scripts-{3}.min.js'.format(
            PATH, includes, OUT_PATH, settings.COMPRESS_REVISION_NUMBER)))

    print 'JavaScript Combined and Minified: {0}scripts-{1}.min.js'.format(
        OUT_PATH, settings.COMPRESS_REVISION_NUMBER)

    # Minify require.js
    # TODO: include require.js above, and use jquery from google CDN!!
    subprocess.check_call(shlex.split(
        'uglifyjs -o {0}require.min.js {1}/static/js/libs/require.js'.format(
            OUT_PATH, PATH)))

    print 'require.js Minified: {0}require.min.js'.format(OUT_PATH)


if __name__ == "__main__":
    compress_statics()
    sys.exit()
