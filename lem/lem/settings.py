import logging
import os
import sys

from envparse import env


# Paths
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Security
SECRET_KEY = env.str('SECRET_KEY', default='3.14159265359')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = []
USE_X_FORWARDED_HOST = True

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Logging
LOG_LEVEL = env.str('LOG_LEVEL', default='DEBUG' if DEBUG else 'INFO')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
            'propagate': True,
        },
        'content': {
            'level': LOG_LEVEL,
            'handlers': ['sentry', 'console'],
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

logger = logging.getLogger('content')


SENTRY_DSN = env.str('SENTRY_DSN', default=None)
if SENTRY_DSN:
    RAVEN_CONFIG = {
        'dsn': SENTRY_DSN,
    }


# RestFul
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'utils.pagination.Pagination',
    'PAGE_SIZE': env.int('PAGE_SIZE', default=50),
}


# Application
SITE_NAME = 'Luiza Employee Manager'
SITE_URL = env.str('SITE_URL', default='http://local.lem.com.br')
INSTALLED_APPS = [
    'raven.contrib.django.raven_compat',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'storages',
    'rest_framework',

    'v1.apps.V1Config',
]
ROOT_URLCONF = 'lem.urls'
WSGI_APPLICATION = 'lem.wsgi.application'


# Internationalization
LANGUAGE_CODE = 'en'
ADMIN_LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Database
if 'SQL_HOST' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.str('SQL_NAME', default='lem'),
            'USER': env.str('SQL_USER', default='postgres'),
            'PASSWORD': env.str('SQL_PASSWORD', default=''),
            'HOST': env.str('SQL_HOST', default='localhost'),
            'PORT': env.str('SQL_PORT', default=''),
            'CONN_MAX_AGE': 60,
        }
    }
else:
    logger.warning("You're using a local file as database engine.")
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(PROJECT_DIR, 'lem.sqlite3'),
        }
    }


# Cache
if 'REDIS_URL' in os.environ:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": env.str('REDIS_URL'),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient"
            },
            "KEY_PREFIX": "lem_"
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': env.int('CACHE_TTL', default=5 * 60),
    'DEFAULT_CACHE_ERRORS': False,
    'DEFAULT_CACHE_KEY_FUNC': 'utils.cache.cache_key_constructor',
    'DEFAULT_OBJECT_CACHE_KEY_FUNC': 'utils.cache.cache_key_constructor',
    'DEFAULT_LIST_CACHE_KEY_FUNC': 'utils.cache.cache_key_constructor',
}


# Middlewares
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Templates & Static
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# AWS S3
AWS_ACCESS_KEY_ID = env.str('AWS_KEY', default=None)
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET', default=None)
AWS_STORAGE_BUCKET_NAME = env.str('AWS_BUCKET', default=None)
AWS_S3_CUSTOM_DOMAIN = env.str('CDN_URL', default=None)
AWS_LOCATION = 'lem'
AWS_PRELOAD_METADATA = True
AWS_QUERYSTRING_AUTH = True
AWS_IS_GZIPPED = True

if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'utils.aws.MediaRootS3BotoStorage'
    STATICFILES_STORAGE = 'utils.aws.StaticRootS3BotoStorage'
    S3_URL = '//{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = '//{}media/'.format(S3_URL)
    STATIC_URL = '//{}static/'.format(S3_URL)
    AWS_QUERYSTRING_AUTH = False
else:
    logger.warning("You're using a local storage for static and media files.")
    MEDIA_URL = MEDIA_ROOT + '/'
    STATIC_URL = STATIC_ROOT + '/'


# DEBUG environment
if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['.lem.com.br']
