.PHONY: install install-prd static migrate runserver test coverage lint clean snitch


install:
	pip install -r requirements/dev.txt

install-prd:
	pip install -r requirements/prd.txt

static:
	python lem/manage.py collectstatic --no-input

migrate:
	python lem/manage.py migrate

runserver:
	python lem/manage.py runserver

test:
	python lem/manage.py test lem --no-input

clean:
	rm -rf .coverage html-coverage .cache

coverage:
	$(MAKE) clean
	$(MAKE) test

lint:
	flake8
