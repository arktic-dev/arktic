# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

# local
from woot.apps.distribution.models import Job
from woot.apps.users.models import User

# util
import time
import datetime
import matplotlib.pyplot as plt

### Command
class Command(BaseCommand):

	args = ''
	help = ''

	def handle(self, *args, **options):
		for user in User.objects.filter(email__contains='eliza'):

			average_ratio = 0

			for job in user.jobs.all():
				if job.date_completed is not None:
					print(job.id_token)
					# print((job.date_completed - job.date_created).total_seconds())
					# print(float(job.total_transcription_time))
					# print('')
					average_ratio += ((job.date_completed - job.date_created).total_seconds() / float(job.total_transcription_time)) / user.jobs.count()

			print('User: {}, average ratio: {}'.format(user.email, average_ratio))
