from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from .views import Home, upload, download

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('upload/', upload, name='upload'),
    url(r'^download/(?P<filename>.*)$', download, name='download')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
