# apps.distribution.command: export

# django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

### Command
class Command(BaseCommand):

	args = ''
	help = ''

	def handle(self, *args, **options):
		# display all paths
		print('ACCESS_ROOT: {}'.format(settings.ACCESS_ROOT))
		print('DATA_ROOT: {}'.format(settings.DATA_ROOT))
		print('DJANGO_ROOT: {}'.format(settings.DJANGO_ROOT))
		print('SITE_ROOT: {}'.format(settings.SITE_ROOT))
		print('SITE_NAME: {}'.format(settings.SITE_NAME))
