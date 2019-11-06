# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.users.models import User
from apps.transcription.models import Transcription, Revision

# util
import os
import json
import time
from optparse import make_option

# var
spacer = ' '*10

### Command
class Command(BaseCommand):

	option_list = BaseCommand.option_list + (

		make_option('--email', # option that will appear in cmd
			action='store', # no idea
			dest='email', # refer to this in options variable
			default='', # some default
			help='Name of the experiment to import' # who cares
		),

		make_option('--password', # option that will appear in cmd
			action='store', # no idea
			dest='password', # refer to this in options variable
			default='', # some default
			help='Name of the series' # who cares
		),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):

		user_email = options['email']
		user_password = options['password']

		if user_email and user_password:
			user = User.objects.get(email=email)
			user.set_password(user_password)
			user.save()

		print('User details ---')
		print('{} {}'.format(User.objects.count(), 'user' if User.objects.count()==1 else 'users'))
		for user in User.objects.all():
			print('---')
			# email
			print('Email: {}'.format(user.email))
			print('\tTotal revisions: {}'.format(user.completed_revisions))
			print('\tTotal audio time: {}'.format(time.strftime('%H:%M:%S', time.gmtime(user.total_audio_time))))
			print('')
		print('')
