# Makefile for syte

.PHONY = clean compress local heroku

# Run Syte locally on 127.0.0.1:8000
local:
	@python manage.py collectstatic --noinput
	@foreman start --port=8000

# Push to heroku
heroku:
	@git push heroku master

# Compress css and js files
compress:
	@cd syte; python compress.py

# Remove generated files
clean:
	rm -f *.pyc */*.pyc */*/*.pyc */*/*/*.pyc
