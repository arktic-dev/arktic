# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.distribution.util import generate_id_token, process_audio

# util
import os
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
      help='Name of client' # who cares
    ),

    make_option('--project', # option that will appear in cmd
      action='store', # no idea
      dest='project', # refer to this in options variable
      default='', # some default
      help='Name of project' # who cares
    ),

    make_option('--completed', # option that will appear in cmd
      action='store_true', # no idea
      dest='completed', # refer to this in options variable
      default='', # some default
      help='Name of project' # who cares
    ),

  )

  args = ''
  help = ''

  def handle(self, *args, **options):
    root = settings.DATA_ROOT
    client_name = options['client']
    project_name = options['project']

    if client_name!='':
      pass
    else:
      print('Listing clients and projects in order of age. Add "--completed" flag to exclude active projects.')
      for client in Client.objects.all():
        print('client {}'.format(client.name))
        for project in client.projects.all():
          print('client {}, project {}, {}/{} completed transcriptions'.format(client.name, project.name, project.transcriptions.filter(is_active=True).count(), project.transcriptions.count()))
