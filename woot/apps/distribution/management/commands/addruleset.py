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
from os.path import join
import json

# var
spacer = ' '*10

### Command
class Command(BaseCommand):

	args = ''
	help = ''

	def handle(self, *args, **options):
		root = settings.DATA_ROOT
