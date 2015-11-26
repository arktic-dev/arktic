# apps.distribution.command: input

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from apps.users.models import User

# util
import os
from os.path import join, exists
import json

### Command
class Command(BaseCommand):

	args = ''
	help = ''

	def handle(self, *args, **options):
		user_access = join(settings.ACCESS_ROOT, settings.USER_ACCESS)
		with open(user_access) as json_data:
			user_data = json.load(json_data)

			for user in user_data:
				User.objects.create_superuser(user['email'], '1970-1-1', user['pwd'])
