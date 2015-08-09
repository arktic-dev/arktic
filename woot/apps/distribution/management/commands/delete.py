# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client

# util
import os
from os.path import join, exists
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

    # test with: 20150730_1

    if client_name!='' and project_name!='':
      client = Client.objects.get(name=client_name)
      project = client.projects.get(name=project_name)

      # to permanently remove a project from storage:
      # 1. Delete all files in the input directory
      project_path = join(settings.DATA_ROOT, client_name, project_name)
      if exists(project_path):
        print('Removing project folder from input directory: {}'.format(project_path))
        os.rmdir(project_path)
      else:
        print('Project folder already removed from input directory: {}'.format(project_path))

      # 2. Delete all audio files in the database along with the files that they reference
      for transcription in project.transcriptions.all():
        file_url = join(settings.DJANGO_ROOT, transcription.audio_file.url[1:])
        print('Removing file {}...'.format(file_url))
        os.remove(file_url)

    else:
      print('Please enter both a client name and a project name.')
