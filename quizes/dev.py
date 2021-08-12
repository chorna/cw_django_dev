import environ

env = environ.Env()

from .settings import *


SECRET_KEY = env('DJANGO_SECRET_KEY')
DATABASES['default'] = env.db('DATABASE_URL')
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
    ]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = [
    '127.0.0.1',
]