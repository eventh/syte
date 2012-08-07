# Makefile for syte

.PHONY = clean compress local heroku all foreman collect static s3

# Push to heroku
all heroku:
	-@git commit -a
	@git push
	@git push heroku stable:master

# Have heroku upload static files to amazon S3
s3 static:
	@heroku run python manage.py collectstatic --noinput --app eventh

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
