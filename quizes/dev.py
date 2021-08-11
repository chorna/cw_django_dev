import environ

env = environ.Env()

from .settings import *


SECRET_KEY = env('DJANGO_SECRET_KEY')

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']