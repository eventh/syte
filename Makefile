# Makefile for syte

.PHONY = clean compress local heroku all

# Push to heroku
all heroku:
	@git push
	@git push heroku master

# Run Syte locally on 127.0.0.1:8000
local:
	@python manage.py collectstatic --noinput
	@foreman start --port=8000 --procfile=Procfile-dev --env=.env

# Compress css and js files
compress:
	@cd syte; python compress.py

# Remove generated files
clean:
	rm -f *.pyc */*.pyc */*/*.pyc */*/*/*.pyc
