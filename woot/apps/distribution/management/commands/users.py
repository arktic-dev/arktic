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

# var
spacer = ' '*10

### Command
class Command(BaseCommand):

  args = ''
  help = ''

  def handle(self, *args, **options):
    # for each user, print details
    print('User details ---')
    print('{} {}'.format(User.objects.count(), 'user' if User.objects.count()==1 else 'users'))
    for user in User.objects.all():
      print('---')
      # email
      print('Email: {}'.format(user.email))

      # total transcriptions
      unique_transcriptions = list(set([r.transcription.pk for r in user.revisions.all()]))
      unique_completed_transcriptions = len(unique_transcriptions)
      # total transcription time
      total_transcription_time = time.strftime('%H:%M:%S', time.gmtime(sum([Transcription.objects.get(pk=pk).audio_time for pk in unique_transcriptions])))

      print('Completed transcriptions: {} ({})'.format(unique_completed_transcriptions, total_transcription_time))

    print('')

    # for each client, print details
    print('Client details ---')
    print('{} {}'.format(Client.objects.count(), 'client' if Client.objects.count()==1 else 'clients'))
    for client in Client.objects.all():
      print('---')
      print('Name: {}'.format(client.name))
      # total transcriptions
      # total transcription time
      total_transcription_time = time.strftime('%H:%M:%S', time.gmtime(sum([t.audio_time for t in client.transcriptions.all()])))
      print('Total transcriptions: {} ({})'.format(client.transcriptions.count(), total_transcription_time))
      # active transcriptions
      print('Active transcriptions: {}'.format(client.transcriptions.filter(is_active=True).count()))
      print('')
      # total projects
      print('{} {}'.format(client.projects.count(), 'project' if client.projects.count()==1 else 'projects'))

      for project in client.projects.order_by('date_created'):
        print('  ---')
        print('  Name: {}'.format(project.name))
        # total transcriptions
        total_transcription_time = time.strftime('%H:%M:%S', time.gmtime(sum([t.audio_time for t in project.transcriptions.all()])))
        print('  Total transcriptions: {} ({})'.format(project.transcriptions.count(), total_transcription_time))
        # active transcriptions
        print('  Active transcriptions: {}'.format(project.transcriptions.filter(is_active=True).count()))

        # users that have worked on this project
        unique_users = list(set([job.user.email for job in project.jobs.all()]))
        print('  Users: {}'.format(', '.join(unique_users)))

        for email in unique_users:
          print('    ---')
          # email
          print('    Email: {}'.format(email))

          # total transcriptions
          user = User.objects.get(email=email)
          unique_transcriptions = list(set([r.transcription.pk for r in user.revisions.filter(job__project=project)]))
          unique_completed_transcriptions = len(unique_transcriptions)
          # total transcription time
          total_transcription_time = time.strftime('%H:%M:%S', time.gmtime(sum([Transcription.objects.get(pk=pk).audio_time for pk in unique_transcriptions])))

          print('    Completed transcriptions: {} ({})'.format(unique_completed_transcriptions, total_transcription_time))
          print('')
        print('')
      print('')
