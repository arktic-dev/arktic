# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.distribution.util import generate_id_token, process_audio

# util
import os
from os.path import join
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
			help='Name of the client' # who cares
		),

		make_option('--path', # option that will appear in cmd
			action='store', # no idea
			dest='path', # refer to this in options variable
			default='', # some default
			help='Path to the ruleset' # who cares
		),
	)

	args = ''
	help = ''

	def handle(self, *args, **options):
		client_name = options['client']
		path = options['path']

		client = Client.objects.get(name=client_name)
		client.ruleset = File(open(path, 'r'))
		client.has_ruleset = True
		client.save()
