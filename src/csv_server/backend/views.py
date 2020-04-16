from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView

class PdfUploadView(viewsets.ViewSet):
    pass

def download_csv(request):
    print()
