#apps.transcription.models

#django
from django.db import models
from django.core.files import File
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

#local
from woot.apps.distribution.models import Client, Project, Job
from woot.apps.users.models import User
from woot.libs.utils import generate_id_token, process_audio

#util
import os
from os.path import basename
from datetime import datetime as dt
import json

#vars

#classes
class Transcription(models.Model):
	#connections
	client = models.ForeignKey(Client, related_name='transcriptions')
	project = models.ForeignKey(Project, related_name='transcriptions')
	job = models.ManyToManyField(Job, related_name='transcriptions')

	#properties
	id_token = models.CharField(max_length=8)
	audio_file_name = models.CharField(max_length=255) #temporary
	audio_file = models.FileField(upload_to='audio')
	audio_time = models.DecimalField(max_digits=8, decimal_places=6, null=True)
	audio_rms = models.TextField()
	utterance = models.CharField(max_length=255)
	requests = models.IntegerField(default=0) #number of times the transcription has been requested.
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=False)
	is_available = models.BooleanField(default=False)
	has_been_exported = models.BooleanField(default=False)
	date_last_requested = models.DateTimeField(auto_now_add=False, null=True)
	latest_revision_done_by_current_user = models.BooleanField(default=False)

	#methods
	def __str__(self):
		return '%s > %s > %d:%s > "%s"'%(self.client.name, self.project.name, self.pk, self.id_token, self.utterance)

	def line(self):
		path = self.audio_file_data_path
		# path = './' + path[path.index('2014'):]
		if self.revisions.count():
			return '%s|%s\n' % (os.path.basename(self.audio_file.file.url), self.revisions.latest().utterance)
		else:
			return ''

	def grammar_name(self):
		return 'grammar'

	def latest_revision_words(self):
		try:
			latest_revision = self.revisions.latest()
			return latest_revision.split_utterance()
		except ObjectDoesNotExist:
			return []

	def update(self):
		#if deactivation condition is satisfied, deactivate transcription
		self.is_active = not self.deactivation_condition()
		if not self.is_active:
			self.client.active_transcriptions -= 1
			self.client.save()
		self.save()

	def audio_file_basename(self):
		return basename(self.audio_file_name)

	def deactivation_condition(self):
		''' Has at least one revision with an utterance'''
		return (self.revisions.exclude(utterance='').count()>0)

	def set_latest_revision_done_by_current_user(self, user):
		if self.revisions.count()>0:
			latest_revision = self.revisions.latest()
			self.latest_revision_done_by_current_user = (latest_revision.user.email==user.email and latest_revision.utterance!='')
		else:
			self.latest_revision_done_by_current_user = False
		self.save()

	def unpack_rms(self):
		return [(int(rms*31+1), 32-int(rms*31+1)) for rms in json.loads(self.audio_rms)]

class Revision(models.Model):
	#connections
	client = models.ForeignKey(Client, related_name='revisions')
	project = models.ForeignKey(Project, related_name='revisions')
	transcription = models.ForeignKey(Transcription, related_name='revisions')
	user = models.ForeignKey(User, related_name='revisions')
	job = models.ForeignKey(Job, related_name='revisions')

	#properties
	id_token = models.CharField(max_length=8)
	date_created = models.DateTimeField(auto_now_add=True)
	utterance = models.CharField(max_length=255)

	''' need to be determined by action_sequence() '''
	time_to_complete = models.DecimalField(max_digits=8, decimal_places=6, null=True)
	number_of_plays = models.IntegerField(default=0)

	#methods
	def __str__(self):
		return '%s: "%s" modified to "%s" > by %s'%(self.id_token, self.transcription.utterance, self.utterance, self.user)

	def split_utterance(self):
		return self.utterance.split(' ')

	def action_sequence(self):
		pass

	def process_words(self):
		words = self.utterance.split()
		for word in words:
			#many to many relationship
			if not (('[' in word and ']' not in word) or (']' in word and '[' not in word)): #reject with only one bracket
				w, created = self.job.project.words.get_or_create(content=word) #unique by char to project
				if created:
					w.client = self.transcription.client
					w.id_token = generate_id_token(Word)
					w.tag = ('[' in word and ']' in word)

				self.words.add(w)
				w.save()

	def process_actions(self):
		for action in self.job.actions.filter(transcription=self.transcription):
			self.actions.add(action)
			action.save()

	#sorting
	class Meta:
		get_latest_by = 'date_created'

class Word(models.Model):
	#connections
	client = models.ForeignKey(Client, related_name='words', null=True)
	project = models.ForeignKey(Project, related_name='words')
	transcription = models.ManyToManyField(Transcription, related_name='words')
	revision = models.ManyToManyField(Revision, related_name='words')

	#properties
	id_token = models.CharField(max_length=8)
	content = models.CharField(max_length=255)
	tag = models.BooleanField(default=False)

	#methods
	def __str__(self):
		return self.content
