# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File

# local
from woot.apps.transcription.models import Revision

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

		make_option('--fragment', # option that will appear in cmd
			action='store', # no idea
			dest='fragment', # refer to this in options variable
			default='', # some default
		),

	)

	args = ''
	help = ''

	def handle(self, *args, **options):
		fragment = options['fragment']

		if fragment:
			matching_revisions = Revision.objects.filter(utterance__contains=fragment)

			print('Fragment: {}'.format(fragment))
			print('{} match{}'.format(matching_revisions.count(), 'es' if matching_revisions.count()!=1 else ''))
			for revision in matching_revisions:
				print('{}\t>>> {}\t>>> {}\t>>> {}\t>>> {}'.format(revision.pk, revision.user, revision.utterance, revision.transcription.utterance, os.path.basename(revision.transcription.audio_file.url)))

			print('Fragment: {}'.format(fragment))
			print('{} match{}'.format(matching_revisions.count(), 'es' if matching_revisions.count()!=1 else ''))
