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
    yes_wo_no = yes.exclude(utterance__contains='no')
    no_wo_yes = no.exclude(utterance__contains='yes')

    yes_no = available_transcription_set.filter(utterance__contains='no').filter(utterance__contains='yes')

    # list of pk
    pk_list = [t.pk for t in other] + [t.pk for t in yes_wo_no] + [t.pk for t in no_wo_yes] + [t.pk for t in yes_no]

    for pk in pk_list:
      print([pk, Transcription.objects.get(pk=pk).utterance])
