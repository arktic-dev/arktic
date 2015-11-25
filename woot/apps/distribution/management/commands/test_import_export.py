# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.transcription.models import Revision
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

		# make_option('--client', # option that will appear in cmd
		# 	action='store', # no idea
		# 	dest='client', # refer to this in options variable
		# 	default='', # some default
		# 	help='Name of client' # who cares
		# ),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):
		# 1. define data root as test directory
		data_root = join(settings.SITE_ROOT, 'test')
