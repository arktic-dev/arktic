# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.distribution.util import generate_id_token, process_audio
from apps.users.models import User

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

		grouped_by_project_and_user = {}
		total = client.transcriptions.count()
		for i, transcription in enumerate(client.transcriptions.all()):
			transcription_file_name = basename(transcription.audio_file.name)
			transcription_file_name_stripped = splitext(transcription_file_name)[0][:-8] + '.wav'

			if transcription_file_name_stripped in completed_transcriptions:
				transcription_data = completed_transcriptions[transcription_file_name_stripped]
				user_email = transcription_data['user_email']

				if transcription.project.name not in grouped_by_project_and_user:
					grouped_by_project_and_user[transcription.project.name] = {}

				if user_email not in grouped_by_project_and_user[transcription.project.name]:
					grouped_by_project_and_user[transcription.project.name][user_email] = {}

				grouped_by_project_and_user[transcription.project.name][user_email].update({
					transcription.pk: transcription_data['revision_utterance'],
				})

		for project in client.projects.all():
			if project.name in grouped_by_project_and_user:
				user_data = grouped_by_project_and_user[project.name]

				for user in User.objects.all():
					if user.email in user_data:
						transcription_data = user_data[user.email]

						print('CREATING JOB IN PROJECT {} FOR USER {}'.format(project.name, user.email))

						for transcription_pk, revision_utterance in transcription_data.items():
							transcription = client.transcriptions.get(pk=transcription_pk)

							print('ADDING TRANSCRIPTION {} TO JOB'.format(transcription.pk))
