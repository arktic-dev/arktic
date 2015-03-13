#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.distribution.models import Job
from apps.transcription.models import Transcription

# util
import numpy as np

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    # get avilable jobs
    available_jobs = Job.objects.filter(is_available=True)

    # get transcription set
    available_transcription_set = Transcription.objects.filter(job__is_available=True)

    # delete available jobs
    # available_jobs.delete()

    # separate transcriptions into yes, no and other
    other = available_transcription_set.exclude(utterance__contains='yes').exclude(utterance__contains='no')
    yes = available_transcription_set.filter(utterance__contains='yes')
    no = available_transcription_set.filter(utterance__contains='no')

    # conflicts
    intersection = np.intersect1d([t.pk for t in yes], [t.pk for t in no])
    print(intersection)
