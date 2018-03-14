from django.conf.urls import url, include
from bookworm import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<book_id>[\w\-]+)/$', views.book_page, name='book_page'),
	url(r'^accounts/', include('registration.backends.simple.urls')),
]

