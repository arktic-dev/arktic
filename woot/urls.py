#woot.urls

#django
from django.contrib import admin
from django.urls import include, path, re_path
from woot.settings.common import MEDIA_ROOT, STATIC_ROOT
from django.views.static import serve

#local
from woot.apps.pages.views import LoginView, StartView, logout_view, FAQView
from woot.apps.transcription.views import create_new_job

#third party

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = [
	# Serving media
	re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT, 'show_indexes': True }),
	re_path('static/(?P<path>.*)', serve, {'document_root': STATIC_ROOT, 'show_indexes': True }),

	#pages
	path('login/', LoginView.as_view()),
	path('logout/', logout_view),
	path('', StartView.as_view()),
	path('start/', StartView.as_view()),
	re_path('faq/(?P<client_name>.+)', FAQView.as_view()),

	#transcription
	path('transcription/', include('woot.apps.transcription.urls')),
	path('new/', create_new_job),

	#admin
	path('admin/', admin.site.urls),
]

#1. make users
#2. make jobs
#3. make transcription url work
#4. make start url work
#5. latest revision words
#6.
