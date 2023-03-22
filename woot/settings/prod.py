"""Production settings and globals."""

#local
from woot.settings.common import *

#util
from os import environ

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = environ.get('EMAIL_PORT', 587)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
########## END EMAIL CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)
########## END SECRET CONFIGURATION


########## DATABASE CONFIGURATION
# installed mysql-connector-python from pip install git+https://github.com/multiplay/mysql-connector-python
# load database details from database config file
if exists(join(ACCESS_ROOT, DB_ACCESS)):
	with open(join(ACCESS_ROOT, DB_ACCESS), 'r') as db_json:
		db_data = json.load(db_json)

DATABASES = {
	'default': {
		'ENGINE': db_data['backend'],
		'NAME': db_data['name'],
		'USER': db_data['user'],
		'PASSWORD': db_data['pwd'],
		'HOST': db_data['host'], # Set to empty string for localhost.
		'PORT': db_data['port'], # Set to empty string for default.
	}
}
########## END DATABASE CONFIGURATION
