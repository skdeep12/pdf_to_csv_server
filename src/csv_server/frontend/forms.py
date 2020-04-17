from django import forms

import datetime
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class UploadForm(forms.Form):
    query_variable = forms.CharField(max_length=60)
    query_year = forms.IntegerField(validators=[MinValueValidator(1960), max_value_current_year])
    document = forms.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def process(self):
        pass


class QueryForm(forms.Form):
    company_name = forms.CharField(max_length=60)
    query_variable = forms.CharField(max_length=60)
    query_year = forms.IntegerField(validators=[MinValueValidator(1960), max_value_current_year])
