#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.distribution.models import Job, Project
from apps.transcription.models import Transcription

# util
import numpy as np

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):

    for p in Project.objects.all():
      # get transcription set
      available_transcription_set = p.transcriptions.exclude(job__pk__gt=0)

      # separate transcriptions into yes, no and other

      other = available_transcription_set.exclude(utterance__contains='yes ').exclude(utterance__contains='yeah ').exclude(utterance__contains='no ').exclude(utterance__contains='nope ')
      yes = available_transcription_set.filter(utterance__contains='yes ').filter(utterance__contains='yeah ')
      no = available_transcription_set.filter(utterance__contains='no ').filter(utterance__contains='nope ')

      # conflicts
      yes_wo_no = yes.exclude(utterance__contains='no ').exclude(utterance__contains='nope ')
      no_wo_yes = no.exclude(utterance__contains='yes ').exclude(utterance__contains='yeah ')

      yes_no = available_transcription_set.filter(utterance__contains='no ').filter(utterance__contains='nope ').filter(utterance__contains='yes ').filter(utterance__contains='yeah ')

      # list of pk
      pk_list = [t.pk for t in yes_wo_no] + [t.pk for t in no_wo_yes] + [t.pk for t in yes_no]

      other_set = p.transcriptions.filter(pk__in=[t.pk for t in other]).order_by('utterance')
      yes_no_set = p.transcriptions.filter(pk__in=pk_list)

      total_pk = [t.pk for t in other_set] + [t.pk for t in yes_no_set]

      print('creating jobs...')
      counter = len(total_pk) - 1 if len(total_pk) else 0
      while counter:
        print('available: %d'%(counter), end='\r')
        job = self.jobs.create(client=self.client, id_token=generate_id_token(Job))
        lower_bound = counter-settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB if counter>=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB else 0
        job_set = total_pk[lower_bound:counter]
        job_t_set = Transcription.objects.filter(pk__in=job_set)
        job.get_transcription_set(job_t_set)
        job.save()
        counter = lower_bound
