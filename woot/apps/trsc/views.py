#woot.apps.trsc.views

#django
from django.views.generic import View
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

#local
from apps.users.models import User
from apps.dstr.models import Project, Job
from apps.trsc.models import Transcription, Revision

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
      words = json.dumps([word.content for word in job.project.words.filter(Q(char__contains=' ') | Q(tag=True))])

      #render
      return render(request, 'transcription/transcription.html', {'transcriptions':transcriptions,'words':words,'job_id':job.id_token,})
    else:
      return HttpResponseRedirect('/start/')

#methods
def create_new_job(request):
  if request.method == 'GET':
    user = request.user
    if user.is_authenticated():
      #get user object
      user = User.objects.get(email=user)

      #if there are available jobs
      if Job.objects.filter(is_available=True).count()>0:
        job = Job.objects.filter(is_available=True)[0]
        job.is_available = False
        user.jobs.add(job)
        job.save()
        return HttpResponseRedirect('/transcription/' + str(job.id_token))
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
    revision, created = transcription.revisions.get_or_create(user=User.objects.get(email=request.user),
                                                              job=Job.objects.get(id_token=request.POST['job_id']))

    if created:
      revision.id_token = generate_id_token(Revision)

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
    if client.words.filter(project=transcription.project, char=word).count()==0 and not (('[' in word and ']' not in word) or (']' in word and '[' not in word)):
      client.words.create(project=transcription.project, grammar=transcription.grammar, char=word, tag=(('[' in word and ']' in word)))

    return HttpResponse('')

class LoginView(View):
  def get(self, request):
    if request.user.is_authenticated():
      return HttpResponseRedirect('/start/')
    else:
      return render(request, 'trsc/login.html', {})

  def post(self, request):
    form = LoginForm(request.POST)

    if form.is_valid():
      user = authenticate(email=request.POST['email'], password=request.POST['password'])
      if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect('/start/')
      else:
        return render(request, 'trsc/login.html', {'invalid_username_or_password':True})
    else:
      return render(request, 'trsc/login.html', {'bad_formatting':True})

class StartView(View):
  def get(self, request):
    user = request.user
    if user.is_authenticated():
      #get user object
      user = User.objects.get(email=user)

      #list of jobs
      active_jobs = user.jobs.filter(is_active=True)

      #total remaining transcriptions
      remaining_transcriptions = Transcription.objects.filter(is_active=True).count()
      transcriptions_done_by_user = len(np.unique([revision.transcription.pk for revision in user.revisions.all()]))

      return render(request, 'trsc/start.html', {'user':user,
                                                 'active_jobs':active_jobs,
                                                 'remaining_transcriptions':remaining_transcriptions,
                                                 'transcriptions_done_by_user':transcriptions_done_by_user,})
    else:
      return HttpResponseRedirect('/login/')

class FAQView(View):
  def get(self, request):
    return render(request, 'trsc/faq.html')

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/login/')
