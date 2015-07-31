# apps.dstr.command: input

# django
from django.core.management.base import BaseCommand, CommandError

# local

# util

### Command
class Command(BaseCommand):
  option_list = BaseCommand.option_list + (

    make_option('--client', # option that will appear in cmd
      action='store', # no idea
      dest='client', # refer to this in options variable
      default='', # some default
      help='Name of the client to import' # who cares
    ),

    make_option('--project', # option that will appear in cmd
      action='store', # no idea
      dest='project', # refer to this in options variable
      default='', # some default
      help='Name of the project' # who cares
    ),

  )

  args = ''
  help = ''

  def handle(self, *args, **options):
    pass
