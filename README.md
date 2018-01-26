[![Build Status](https://travis-ci.org/joaodaher/lem.svg?branch=master)](https://travis-ci.org/joaodaher/lem)
[![codecov](https://codecov.io/gh/joaodaher/lem/branch/master/graph/badge.svg)](https://codecov.io/gh/joaodaher/lem)
[![python](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
[![django](https://img.shields.io/badge/django-2-green.svg)](https://www.djangoproject.com/)
# Luiza Employee Manager
Service for managing company's employees.

Microservice-based RestFul API for programmatic integrations and Admin for user-friendly interface.


## Documentation

Visit the [API Docs]() for more information about each endpoint available.


# Developing Environment

## Setup
  - clone this project
  - setup [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/)
  - create a virtualenv (`mkvirtualenv lem --python=python3`)
  - install dependencies (`make install`)

## Running the app
  - prepare your database: `make migrate`
  > By default, the database is SQLite. See Production Environment for advanced usage.
  - fire up the server: `make runserver`
  
## Tests
To run tests, run `make test`.

  To get a better code coverage report: `make coverage`
  and open the `html-coverage/index.html` file in your browser.

## Lint
To check the code style, run `make lint`.


# Production Environment

The Django app defines development from production environment through environment variables.

If not environment variable is set up, the default behaviour is development environment,
and all default settings aims a fluid and rapid development environment.

> "You develop a hundred times to deploy 1 time."

## Django

   - Turn off *debug* with: `DEBUG=0`
   - Set Site's domain with `SITE_URL=<my-domain>`


## Database

Production database is, by default, PostgreSQL.

   - Set up the database host with: `SQL_HOST=<my-db-host>`
   - Set up the database username with: `SQL_USER=<my-db-username>`
   - Set up the database password with: `SQL_PASSWORD=<my-db-password>`
   - Set up the database name with: `SQL_NAME=<my-db-name>`
   - Optionally, set up the database port with: `SQL_PORT=<my-db-port>`


## Cache

Production caching system is, by default, Redis.

   - Set up the Redis server with a single connection URL: `REDIS_URL=redis://<my-cache-host>`
   - Optionally, set the default cache duration for GET resquests with: `CACHE_TTL=<seconds>`
   
   
## Static Files

Production static files server is, by default, AWS S3.

   - Set the AWS Key ID with: `AWS_KEY=<my-aws-key>`
   - Set the AWS Secret Key with: `AWS_KEY=<my-aws-secret>`
   - Set the AWS S3 Bucket name with: `AWS_BUCKET=<my-s3-bucket>`
   - Optionally, set the CDN server with: `CDN_URL=<my-cdn-url>`


## Logging

Production logging system is, by default, Sentry.

   - Set Sentry configuration with: `SENTRY_DSN=<my-sentry-dsn>`
   - Optionally, set the logging level with: `LOG_LEVEL=<my-log-level>`

## APM Monitoring

Production monitoring tool is, by default, NewRelic.

   - Set NewRelic Key with: `NEW_RELIC_LICENSE_KEY=<my-newrelic-key>`
   - Any additional configuration can be used with [more environment variables](https://docs.newrelic.com/docs/agents/python-agent/installation-configuration/python-agent-configuration#environment-variables).


## Running Server

Production server is run, by default, with Gunicorn.

   - Set server binding port with: `PORT=<my-port>`
   - Run and/or customise using Procfile.
   
   
## Healthcheck

Healthcheck URL is `/healthcheck` and assures the database connection aliveness.