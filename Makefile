# Makefile for syte

.PHONY = clean compress local heroku all foreman collect s3 refresh

# Push to heroku
heroku:
	-@git commit -a
	@git push
	@git push dev

# Push complete production
all: compress heroku s3 refresh

# Have heroku upload static files to amazon S3
s3:
	@heroku run python manage.py collectstatic --noinput --app eventh-dev

# Have heroku refresh caches of certain views
refresh:
	@heroku run python syte/refresh.py github bitbucket ohloh --app eventh-dev

# Run Syte locally on django dev server at 127.0.0.1:8000
local: collect
	python manage.py runserver

# Run Syte locally with foreman
foreman: collect
	foreman start --port=8000 --env=.env

# Compress css and js files
compress:
	@python syte/compress.py

# Collect static files locally
collect:
	@python manage.py collectstatic --noinput

# Remove generated files
clean:
	rm -f *.pyc */*.pyc */*/*.pyc */*/*/*.pyc
	rm -fr static/
