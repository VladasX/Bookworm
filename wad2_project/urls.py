from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from bookworm import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^search/$', views.search, name='search'),

]

