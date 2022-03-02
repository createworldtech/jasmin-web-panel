# -*- coding: utf-8 -*-
from .com import *  # noqa

# SCRIPT_NAME is appended only if STATIC_URL/MEDIA_URL is relative (e.g. does not beging with "http", "https", "/")
# See: Fixed #25598 -- Added SCRIPT_NAME prefix to STATIC_URL and MEDIA_URL
# https://github.com/django/django/commit/c574bec0929cd2527268c96a492d25223a9fd576
# https://github.com/django/django/blob/main/django/conf/__init__.py#L137
STATIC_URL = 'static/'
MEDIA_URL = 'media/'

DATABASES = {
    'default': env.db('PRODB_URL', default='postgres://postgres:123456@127.0.0.1:5432/jasmin_webdb')
}

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['*'])

INSTALLED_APPS += ("gunicorn", )

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(str(ROOT_DIR), 'logs/app.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(str(ROOT_DIR), 'logs/django.log'),
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}