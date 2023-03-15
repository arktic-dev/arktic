#woot.apps.pages.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.conf import settings

#local
from woot.apps.pages.forms import LoginForm
from woot.apps.users.models import User
from woot.apps.transcription.models import Transcription
from woot.apps.distribution.models import Client

#util
import os
from os.path import join

#classes
class LoginView(View):
	def get(self, request):
		if request.user.is_authenticated:
			return HttpResponseRedirect('/start/')
		else:
			return render(request, 'pages/login.html', {})

	def post(self, request):
		form = LoginForm(request.POST)

		if form.is_valid():
			user = authenticate(email=request.POST['email'], password=request.POST['password'])
			if user is not None and user.is_active:
				login(request, user)
				return HttpResponseRedirect('/start/')
			else:
				return render(request, 'pages/login.html', {'invalid_username_or_password':True})
		else:
			return render(request, 'pages/login.html', {'bad_formatting':True})

class StartView(View):
	def get(self, request):
		user = request.user
		if user.is_authenticated:
			#get user object
			user = User.objects.get(email=user)

			#list of jobs
			active_jobs = user.jobs.filter(is_active=True)

			#total remaining transcriptions
			remaining_transcriptions = Transcription.objects.filter(is_available=True, client__is_demo=user.is_demo).count()

			return render(request, 'pages/start.html', {'user':user,
																									'active_jobs':active_jobs,
																									'remaining_transcriptions':remaining_transcriptions,})
		else:
			return HttpResponseRedirect('/login/')

class FAQView(View):
	def get(self, request, client_name):
		# default faq
		default_faq = ''
		with open(join(settings.SITE_ROOT, 'default_faq.md')) as df:
			default_faq = df.read()

		if client_name=='default':
			return render(request, 'pages/faq.html', {'default_faq':default_faq})
		else:
			client = Client.objects.get(name=client_name)
			return render(request, 'pages/faq.html', {'client':client, 'default_faq':default_faq})

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login/')
