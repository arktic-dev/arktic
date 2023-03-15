# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from woot.apps.distribution.models import Client, Project
from woot.apps.transcription.models import Transcription
from woot.apps.users.models import User

# util
import os
import time
import json
from os.path import join, basename, exists

# var
spacer = ' '*10

### Command
class Command(BaseCommand):
	args = ''
	help = ''

	def handle(self, *args, **options):
		for client in Client.objects.all():
			print('client {}'.format(client.name))
			client.total_transcriptions = client.transcriptions.count()
			client.total_audio_time = sum([t.audio_time for t in client.transcriptions.all()])
			client.active_transcriptions = client.transcriptions.filter(is_active=True).count()
			client.save()

		for project in Project.objects.all():
			print('project {}'.format(project.name))
			project.total_transcriptions = project.transcriptions.count()
			project.total_audio_time = sum([t.audio_time for t in project.transcriptions.all()])
			project.active_transcriptions = project.transcriptions.filter(is_active=True).count()
			project.unexported_transcriptions = project.transcriptions.filter(has_been_exported=False).count()
			project.save()

		for user in User.objects.all():
			print('user {}'.format(user.email))
			unique_transcriptions = list(set([r.transcription.pk for r in user.revisions.filter()]))
			user.completed_revisions = len(unique_transcriptions)
			user.total_audio_time = sum([Transcription.objects.get(pk=pk).audio_time for pk in unique_transcriptions])
			user.save()
