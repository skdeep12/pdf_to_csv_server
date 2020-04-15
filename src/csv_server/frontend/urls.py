from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import routers
from .views import Home, upload, download
from django.conf import settings

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('upload/', upload, name='upload'),
    path('download/', download, name='download')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)