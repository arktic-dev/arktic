#woot.apps.transcription.views

#django
from django.views.generic import View
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Max, Min

#local
from apps.users.models import User
from apps.distribution.models import Project, Job
from apps.transcription.models import Transcription, Revision
from apps.distribution.util import generate_id_token

#util
import random
import json

#class views
class TranscriptionView(View):
	def get(self, request, job_id_token):
		user = request.user
		if user.is_authenticated():
			user = User.objects.get(email=user)

			job = get_object_or_404(user.jobs, id_token=job_id_token) #does this do 'return HTTP... blah'?

			#transcriptions
			transcriptions = job.transcriptions.all()
			for transcription in transcriptions:
				transcription.set_latest_revision_done_by_current_user(user)
				transcription.update()

			#words
			words = json.dumps([word.content for word in job.project.words.filter(Q(content__contains=' ') | Q(tag=True))])

			#render
			return render(request, 'transcription/transcription.html', {'transcriptions':transcriptions,'words':words,'job_id':job.id_token,'client':transcription.client})
		else:
			return HttpResponseRedirect('/start/')

#methods
def create_new_job(request):
	if request.method == 'GET':
		user = request.user
		if user.is_authenticated():
			#get user object
			user = User.objects.get(email=user)

			#if there are available transcriptions
			if Transcription.objects.filter(is_available=True).count()>0:

				# 1. sort projects by age (newest first), and get a set of transcriptions if they exist
				project = None
				for P in Project.objects.all().order_by('date_created'):
					if P.transcriptions.filter(is_available=True).count()>0 and project is None:
						if user.is_demo:
							project = P if P.client.is_demo else None
						else:
							project = P

				if project is not None:
					job_transcription_set = project.transcriptions.filter(is_available=True).order_by('utterance')
					if job_transcription_set.count()!=0:
						job = project.jobs.create(client=project.client, user=user)
						job.is_available = False
						job.id_token = generate_id_token('distribution','Job')
						job_transcription_set = job_transcription_set[:settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB] if len(job_transcription_set)>=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB else job_transcription_set
						job.get_transcription_set(job_transcription_set)
						job.save()

						return HttpResponseRedirect('/transcription/' + str(job.id_token))

					else:
						return HttpResponseRedirect('/start/')

				else:
					return HttpResponseRedirect('/start/')

			else:
				return HttpResponseRedirect('/start/')

		else:
			return HttpResponseRedirect('/login/')

def start_redirect(request):
	return HttpResponseRedirect('/start/')

def update_revision(request):
	if request.user.is_authenticated:
		#get user and update revision utterance
		transcription = Transcription.objects.get(id_token=request.POST['transcription_id'])
		revision, created = transcription.revisions.get_or_create(client=transcription.client,
																															project=transcription.project,
																															user=User.objects.get(email=request.user),
																															job=Job.objects.get(id_token=request.POST['job_id']))

		if created:
			revision.id_token = generate_id_token('transcription', 'Revision')

		#split utterance
		revision.utterance = request.POST['utterance']
		revision.save()

		#processing
		revision.process_words()
		revision.job.update()

		return HttpResponse('')

def add_word(request):
	if request.user.is_authenticated:
		#get POST vars
		transcription_id = request.POST['transcription_id']
		word = request.POST['word']

		#vars
		transcription = Transcription.objects.get(id_token=transcription_id)
		client = transcription.client
		if client.words.filter(project=transcription.project, content=word).count()==0 and not (('[' in word and ']' not in word) or (']' in word and '[' not in word)):
			client.words.create(project=transcription.project, content=word, tag=(('[' in word and ']' in word)))

		return HttpResponse('')

'''

http://stackoverflow.com/a/2257449/2127199
http://stackoverflow.com/a/23728630/2213647

This Stack Overflow quesion is the current top Google result for "random string Python". The current top answer is:

''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

This is an excellent method, but the PRNG in random is not cryptographically secure.
I assume many people researching this question will want to generate random strings for encryption or passwords.
You can do this securely by making a small change in the above code:

''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(n))

Using random.SystemRandom() instead of just random uses /dev/urandom on *nix machines and CryptGenRandom() in Windows.
These are cryptographically secure PRNGs. Using random.choice instead of random.SystemRandom().choice in an application
that requires a secure PRNG could be potentially devastating, and given the popularity of this question,
I bet that mistake has been made many times already.

'''
