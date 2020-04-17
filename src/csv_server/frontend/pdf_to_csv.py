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
                'attribute': is query attribute queried by user
                'year': is the year user has asked in the query
                'attribute_value': is value returned by db query for 'attribute' and 'year' combination
            }
        """
        errors = []
        csv_file_path = path.join(BrowserProcessor.csvLocation,
                                  ''.join(random.choices(string.ascii_uppercase + string.digits, k=20) + ['.csv']))
        header_info, years, rows = \
            PdfToCsvProcessor.process(path.join(BrowserProcessor.pdfLocation, file_name), csv_file_path)
        response = dict()
        company_name = BrowserProcessor.get_company_name_from_header(header_info)
        response['file_id'] = csv_file_path.split('/')[-1]
        dictionary = BrowserProcessor.convert_to_dictionary(rows, years)
        company, created = Company.objects.get_or_create(name=company_name)
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
            return response, e.args
        log.info("Company {0} has value {1} for the variable {2} in {3}"
                 .format(company.name, concrete_line_item.amount, query_attribute, query_year))
        response['attribute'] = query_attribute
        response['year'] = query_year
        response['attribute_value'] = concrete_line_item.amount
        return response, None

    @staticmethod
    def convert_to_dictionary(rows, years) -> dict:
        """

        :param rows: are processed rows and each row is of the form
                                [line_item, amount, amount, line_item, amount, amount]
        :param years: [start_year, end_year]
        :return: a dictionary of the format dict = {
            'start_year': { 'line_item': amount
                            .
                            .
                            .
                        },
            'end_year': {'line_item': amount
                            .
                            .
                            .
                        }
        }
        """
        attribute_dict = {}
        start_dict = {}
        end_dict = {}
        for row in rows:
            if len(row[0]) is not 0:
                line_item_without_prefix = row[0][3:]  # stripping 'To ' from start of the string
                start_dict[line_item_without_prefix] = row[1], True
                end_dict[line_item_without_prefix] = row[2], True
            if len(row[3]) is not 0:
                line_item_without_prefix = row[3][3:]  # stripping 'By ' from start of the string
                end_dict[line_item_without_prefix] = row[4], False
                end_dict[line_item_without_prefix] = row[5], False
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

