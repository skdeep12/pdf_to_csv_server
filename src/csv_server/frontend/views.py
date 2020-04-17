
import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.generic import TemplateView

from .forms import UploadForm, QueryForm
from .pdf_to_csv import BrowserProcessor
from .models import LineItem, Finances, Company

from django.core.exceptions import ObjectDoesNotExist


class Home(TemplateView):
    template_name = 'root.html'


def upload(request):
    context = {}
    if request.method == 'POST':
        form = UploadForm(request.POST,request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            query_response, errors = \
                BrowserProcessor.process_pdf_to_csv_request(uploaded_file.name,
                                                            cd['query_variable'].strip(),
                                                            str(cd['query_year']).strip())
            if errors is not None:
                context['error'] = 'The Combination of ' + \
                                   cd['query_variable'] + ' and ' + str(cd['query_year']) + ' is not valid'
            context.update(query_response)
            return render(request, 'upload_success.html', context)
        else:
            context['error'] = form.errors
    return render(request, 'upload.html', context)


def download(request, filename):
    file_path = os.path.join(settings.MEDIA_ROOT, filename)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="text/csv")
            response['Content-Disposition'] = 'inline; filename=' + 'BalSheet.csv'
            return response
    raise Http404


def query(request):
    context = {}
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                company = Company.objects.get(name=cd['company_name'].strip())
                line_item = LineItem.objects.get(name=cd['query_variable'].strip(),
                                                 company_id=company)
                concrete_line_item = Finances.objects.get(year=str(cd['query_year']).strip(), line_item_id=line_item)
                context['company_name'] = cd['company_name']
                context['attribute'] = cd['query_variable']
                context['year'] = cd['query_year']
                context['attribute_value'] = concrete_line_item.amount
            except ObjectDoesNotExist as e:
                context['error'] = "Queried data is not present in the database"
            return render(request, 'query_success.html', context)
        else:
            context['error'] = form.errors
    return render(request, 'query.html', context)