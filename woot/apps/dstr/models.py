# woot.apps.dstr.models

# django
from django.db import models

# local
from apps.users.models import User
from apps.dstr.util import generate_id_token

# util


### Models
class Client(models.Model):
  # connections

  # properties
  name = models.CharField(max_length=255)

  # methods
  def __str__(self):
    return '{}'.format(self.name)

class Project(models.Model):
  # connections
  client = models.ForeignKey(Client, related_name='projects')

  # properties
  id_token = models.CharField(max_length=8)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  project_path = models.TextField(max_length=255)
  completed_project_file = models.FileField(upload_to='completed_projects', null=True)

  # methods
  def __str__(self):
    return '{}: {}'.format(self.client.name, self.name)

class Job(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='jobs', null=True)
  project = models.ForeignKey(Project, related_name='jobs', null=True)
  user = models.ForeignKey(User, related_name='jobs', null=True)

  #properties
  is_active = models.BooleanField(default=True)
  is_available = models.BooleanField(default=True)
  id_token = models.CharField(max_length=8) #a random string of characters to identify the job
  active_transcriptions = models.IntegerField(editable=False, default=0)
  date_created = models.DateTimeField(auto_now_add=True)
  date_completed = models.DateTimeField(auto_now_add=False, null=True)
  total_transcription_time = models.DecimalField(max_digits=8, decimal_places=5, null=True)
  time_taken = models.DecimalField(max_digits=8, decimal_places=6, null=True)

  # methods
  def __str__(self):
    return str(self.project) + ' > ' + str(self.user) + ', job ' + str(self.pk) + ':' + str(self.id_token)
