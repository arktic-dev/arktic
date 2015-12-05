# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Job
from apps.users.models import User

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
			help='Name of the user to transfer' # who cares
		),

		make_option('--client', # option that will appear in cmd
			action='store', # no idea
			dest='client', # refer to this in options variable
			default='', # some default
			help='Name of the project to transfer' # who cares
		),

		make_option('--project', # option that will appear in cmd
			action='store', # no idea
			dest='project', # refer to this in options variable
			default='', # some default
			help='Name of the project to transfer' # who cares
		),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):
		client_name = options['client']
		project_name = options['project']
		user_name = options['user']

		if client_name:
			for job in Job.objects.filter(is_active=True, client__name=client_name, project__name=project_name):
				print('{}: {} active'.format(job, job.transcriptions.filter(is_active=True).count()))
				if user_name:
					user = User.objects.get(email__contains=user_name)
					job.user = user
					user.jobs.add(job)
					job.save()
					user.save()
		else:
			for job in Job.objects.filter(is_active=True, client__is_demo=False):
				print('{}: {} active'.format(job, job.transcriptions.filter(is_active=True).count()))
				if user_name:
					user = User.objects.get(email__contains=user_name)
					job.user = user
					user.jobs.add(job)
					job.save()
					user.save()
