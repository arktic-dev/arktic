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
from os.path import join, basename, exists, isdir
import json
from optparse import make_option

# var
spacer = ' '*10

### Command
class Command(BaseCommand):

	args = ''
	help = ''

	def handle(self, *args, **options):
		root = settings.DATA_ROOT
		client_name = 'voxgen'

		# 1. open failsafe data
		# 2. group by project and user
		grouped = {}
		failsafe_path = join(root, 'extraction_0_2019-08-30-09-46_number-2300.csv')
		with open(failsafe_path, 'r') as failsafe_file:
			for line in failsafe_file.readlines():
				tokens = line.rstrip().split('|')

				# 1. identify transcription object
				transcription_file_name = basename(tokens[0])
				transcription = Client.transcriptions.filter(audio_file_name=transcription_file_name)

				if transcription:
					print(transcription)
