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

	option_list = BaseCommand.option_list + (

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
		root = settings.DATA_ROOT
		client_name = options['client']
		project_name = options['project']

		if client_name and project_name:
			if exists(join(root, client_name)):
				if exists(join(root, client_name, project_name)):
					# create client and project
					client, client_created = Client.objects.get_or_create(name=client_name)
					print('client {}... {}{}'.format(client_name, 'already exists.' if not client_created else 'created.', spacer))

					project, project_created = client.projects.get_or_create(name=project_name)
					print('client {}, project {}... {}{}'.format(client_name, project_name, 'already exists.' if not project_created else 'created.', spacer))

					# 2-4. list all files in the project directory and create transcriptions
					audio_root = join(root, client_name, project_name)
					audio_files = [join(d,f) for d,ds,fs in os.walk(audio_root) for f in fs if '.wav' in f] # double list of filenames to single list
					relfile_name = [f for f in os.listdir(audio_root) if '.csv' in f] # return single item

					relfile_dictionary = {}
					if relfile_name:
						relfile_path = join(root, client_name, project_name, relfile_name[0])

						with open(relfile_path, 'r') as open_relfile:
							# super complicated dictionary comprehension
							relfile_dictionary = {basename(line.rstrip().split('|')[0]):{'utterance':line.rstrip().split('|')[1], 'path':line.rstrip().split('|')[0]} for line in open_relfile.readlines()}

					for i, audio_file in enumerate(audio_files):
						if project.transcriptions.filter(audio_file_name='{}'.format(audio_file)).count()==0:
							audio_file_path = audio_file
							utterance = relfile_dictionary[basename(audio_file)]['utterance'] if relfile_dictionary else ''
							(seconds, rms_values) = process_audio(audio_file_path)

							max_rms = max(rms_values)
							rms_values = [float(value)/float(max_rms) for value in rms_values]
							audio_rms = json.dumps(rms_values)

							with open(audio_file_path, 'rb') as open_audio_file:
								transcription, transcription_created = project.transcriptions.get_or_create(client=client,
																																														utterance=utterance,
																																														audio_file_name=audio_file_path,
																																														is_active=True,
																																														is_available=True)

								if transcription_created:
									transcription.id_token = generate_id_token('transcription','Transcription')
									transcription.audio_time = seconds
									transcription.audio_rms = audio_rms
									transcription.audio_file = File(open_audio_file)
									transcription.save()

							print('client {}, project {}, file {}... created ({}/{})'.format(client_name, project_name, audio_file, i+1, len(audio_files)), end='\r' if i<len(audio_files)-1 else '\n')

						else:
							print('client {}, project {}, file {}... already exists. ({}/{})'.format(client_name, project_name, audio_file, i+1, len(audio_files)), end='\r' if i<len(audio_files)-1 else '\n')

					project.active_transcriptions = project.transcriptions.filter(is_active=True).count()
					project.total_transcriptions = project.transcriptions.count()
					project.unexported_transcriptions = project.transcriptions.count()
					project.save()

				else:
					print('Project {}:{} not found in data root.'.format(client_name, project_name))

			else:
				print('Client {} not found in data root.'.format(client_name))
		else:
			for client_name in [f for f in os.listdir(root) if '.DS' not in f]:
				client = None
				if Client.objects.filter(name=client_name).count():
					client = Client.objects.get(name=client_name)

				print('Client: {}'.format(client_name))
				count = 0
				new_projects = [f for f in os.listdir(join(root, client_name)) if isdir(join(root, client_name, f))]
				for project_name in new_projects:
					if (client is not None and not client.projects.filter(name=project_name).count()) or client is None:
						count += 1
						print('-- Project: {}'.format(project_name))

				if not count:
					print('-- No new projects')
