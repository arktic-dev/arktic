"""Development settings and globals."""

#util
from os.path import join, normpath
import os

#local
from woot.settings.common import *

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
DATABASE_USER = os.getenv('DB_USER')
DATABASE_PWD = os.getenv('DB_PWD')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'arktic_db',
#     'USER': DATABASE_USER,
#     'PASSWORD': DATABASE_PWD,
#     'HOST': 'localhost',
#   }
# }

# 1. install psycopg2: 'pip install psycopg2'
# 2. install postgres: 'brew install postgres'
# 3. set postgres to start at startup: 'ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents'
# 4. <Already done by brew> create db cluster: 'postgres -D /usr/local/var/postgres'
# 5. <Already done by brew> create default db: initdb /usr/local/var/postgres -E utf8
# 6. create main user: 'createuser -d -P nicholas'
# 7. access default database: 'psql postgres'
# 8. create main database: '~# CREATE DATABASE arktic_db; ctrl+D'
# 9. change backend in django code
# 10. syncdb

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'arktic_db',
    'USER': DATABASE_USER,
    'PASSWORD': DATABASE_PWD,
    'HOST': 'localhost',
  }
}

#1. install mysql python package
#2. set up environment variables
#3. create database
#4. syncdb
#5. run

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
  }
}
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
  'debug_toolbar',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
  'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {

}
########## END TOOLBAR CONFIGURATION
