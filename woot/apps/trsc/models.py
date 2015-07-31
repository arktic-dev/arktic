# woot.apps.trsc.models

# django
from django.db import models

# local


# util


### Models
class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  job = models.ManyToManyField(Job, related_name='transcriptions', null=True)

  #properties
  id_token = models.CharField(max_length=8)
  audio_file = models.FileField(upload_to='audio')
  audio_time = models.DecimalField(max_digits=8, decimal_places=6, null=True)
  audio_rms = models.TextField()
  utterance = models.CharField(max_length=255)
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  is_available = models.BooleanField(default=False)
  date_last_requested = models.DateTimeField(auto_now_add=False, null=True)
  latest_revision_done_by_current_user = models.BooleanField(default=False)

class Revision(models.Model):


class Word(models.Model):
