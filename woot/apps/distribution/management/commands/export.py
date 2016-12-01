# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Project, Client
from apps.transcription.models import Revision
from apps.distribution.util import generate_id_token, process_audio

# util
import os
import json
from optparse import make_option

# var
spacer = ' '*10

### Command
class Command(BaseCommand):
	option_list = BaseCommand.option_list + (

		make_option('--client', # option that will appear in cmd
			action='store', # no idea
			dest='client', # refer to this in options variable
			default='', # some default
			help='Name of client' # who cares
		),

		make_option('--project', # option that will appear in cmd
			action='store', # no idea
			dest='project', # refer to this in options variable
			default='', # some default
			help='Name of project' # who cares
		),

		make_option('--completed', # option that will appear in cmd
			action='store_true', # no idea
			dest='completed', # refer to this in options variable
			default=False, # some default
			help='Name of project' # who cares
		),

		make_option('--users', # option that will appear in cmd
			action='store_true', # no idea
			dest='users', # refer to this in options variable
			default=False, # some default
			help='Toggle username in export csv' # who cares
		),

		make_option('--number', # option that will appear in cmd
			action='store', # no idea
			dest='number', # refer to this in options variable
			default=-1, # some default
		),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):
		root = settings.DATA_ROOT
		client_name = options['client']
		client_root = os.path.join(root, client_name)
		project_name = options['project']
		include_users = options['users']
		number_to_export = int(options['number'])

		if client_name and project_name:
			project = Project.objects.get(client__name=client_name, name=project_name)
			project.update()
			project.export(client_root, users_flag=include_users, number_to_export=number_to_export)

		else:
			print('Listing clients and projects in order of age. Add "--completed" flag to exclude active projects.')
			print('Nothing will be exported.')
			for client in Client.objects.all():
				print('client {}'.format(client.name))
				for project in client.projects.all():
					project.update()
					active_transcriptions = project.active_transcriptions
					if options['completed']:
						if active_transcriptions==0:
							print('client {}, project {}, {}/{} completed transcriptions, {} not yet exported.'.format(client.name, project.name, project.total_transcriptions-project.active_transcriptions, project.total_transcriptions, project.unexported_transcriptions))
					else:
						print('client {}, project {}, {}/{} completed transcriptions, {} not yet exported.'.format(client.name, project.name, project.total_transcriptions-project.active_transcriptions, project.total_transcriptions, project.unexported_transcriptions))
