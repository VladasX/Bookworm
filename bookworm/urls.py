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
	url(r'^faq/$', views.faq, name='faq'),
    url(r'^search/$', views.book_search, name='book_search'),
    url(r'^books/page-(?P<pages>[0-9]+)/$', views.book_list, name='book_list'),
    url(r'^books/page-(?P<pages>[0-9]+)/(?P<sort>[\w\-]+)/$', views.book_list, name='book_list'),
    url(r'^book/(?P<bookid>[\w\-]+)/$', views.book_page, name='book_page'),
    url(r'^book/(?P<bookid>[\w\-]+)/review/$', views.add_review, name='add_review'),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^profile_edit/(?P<username>[\w\-]+)/$', views.profile_edit, name='profile_edit'),
	url(r'^reading_list/(?P<username>[\w\-]+)/$', views.reading_list, name='reading_list'),
    url(r'^ajax/validate_username/$', views.validate_username, name='validate_username'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

