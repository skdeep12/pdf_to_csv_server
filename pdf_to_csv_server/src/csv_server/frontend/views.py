
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.urls import include, path
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
import os
from django.views.generic.edit import CreateView

from .forms import UploadForm
from .pdf_to_csv import convert_pdf_to_csv

class Home(TemplateView):
    template_name = 'root.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            print(cd)
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            query_response = convert_pdf_to_csv(uploaded_file.name, cd['query_variable'], str(cd['query_year']))
            context.update(query_response)
            return render(request, 'upload_success.html', context)
        else:
            context['error'] = form.errors
    return render(request, 'upload.html', context)


def download(request):
    context = {}
    return render(request, 'download.html', context)