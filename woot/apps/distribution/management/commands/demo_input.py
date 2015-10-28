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
import json

# var
spacer = ' '*10

### Command
class Command(BaseCommand):

  args = ''
  help = ''

  def handle(self, *args, **options):
    root = settings.DATA_ROOT

    # 1. for each client name in root:
    for client_name in [f for f in os.listdir(root) if '.DS' not in f]:

      # 2. get or create client
      client, client_created = Client.objects.get_or_create(name=client_name)
      if client_created:
        client.is_demo=True
        client.save()
      print('client {}... {}{}'.format(client_name, 'already exists.' if not client_created else 'created.', spacer))

      # 3. for each project name in client dir:
      for project_name in [f for f in os.listdir(os.path.join(root, client_name)) if os.path.isdir(os.path.join(root, client_name, f))]:

        # 3. get or create project
        project, project_created = client.projects.get_or_create(name=project_name)
        print('client {}, project {}... {}{}'.format(client_name, project_name, 'already exists.' if not project_created else 'created.', spacer))

        # 4. list all files in the project directory and create transcriptions
        audio_root = os.path.join(root, client_name, project_name)
        audio_files = [f for f in os.listdir(os.path.join(audio_root)) if '.wav' in f]

        for i, audio_file in enumerate(audio_files):
          if project.transcriptions.filter(audio_file='audio/{}'.format(audio_file)).count()==0:
            audio_file_path = os.path.join(audio_root, audio_file)
            (seconds, rms_values) = process_audio(audio_file_path)

            max_rms = max(rms_values)
            rms_values = [float(value)/float(max_rms) for value in rms_values]
            audio_rms = json.dumps(rms_values)

            with open(audio_file_path, 'rb') as open_audio_file:
              transcription, transcription_created = project.transcriptions.get_or_create(client=client,
                                                                                          id_token=generate_id_token('transcription','Transcription'),
                                                                                          audio_time=seconds,
                                                                                          audio_rms=audio_rms,
                                                                                          audio_file=File(open_audio_file),
                                                                                          is_active=True,
                                                                                          is_available=True)

            print('client {}, project {}, file {}... created ({}/{})'.format(client_name, project_name, audio_file, i+1, len(audio_files)), end='\r' if i<len(audio_files)-1 else '\n')

          else:
            print('client {}, project {}, file {}... already exists. ({}/{})'.format(client_name, project_name, audio_file, i+1, len(audio_files)), end='\r' if i<len(audio_files)-1 else '\n')