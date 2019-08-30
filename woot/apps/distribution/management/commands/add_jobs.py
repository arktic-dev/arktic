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
from os.path import join, basename, exists, isdir, splitext
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
		client = Client.objects.get(name=client_name)

		# 1. open failsafe data
		completed_transcriptions = {}
		failsafe_path = join(root, 'extraction_0_2019-08-30-09-46_number-2300.csv')
		with open(failsafe_path, 'r') as failsafe_file:
			for line in failsafe_file.readlines():
				tokens = line.rstrip().split('|')

				transcription_file_name = basename(tokens[0])
				revision_utterance = tokens[1]
				user_email = tokens[2]

				completed_transcriptions.update({
					transcription_file_name: {
						'revision_utterance': revision_utterance,
						'user_email': user_email,
					},
				})

		total = client.transcriptions.count()
		for i, transcription in enumerate(client.transcriptions.all()):
			transcription_file_name = basename(transcription.audio_file.name)
			transcription_file_name_stripped = splitext(transcription_file_name)[0][:-8] + '.wav'

			if transcription_file_name_stripped in completed_transcriptions:
				transcription_data = completed_transcriptions[transcription_file_name]
				print('{}/{}'.format(i+1, total), transcription_file_name_stripped, transcription_data)
