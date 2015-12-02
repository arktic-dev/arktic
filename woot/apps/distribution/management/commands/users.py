# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.users.models import User
from apps.transcription.models import Transcription, Revision

# util
import os
import json
import time
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
			help='Name of the experiment to import' # who cares
		),

		make_option('--project', # option that will appear in cmd
			action='store', # no idea
			dest='project', # refer to this in options variable
			default='', # some default
			help='Name of the series' # who cares
		),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):

		client_name = options['client']
		project_name = options['project']

		print('User details ---')
		print('{} {}'.format(User.objects.count(), 'user' if User.objects.count()==1 else 'users'))
		for user in User.objects.all():
			print('---')
			# email
			print('Email: {}'.format(user.email))
			print('		Total revisions: {}'.format(user.completed_revisions))
			print('		Total audio time: {}'.format(user.total_audio_time))
			print('')
		print('')

		if client_name!='':
			if project_name!='':
				# for each client, print details
				print('Client details ---')
				client = Client.objects.get(name=client_name)
				print('---')
				print('Name: {}'.format(client.name))
				# total transcriptions
				# total transcription time
				print('Total transcriptions: {} ({})'.format(client.total_transcriptions, client.total_audio_time))
				# active transcriptions
				print('Active transcriptions: {}'.format(client.active_transcriptions))
				print('')
				# total projects
				print('{} {}'.format(client.projects.count(), 'project' if client.projects.count()==1 else 'projects'))

				project = client.projects.get(name=project_name)
				print('	---')
				print('	Name: {}'.format(project.name))
				# total transcriptions
				print('	Total transcriptions: {} ({})'.format(project.total_transcriptions, project.total_audio_time))
				# active transcriptions
				print('	Active transcriptions: {}'.format(project.active_transcriptions))

				# users that have worked on this project
				unique_users = list(set([job.user.email for job in project.jobs.all()]))
				print('	Users: {}'.format(', '.join(unique_users)))

				for email in unique_users:
					print('		---')
					# total transcriptions
					user = User.objects.get(email=email)

					print('		Email: {}'.format(user.email))
					print('		Total revisions: {}'.format(user.completed_revisions))
					print('		Total audio time: {}'.format(user.total_audio_time))
					print('')
			else:

				# for each client, print details
				print('Client details ---')
				client = Client.objects.get(name=client_name)
				print('---')
				print('Name: {}'.format(client.name))
				# total transcriptions
				# total transcription time
				print('Total transcriptions: {} ({})'.format(client.transcriptions.count(), total_transcription_time))
				# active transcriptions
				print('Active transcriptions: {}'.format(client.transcriptions.filter(is_active=True).count()))
				print('')
				# total projects
				print('{} {}'.format(client.projects.count(), 'project' if client.projects.count()==1 else 'projects'))

				for project in client.projects.order_by('date_created'):
					print('	---')
					print('	Name: {}'.format(project.name))
					# total transcriptions
					print('	Total transcriptions: {} ({})'.format(project.total_transcriptions, project.total_audio_time))
					# active transcriptions
					print('	Active transcriptions: {}'.format(project.active_transcriptions))

					# users that have worked on this project
					unique_users = list(set([job.user.email for job in project.jobs.all()]))
					print('	Users: {}'.format(', '.join(unique_users)))

					for email in unique_users:
						print('		---')
						user = User.objects.get(email=email)

						print('		Email: {}'.format(user.email))
						print('		Total revisions: {}'.format(user.completed_revisions))
						print('		Total audio time: {}'.format(user.total_audio_time))
						print('')
					print('')

		else:
			if project_name!='':
				print('Ignoring project {}. Please enter client first.'.format(project))

			else:
				print('You can also enter a client and a project using --client=<client> --project=<project>')

				# for each client, print details
				print('Client details ---')
				print('{} {}'.format(Client.objects.count(), 'client' if Client.objects.count()==1 else 'clients'))
				for client in Client.objects.all():
					print('---')
					print('Name: {}'.format(client.name))
					# total transcriptions
					# total transcription time
					print('Total transcriptions: {} ({})'.format(client.total_transcriptions, client.total_audio_time))
					# active transcriptions
					print('Active transcriptions: {}'.format(client.active_transcriptions))
					print('')
					# total projects
					print('{} {}'.format(client.projects.count(), 'project' if client.projects.count()==1 else 'projects'))

					for project in client.projects.order_by('date_created'):
						print('	---')
						print('	Name: {}'.format(project.name))
						# total transcriptions
						print('	Total transcriptions: {} ({})'.format(project.total_transcriptions, project.total_audio_time))
						# active transcriptions
						print('	Active transcriptions: {}'.format(project.active_transcriptions))

						# users that have worked on this project
						unique_users = list(set([job.user.email for job in project.jobs.all()]))
						print('	Users: {}'.format(', '.join(unique_users)))

						for email in unique_users:
							print('		---')
							user = User.objects.get(email=email)
							print('		Email: {}'.format(user.email))
							print('		Total revisions: {}'.format(user.completed_revisions))
							print('		Total audio time: {}'.format(user.total_audio_time))
							print('')
						print('')
					print('')
