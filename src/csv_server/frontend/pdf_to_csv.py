import random
import string
from os import path

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .PdfProcessor import PdfToCsvProcessor
from .logger import log
from .models import *

from pathlib import Path


class BrowserProcessor:
    csvLocation = Path(settings.MEDIA_ROOT)
    pdfLocation = Path(settings.MEDIA_ROOT)

    @staticmethod
    def process_pdf_to_csv_request(file_name, query_attribute='', query_year=''):
        """
        This function receives a pdf file and uses @PdfToCsvProcessor.process to convert the pdf file to convert to csv
        and receives the data for database processing. Then it stores the data in database, and queries the db for
        request
        :param file_name:
        :param query_attribute:
        :param query_year:
        :return: response = {
                'company_name': 'dehaat',
                'file_id': 'xyz.csv' this file is stored at MEDIA_ROOT declared in settings.
            }
        """
        errors = []
        csv_file_path = path.join(BrowserProcessor.csvLocation,
                                  ''.join(random.choices(string.ascii_uppercase + string.digits, k=20) + ['.csv']))
        header_info, years, rows = \
            PdfToCsvProcessor.process(path.join(BrowserProcessor.pdfLocation, file_name), csv_file_path)
        response = dict()
        response['company_name'] = BrowserProcessor.get_company_name_from_header(header_info)
        dictionary = BrowserProcessor.convert_to_dictionary(rows, years)
        company, created = Company.objects.get_or_create(name=response['company_name'])
        for year, attributes in dictionary.items():
            for attribute, value in attributes.items():
                attribute_value, is_expense = value
                line_item, created = LineItem.objects.get_or_create(company_id=company,
                                                                    name=attribute, isExpense=is_expense)
                concrete_line_item, created = Finances. \
                    objects.get_or_create(year=year, line_item_id=line_item, amount=attribute_value)
        try:
            line_item = LineItem.objects.get(name=query_attribute, company_id=company)
            concrete_line_item = Finances.objects.get(year=query_year, line_item_id=line_item)
        except ObjectDoesNotExist as e:
            return None, e.args
        log.info("Company {0} has value {1} for the variable {2} in {3}",
                 company.name, concrete_line_item.amount, query_attribute, query_year)
        response['attribute'] = query_attribute
        response['year'] = query_year
        response['attribute_value'] = concrete_line_item.amount
        response['file_id'] = csv_file_path.split('/')[-1]
        return response, None

    @staticmethod
    def convert_to_dictionary(rows, years) -> dict:
        attribute_dict = {}
        start_dict = {}
        end_dict = {}
        for row in rows:
            if len(row[0]) is not 0:
                start_dict[row[0]] = row[1], True
                end_dict[row[0]] = row[2], True
            if len(row[3]) is not 0:
                end_dict[row[3]] = row[4], False
                end_dict[row[3]] = row[5], False
        attribute_dict[years[0]] = start_dict
        attribute_dict[years[1]] = end_dict
        return attribute_dict

    @staticmethod
    def get_company_name_from_header(header) -> string:
        """Returns company name
        This function assumes that first non empty line in the list of lines is company name
        """
        for line in header:
            if len(line.strip()) is not 0:
                return line.strip()
        raise Exception("Company name not found")

