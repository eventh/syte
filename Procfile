web: python manage.py collectstatic --noinput; gunicorn_django -b 0.0.0.0:$PORT -w 7 -k gevent --max-requests 250 --preload
