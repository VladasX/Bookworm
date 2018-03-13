from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    
    # Maps all urls to the bookworm app
    url(r'^', include('bookworm.urls')),
]

