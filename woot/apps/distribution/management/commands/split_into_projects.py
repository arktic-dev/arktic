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
						audio_path = tokens[0]
						utterance = tokens[1]
						relfile_dictionary.update({
							audio_path: {
								'utterance': utterance,
								'grammar_name': grammar_name,
							},
						})

		print(relfile_dictionary)

		# 3. loop over transcriptions
		# 4. fetch utterance and relfile_name based on dictionary
		# 5. get_or_create new project and set project on transcription
		# 6. if part of a job, create new job under project
		# 7. Add revision to new job if necessary

		# mysql dump:
		# mysqldump -u arkaeologic -h arkaeologic.mysql.pythonanywhere-services.com -p 'arkaeologic$arktic' > db.dat
		#
