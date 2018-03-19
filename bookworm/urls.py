from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from registration.backends.simple.views import RegistrationView
from bookworm import views

#Redirects from the default page to the index page instead.
class MyRegistrationView(RegistrationView):
	def get_success_url(self, user):
		return '/index/'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^home/$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^book/(?P<book_id>[\w\-]+)/$', views.book_page, name='book_page'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profile_edit/(?P<username>[\w\-]+)/$', views.profile_edit, name='profile_edit'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

