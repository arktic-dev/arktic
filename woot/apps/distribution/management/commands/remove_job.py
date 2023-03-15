# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from woot.apps.distribution.models import Job
from woot.apps.users.models import User

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

		make_option('--user', # option that will appear in cmd
			action='store', # no idea
			dest='user', # refer to this in options variable
			default='', # some default
		),

		make_option('--id', # option that will appear in cmd
			action='store', # no idea
			dest='id', # refer to this in options variable
			default='', # some default
		),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):
		user_name = options['user']
		id_token = options['id']

		if user_name:
			user = User.objects.get(email__contains=user_name)

			for job in user.jobs.filter(is_active=True):
				for transcription in job.transcriptions.filter(is_active=True):
					transcription.is_available = True
					transcription.save()

		elif id_token:
			job = Job.objects.get(id_token=id_token)
			for transcription in job.transcriptions.filter(is_active=True):
				transcription.is_available = True
				transcription.save()
