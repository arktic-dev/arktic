# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from apps.distribution.models import Client
from apps.transcription.models import Revision
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
    client_root = os.path.join(root, client_name)
    project_name = options['project']

    if client_name!='':
      client = Client.objects.get(name=client_name)

      if project_name!='':
        print('Exporting project {} from client {}...'.format(project_name, client_name))
        project = client.projects.get(name=project_name)

        number_of_transcriptions = project.transcriptions.count()
        revisions = Revision.objects.filter(transcription__project=project)

        # with open(os.path.join(client_root, '{}.csv'.format(project.name)), 'w+') as csv_file:
        for i, revision in enumerate(revisions):
          # print('Exporting {}/{}...     '.format(i+1, revisions.count()), end='\r' if i+1<revisions.count() else '\n')
          # csv_file.write('{},{},{}\n'.format(i, revision.transcription.audio_file.name, revision.utterance))
          print('{},{},{}'.format(i, os.path.basename(revision.transcription.audio_file.name), revision.utterance))

      else:
        print('Exporting all projects from client {}'.format(client_name))
        for project in client.projects.all():
          number_of_transcriptions = project.transcriptions.count()
          revisions = Revision.objects.filter(transcription__project=project)
          for i, revision in enumerate(revisions):
            print('Exporting {} {}/{}...     '.format(project.name, i+1, revisions.count()), end='\r' if i+1<revisions.count() else '\n')

    else:
      print('Listing clients and projects in order of age. Add "--completed" flag to exclude active projects.')
      print('Nothing will be exported.')
      for client in Client.objects.all():
        print('client {}'.format(client.name))
        for project in client.projects.all():
          number_of_revisions = Revision.objects.filter(transcription__project=project).count()
          number_of_transcriptions = project.transcriptions.count()
          if options['completed']:
            if number_of_revisions==number_of_transcriptions:
              print('client {}, project {}, {}/{} completed transcriptions'.format(client.name, project.name, number_of_revisions, number_of_transcriptions))
          else:
            print('client {}, project {}, {}/{} completed transcriptions'.format(client.name, project.name, number_of_revisions, number_of_transcriptions))
