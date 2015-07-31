# woot.apps.trsc.models

# django
from django.db import models

# local
from apps.dstr.models import Client, Project, Job
from apps.users.models import User
from django.core.files import File

# util


### Models
class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  job = models.ManyToManyField(Job, related_name='transcriptions')

  #properties
  id_token = models.CharField(max_length=8)
  audio_file_name = models.CharField(max_length=255)
  audio_file = models.FileField(upload_to='audio')
  audio_time = models.DecimalField(max_digits=8, decimal_places=6, null=True)
  audio_rms = models.TextField()
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  is_available = models.BooleanField(default=False)
  date_last_requested = models.DateTimeField(auto_now_add=False, null=True)

  # latest_revision_done_by_current_user = models.BooleanField(default=False)

  # methods
  def unpack_rms(self):
    return [(int(rms*31+1), 32-int(rms*31+1)) for rms in json.loads(self.audio_rms)]

class Revision(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='revisions')
  user = models.ForeignKey(User, related_name='revisions')
  job = models.ForeignKey(Job, related_name='revisions')

  #properties
  id_token = models.CharField(max_length=8)
  date_created = models.DateTimeField(auto_now_add=True)
  utterance = models.CharField(max_length=255)

  #methods
  def __str__(self):
    return '%s: "%s" modified to "%s" > by %s'%(self.id_token, self.transcription.utterance, self.utterance, self.user)

  #sorting
  class Meta:
    get_latest_by = 'date_created'

class Word(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words')
  project = models.ForeignKey(Project, related_name='words')
  transcription = models.ManyToManyField(Transcription, related_name='words')
  revision = models.ManyToManyField(Revision, related_name='words')

  #properties
  id_token = models.CharField(max_length=8)
  content = models.CharField(max_length=255)
  tag = models.BooleanField(default=False)
