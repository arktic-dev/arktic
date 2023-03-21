"""Common settings and globals."""

#util
import os
from pathlib import Path
from datetime import timedelta
from os.path import abspath, basename, dirname, join, normpath, expanduser, exists
from sys import path
import string
import json

#mysql: https://github.com/PyMySQL/mysqlclient-python
#rabbitmq: https://www.rabbitmq.com/man/rabbitmqctl.1.man.html
#celery: https://zapier.com/blog/async-celery-example-why-and-how/

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

########## JOBS
NUMBER_OF_TRANSCRIPTIONS_PER_JOB = 50
JOB_ID_CHARS = string.ascii_uppercase + string.digits
JOB_ID_LENGTH = 8

########## TESTS
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## AUTH
AUTH_USER_MODEL = 'users.User'

########## AUDIO CONFIGURATION

NUMBER_OF_AUDIO_FILE_BINS = 100
AUDIO_SAMPLE_WIDTH = 2

########## END AUDIO CONFIGURATION

########## ALLOWED HOSTS
ALLOWED_HOSTS = [
	'localhost',
	'arkaeologic.pythonanywhere.com',
]

########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = Path(abspath(__file__)).parent.parent

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = DJANGO_ROOT.parent

# Site name:
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
	('Nicholas Piano', 'nicholas.d.piano@gmail.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': DJANGO_ROOT / 'db.sqlite3',
	}
}
########## END DATABASE CONFIGURATION


########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/London'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = Path(normpath(join(DJANGO_ROOT, 'media')))

MEDIA_TEMP_ROOT = MEDIA_ROOT / 'temp__data__qsq23qw3'

if not exists(MEDIA_TEMP_ROOT):
	os.makedirs(MEDIA_TEMP_ROOT)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(DJANGO_ROOT, 'static'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
	normpath(join(DJANGO_ROOT, 'assets')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"8hbo@s@z$tg2@o!x8dtf%@&!3+ury6_nm5w1zi$3c^)=k19j^0"
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
	normpath(join(DJANGO_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [DJANGO_ROOT / 'templates'],
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
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE = (
	# Use GZip compression to reduce bandwidth.
	'django.middleware.gzip.GZipMiddleware',

	# Default Django middleware.
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = '%s.urls' % SITE_NAME
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
	# Default Django apps:
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# Useful template tags:
	'django.contrib.humanize',

	# Admin panel and documentation:
	'django.contrib.admin',
	'django.contrib.admindocs',
)

LOCAL_APPS = (
	# Transcription object definition and processing
	'woot.apps.transcription',

	# # Client registration and job creation
	'woot.apps.distribution',

	# # Pre-client frontend
	'woot.apps.pages',

	# Augmented auth model
	'woot.apps.users',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		}
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'filters': ['require_debug_false'],
			'class': 'django.utils.log.AdminEmailHandler'
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler'
		}
	},
	'loggers': {
		'django.request': {
			'handlers': ['mail_admins', 'console'],
			'level': 'ERROR',
			'propagate': True,
		},
	}
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## FILE UPLOAD CONFIGURATION
FILE_UPLOAD_HANDLERS = (
	'django.core.files.uploadhandler.MemoryFileUploadHandler',
	'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
########## END FILE UPLOAD CONFIGURATION
