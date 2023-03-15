#apps.transcription.urls

#django
from django.contrib import admin
from django.urls import include, path, re_path

#local
from woot.apps.transcription.views import start_redirect, TranscriptionView, create_new_job, update_revision, add_word, delete_word

#third party

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = [
	path('', start_redirect),
	re_path('(?P<job_id_token>[A-Z0-9]{8})', TranscriptionView.as_view()),
	path('new/', create_new_job),
	path('revision/', update_revision),
	path('add/', add_word),
	path('delete/', delete_word),
]
