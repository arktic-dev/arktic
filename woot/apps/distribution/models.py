#woot.apps.distribution.models

#django
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models import Count

#local
from apps.users.models import User
from libs.utils import generate_id_token

#util
import os
import zipfile as zp
import shutil as sh
import datetime as dt

#vars

#classes
class Client(models.Model):
	#properties
	name = models.CharField(max_length=255)
	client_path = models.TextField(max_length=255)
	is_demo = models.BooleanField(default=False)
	has_ruleset = models.BooleanField(default=False)
	ruleset = models.FileField(upload_to='rulesets')

	# counts
	total_transcriptions = models.IntegerField(default=0)
	total_audio_time = models.FloatField(default=0.0)
	active_transcriptions = models.IntegerField(default=0)

	#methods
	def __str__(self):
		return self.name

	def update(self):
		'''

		Update is called when a revision is submitted. This will propagate down the chain:
		Client > Project > Grammar > Transcription

		When a relfile is completed, a completed_relfile object will be created from the chosen revisions.
		When a project is completed, a completed_project object will be created. This will be available for
		download from the admin in the form of a zip file.

		'''
		for project in self.projects.filter(is_active=True, is_approved=True):
			project.update()

	def display_ruleset(self):
		if self.ruleset.name:
			self.ruleset.open()
			return self.ruleset.read()
		else:
			return ''

class Project(models.Model):
	#connections
	client = models.ForeignKey(Client, related_name='projects')

	#properties
	id_token = models.CharField(max_length=8)
	name = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=False)
	project_path = models.TextField(max_length=255)
	completed_project_file = models.FileField(upload_to='completed_projects')

	# counts
	total_transcriptions = models.IntegerField(default=0)
	total_audio_time = models.FloatField(default=0.0)
	active_transcriptions = models.IntegerField(default=0)
	unexported_transcriptions = models.IntegerField(default=0)

	#methods
	def __str__(self):
		return str(self.client) + ' > ' + str(self.name)

	def update(self):
		''' Updates project when a revision is submitted. '''
		for job in self.jobs.filter(is_active=True):
			job.update()

		#update status: active, processed
		self.active_transcriptions = self.transcriptions.filter(is_active=True).count()
		self.is_active = self.jobs.filter(is_active=True).count() != 0
		self.save()

	def export(self, root, users_flag=False, number_to_export=-1):
		''' Export prepares all of the individual relfiles to be packaged and be available for download. '''
		print('Exporting project {} from client {}...'.format(self.name, self.client.name))

		# 1. vars
		revisions_to_export = self.revisions.filter(transcription__has_been_exported=False)
		current_date = dt.datetime.now().strftime('%Y-%m-%d-%H-%M')

		total_to_export = len(set([r.transcription.pk for r in revisions_to_export]))
		total_to_export = number_to_export if number_to_export>-1 and total_to_export>number_to_export else total_to_export

		with open(os.path.join(root, '{}_{}_number-{}.csv'.format(self.name, current_date, total_to_export)), 'w+') as csv_file:
			total_exported = 0
			for i, revision in enumerate(revisions_to_export):
				if revision.pk == revision.transcription.revisions.latest().pk and total_exported!=total_to_export: # if is latest revision
					total_exported += 1
					transcription = revision.transcription
					transcription.has_been_exported = True
					transcription.save()
					self.unexported_transcriptions -= 1
					self.save()

					print('Exporting {} {}/{}...		 '.format(i, total_exported, total_to_export), end='\r' if total_exported<total_to_export else '\n')

					csv_file.write('{}|{}'.format(os.path.basename(revision.transcription.audio_file.name), revision.utterance))

					if users_flag:
						csv_file.write('|{}'.format(revision.user.email))

					csv_file.write('\n')

				if total_exported==total_to_export:
					break

	def process_words(self):
		'''
		Wrapper for transcription word processing.
		'''
		print('processing words...')
		count = self.transcriptions.count()
		for i, transcription in enumerate(self.transcriptions.all()):
			print('words %d/%d'%(i+1, count), end='\r' if i<count-1 else '\n')
			transcription.process_words()

	def create_jobs(self):
		'''
		Create all possible jobs from the set of transcriptions.
		'''
		if self.jobs.count()==0:
			print('creating jobs...')
			filter_set = self.transcriptions.filter(is_available=True).order_by('grammar__name').order_by('utterance')
			counter = filter_set.count() - 1 if filter_set.count() else 0
			while counter:
				print('available: %d'%(counter), end='\r')
				job = self.jobs.create(client=self.client, id_token=generate_id_token(Job))
				lower_bound = counter-settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB if counter>=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB else 0
				job_set = filter_set[lower_bound:counter]
				job.get_transcription_set(job_set)
				job.save()
				counter = lower_bound
			print('available: 0')

class Job(models.Model):
	#connections
	client = models.ForeignKey(Client, related_name='jobs', null=True)
	project = models.ForeignKey(Project, related_name='jobs', null=True)
	user = models.ForeignKey(User, related_name='jobs', null=True)

	#properties
	is_active = models.BooleanField(default=True)
	is_available = models.BooleanField(default=True)
	id_token = models.CharField(max_length=8) # a random string of characters to identify the job
	active_transcriptions = models.IntegerField(editable=False, default=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB)
	date_created = models.DateTimeField(auto_now_add=True)
	date_completed = models.DateTimeField(auto_now_add=False, null=True)
	total_transcription_time = models.DecimalField(max_digits=8, decimal_places=5, null=True)
	time_taken = models.DecimalField(max_digits=8, decimal_places=6, null=True)

	#methods
	def __str__(self):
		return str(self.project) + ' > ' + str(self.user) + ', job ' + str(self.pk) + ':' + str(self.id_token)

	def get_transcription_set(self, job_set):
		self.active_transcriptions = len(job_set)

		''' total_transcription_time variable '''

		for transcription in job_set:
			transcription.date_last_requested = timezone.now()
			if not self.client.is_demo:
				transcription.is_available = False
			self.transcriptions.add(transcription)
			transcription.save()

		#set total_transcription_time
		self.total_transcription_time = float(sum([float(t.audio_time) for t in self.transcriptions.all()]))

	def update(self): #not used for export. Just for recording values.
		''' active_transcriptions, time_taken '''

		for transcription in self.transcriptions.all():
			transcription.update()

		self.active_transcriptions = self.transcriptions.filter(is_active=True).count()
		if self.active_transcriptions==0:
			if self.client.is_demo: # this should reset the entire job upon completion
				for transcription in self.transcriptions.filter(is_active=False):
					transcription.revisions.all().delete()
					transcription.is_active = True
					transcription.is_available = True
					transcription.save()
			else:
				self.is_active = False
				self.date_completed = timezone.now()

		time_taken = 0
		for transcription in self.transcriptions.filter(is_active=False):
			#get total time for current user
			for revision in transcription.revisions.filter(user=self.user):
				time_taken += revision.time_to_complete if revision.time_to_complete else 0
		self.time_taken = time_taken

		self.save()
