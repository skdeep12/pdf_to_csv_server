from django.test import TestCase, SimpleTestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from .pdf_to_csv import BrowserProcessor
from .forms import UploadForm
dir_path = os.path.dirname(os.path.realpath(__file__))


class ConversionTest(TestCase):
    client = Client(enforce_csrf_checks=True,HTTP_USER_AGENT='Mozilla/5.0')

    def setUp(self) -> None:
        BrowserProcessor.process_pdf_to_csv_request(dir_path + "/test_data/BalSheet.pdf")

    @staticmethod
    def test_upload_form_with_invalid_file_extensions():
        my_file = open(dir_path + '/tests.py', 'rb')
        post_dict = {
            'query_variable': 'something',
            'query_year': '2014',
        }
        file_dict = {
            'document': SimpleUploadedFile(my_file.name, my_file.read())
        }
        form = UploadForm(post_dict, file_dict)
        assert form.is_valid() is False
        print(form.errors)

    @staticmethod
    def test_upload_form_with_valid_file_extensions():
        my_file = open(dir_path + '/test_data/BalSheet.pdf', 'rb')
        post_dict = {
            'query_variable': 'something',
            'query_year': '2014',
        }
        file_dict = {
            'document': SimpleUploadedFile(my_file.name, my_file.read())
        }
        form = UploadForm(post_dict,file_dict)
        assert form.is_valid() is True

    def test_upload_invalid_query_fields(self):
        data = {
            'query_variable': 'Accounting Charges',
            'query_year': '2016',
            'company_name': 'SEUNE COTTONLIFE PVT LTD',
        }
        response = self.client.post('/query/', data=data)
        assert response.status_code == 200

        print(response.context['attribute_value'])
