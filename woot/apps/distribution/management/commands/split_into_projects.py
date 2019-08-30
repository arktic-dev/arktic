# apps.distribution.command: split_into_projects

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client, Project
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

		# 1. Get specific project
		client_name = 'voxgen'
		client = Client.objects.get(name=client_name)

		project_name = 'extraction_0'
		project = Project.objects.get(name=project_name)

		# 2. Load all relfiles into dictionary with
		# {
		#   [audio_file_name]: {
		#     utterance: '',
		#     relfile_name: '',
		#   },
		# }
		relfile_dictionary = {}
		project_root = join(root, client_name, project_name)
		for grammar_name in os.listdir(project_root):
			grammar_path = join(project_root, grammar_name)
			if isdir(grammar_path):
				with open(join(grammar_path, '{}.csv'.format(grammar_name)), 'r') as grammar_file:
					for line in grammar_file.readlines():
						tokens = line.rstrip().split('|')
						audio_path = basename(tokens[0])
						utterance = tokens[1]
						relfile_dictionary.update({
							audio_path: {
								'utterance': utterance,
								'grammar_name': grammar_name,
							},
						})

		# 3. loop over transcriptions
		for transcription in project.transcriptions.all():

			print('>>>')

			# 4. fetch utterance and relfile_name based on dictionary
			audio_path = basename(transcription.audio_file.name)
			print('PATH', audio_path)
			grammar_details = relfile_dictionary[audio_path]

			# 5. set utterance
			utterance = grammar_details['utterance']
			print('UTTERANCE', utterance)
			# transcription.utterance = utterance

			# 6. get_or_create new project and set project on transcription
			grammar_name = grammar_details['grammar_name']
			print('PROJECT', grammar_name)
			# grammar_project, grammar_project_created = client.projects.get_or_create(name=grammar_name)

			# 6. if part of a job, create new job under project
			if transcription.job.all():
				print('JOB', transcription.job.all())
				print('REVISION', transcription.revisions.all())

			print('<<<')


		# 7. Add revision to new job if necessary

		# mysql dump:
		# mysqldump -u arkaeologic -h arkaeologic.mysql.pythonanywhere-services.com -p 'arkaeologic$arktic' > db.dat
		#
