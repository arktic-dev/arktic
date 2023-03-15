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

		# figure
		fig, ax = plt.subplots(1)

		all_values = []

		# go through users
		for user in User.objects.exclude(email__contains='stj'):
			values = []

			for job in user.jobs.all():

				d1 = job.date_created
				df = datetime.datetime(1970,1,1,tzinfo=d1.tzinfo)

				d = (d1 - df).total_seconds()

				values.append(d)
				all_values.append(d)

			if values != []:
				ax.hist(values, bins=100, alpha=0.5, label=user.email)

		min_time = min(all_values)
		min_dt = datetime.datetime.fromtimestamp(min_time)

		max_time = max(all_values)
		max_dt = datetime.datetime.fromtimestamp(max_time)

		r = range(int(min_time), int(max_time), int((max_time-min_time)/20.0))
		da = [datetime.datetime.fromtimestamp(t) for t in r]
		plt.xticks(r, da)
		fig.autofmt_xdate()
		plt.legend()
		plt.show()
