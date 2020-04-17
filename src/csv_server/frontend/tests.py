from django.test import TestCase, SimpleTestCase
from django.conf import settings
# Create your tests here.
import os
from .models import *
from .pdf_to_csv import BrowserProcessor


class ConversionTest(TestCase):
    def setUp(self) -> None:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        BrowserProcessor.process_pdf_to_csv_request(dir_path + "/BalSheet.pdf")
        self.company = Company.objects.get(name='SEUNE COTTONLIFE PVT LTD')
        print(self.company)
        line_items = LineItem.objects.all()
        for item in line_items:
            print(LineItem.objects.filter(id=item.id).values())
        self.line_item = LineItem.objects.get(name='Gross Profit B/D',
                                         company_id=self.company)

    def test_something(self):
        concrete_line_items = Finances.objects.all()
        for item in concrete_line_items:
            print(Finances.objects.filter(id=item.id).values())
        concrete_line_item = Finances.objects.get(year='2015', line_item_id=self.line_item)
        print(concrete_line_item)
