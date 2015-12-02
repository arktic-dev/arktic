# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.transcription.models import Transcription, Revision
from apps.distribution.util import generate_id_token, process_audio, random_string
from apps.users.models import User

# util
import os
from os.path import join, basename, exists
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

		# 2. perform input
		for client_name in [f for f in os.listdir(data_root) if '.DS' not in f and os.path.isdir(os.path.join(data_root, f))]:
			# 2-2. get or create client
			client, client_created = Client.objects.get_or_create(name=client_name)
			print('TEST | client {}... {}{}'.format(client_name, 'already exists.' if not client_created else 'created.', spacer))

			# 2-3. for each project name in client dir:
			for project_name in [f for f in os.listdir(os.path.join(data_root, client_name)) if os.path.isdir(os.path.join(data_root, client_name, f))]:

				# 2-3. get or create project
				project, project_created = client.projects.get_or_create(name=project_name)
				print('TEST | client {}, project {}... {}{}'.format(client_name, project_name, 'already exists.' if not project_created else 'created.', spacer))

				# 2-4. list all files in the project directory and create transcriptions
				audio_root = os.path.join(data_root, client_name, project_name)
				audio_files = [join(d,f) for d,ds,fs in os.walk(audio_root) for f in fs if '.wav' in f] # double list of filenames to single list
				relfile_name = [f for f in os.listdir(audio_root) if '.csv' in f] # return single item

				relfile_dictionary = {}
				if relfile_name:
					relfile_path = os.path.join(data_root, client_name, project_name, relfile_name[0])

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

						print('TEST | client {}, project {}, file {}... created ({}/{})'.format(client_name, project_name, audio_file, i+1, len(audio_files)), end='\r' if i<len(audio_files)-1 else '\n')

					else:
						print('TEST | client {}, project {}, file {}... already exists. ({}/{})'.format(client_name, project_name, audio_file, i+1, len(audio_files)), end='\r' if i<len(audio_files)-1 else '\n')

		# 3. create test user and password
		print('TEST | creating test user...')
		test_user = User.objects.create_user('a@b.com', '1970-1-1', 'testpassword')

		# 4. create one job for each project
		print('TEST | creating jobs...')
		test_client = Client.objects.get(name='test')

		while Transcription.objects.filter(is_available=True).count() > 0:

			# 1. sort projects by age (newest first), and get a set of transcriptions if they exist
			project = None
			for P in test_client.projects.all().order_by('date_created'):
				if P.transcriptions.filter(is_available=True).count()>0 and project is None:
					if test_user.is_demo:
						project = P if P.client.is_demo else None
					else:
						project = P

			if project is not None:
				job_transcription_set = project.transcriptions.filter(is_available=True)
				if job_transcription_set.count()!=0:
					job = project.jobs.create(client=project.client, user=test_user)
					job.is_available = False
					job.id_token = generate_id_token('distribution','Job')
					job_transcription_set = job_transcription_set[:settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB] if len(job_transcription_set)>=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB else job_transcription_set
					job.get_transcription_set(job_transcription_set)
					job.save()

		# 5. add revisions with utterances
		for job in test_user.jobs.all():
			print('TEST | creating revisions and utterances for {}/{}'.format(job.pk, test_user.jobs.count()))
			for transcription in job.transcriptions.all():
				revision = transcription.revisions.create(client=test_client, project=job.project, user=test_user, job=job, id_token=generate_id_token('transcription', 'Revision'), utterance=random_string())
				revision.process_words()
				job.update()

		# 6. export projects
		print('TEST | exporting projects...')
		for project in test_client.projects.all():
			project.export(join(data_root, test_client.name), users_flag=project.name=='with_relfile')

		# 7. delete database objects but leave original files
		print('TEST | deleting database objects...')
		for project in test_client.projects.all():
			# to permanently remove a project from storage:
			# - Delete all audio files in the database along with the files that they reference
			for transcription in project.transcriptions.all():
				file_url = join(settings.DJANGO_ROOT, transcription.audio_file.url[1:])
				if exists(file_url):
					print('Removing file {}...'.format(file_url))
					os.remove(file_url)

				media_file_url = join(settings.DJANGO_ROOT, 'audio', transcription.audio_file.url[1:])
				if exists(media_file_url):
					print('Removing media file {}...'.format(media_file_url))
					os.remove(media_file_url)

				transcription.delete()

			project.delete()

		# delete client
		print('TEST | deleting client...')
		test_client.delete()

		# delete user
		print('TEST | deleting user...')
		test_user.delete()

		print('TEST | done.')
