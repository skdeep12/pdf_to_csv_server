import re
import pdftotext
import argparse
from os import path
from pathlib import Path
import os
import csv
import random
import string
import logging
import sys

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

PDF_FILE_LOCATION = Path('/tmp/dehaat')
CSV_FILE_LOCATION = Path('/tmp/dehaat')

year_regex = re.compile("\d\d\d\d")
two_decimal_regex = re.compile("\d+\.\d\d")
particulars_string = 'Particulars'
to_regex = re.compile("(To\s+[A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
by_regex = re.compile("(By\s+[A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
start_till_no_digit = re.compile("[^\d]*")
particulars_regex = re.compile("Particulars\s+\d\d\d\d\s+\d\d\d\d")
total_regex = re.compile("Total.*[^\d]")


def get_years_from_particular(page):
    particulars = particulars_regex.findall(page)
    y = []
    for token in particulars[0].split(" "):
        match = year_regex.search(token)
        if match is not None:
            y.append(token)
    y.sort()
    return y


def get_company_name_from_header(header) -> string:
    """Returns company name
    This function assumes that first non empty line in the list of lines is company name
    """
    for line in header:
        if len(line.strip()) is not 0:
            return line.strip()
    raise Exception("Company name not found")


def get_query_response(response, dictionary, attribute):
    if attribute in dictionary:
        response['attribute'] = attribute
        response['attribute_value'] = dictionary[attribute]


def process_row(row, start_year_dict, end_year_dict) -> list:
    left_row = []
    right_row = []
    left_line_item_without_prefix = ''
    right_line_item_without_prefix = ''
    numbers_in_row = two_decimal_regex.findall(row)
    if len(numbers_in_row) == 0:
        return []
    elif len(numbers_in_row) == 2:
        to_match = to_regex.findall(row)
        if len(to_match) == 0:
            by_match = by_regex.findall()
            right_row += by_match
            right_row += numbers_in_row
            right_line_item_without_prefix = by_match[0][3:].strip()
            start_year_dict[right_line_item_without_prefix] = numbers_in_row[0]
            end_year_dict[right_line_item_without_prefix] = numbers_in_row[1]
            left_row += ["", "", ""]
        else:
            left_line_item_without_prefix = to_match[0][3:].strip()
            start_year_dict[left_line_item_without_prefix] = numbers_in_row[0]
            end_year_dict[left_line_item_without_prefix] = numbers_in_row[1]
            left_row += to_match
            left_row += numbers_in_row
            right_row += ["", "", ""]
    else:
        to_match = to_regex.findall(row)
        if len(to_match) == 0:  # total row
            left_row.append(start_till_no_digit.search(row).group(0))
            right_row.append("Total Rs.")
        else:
            by_match = by_regex.findall(row)
            start_year_dict[to_match[0][3:].strip()] = numbers_in_row[0]
            end_year_dict[to_match[0][3:].strip()] = numbers_in_row[1]
            start_year_dict[by_match[0][3:].strip()] = numbers_in_row[2]
            end_year_dict[by_match[0][3:].strip()] = numbers_in_row[3]
            left_row += to_match
            right_row += by_match
        left_row += numbers_in_row[:2]
        right_row += numbers_in_row[2:]

    return left_row + right_row;


def convert_pdf_to_csv(file_name, query_attribute='', query_year=''):
    pdf_file_path = path.join(PDF_FILE_LOCATION, file_name)
    if path.isfile(pdf_file_path):
        csv_file_path = path.join(CSV_FILE_LOCATION,
                                  ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)))
        valid_query = False
        start_dict = {}
        end_dict = {}
        response = {}
        with open(pdf_file_path, "rb") as f, open(csv_file_path, "w") as csv_file:
            log.info("processing {0}".format(pdf_file_path))
            writer = csv.writer(csv_file)
            page1 = pdftotext.PDF(f)[0]
            rows = page1.split("\n")
            years = []
            i = 0
            for row in rows:
                i += 1
                if particulars_string in row:
                    years = get_years_from_particular(row)
                    break
            lines = rows[i:]
            header_info = rows[:i]
            response['year'] = years[0]
            writer.writerow([particulars_string, years[0], years[1]]*2)
            for line in lines:
                processed_row = process_row(line,start_dict,end_dict)
                if len(processed_row) > 0:
                    for i in range(len(processed_row)):  # remove all trailing and leading whitespace for each entry
                        processed_row[i] = processed_row[i].strip()
                    writer.writerow(processed_row)
        log.info("wrote the csv data to temp file {0} for pdf file {1}".format(csv_file_path, file_name))
        response['company_name'] = get_company_name_from_header(header_info)
        os.rename(csv_file_path, path.join(CSV_FILE_LOCATION,
                                           '_'.join([response['company_name'], years[1]])))
        for i in range(len(years)):
            if years[i] == query_year:
                if i == 0:
                    get_query_response(response,start_dict,query_attribute)
                else:
                    get_query_response(response,end_dict,query_attribute)
        log.info("query response is {0}".format(response))
        return response
    else:
        raise Exception("file does not exist" + file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arg parser')
    parser.add_argument('-f', type=str, help="path to pdf file")
    args = parser.parse_args()
    convert_pdf_to_csv(args.f,'Accounting Charges','2015')

# To regex: To
# By regex: By [A-Za-z" "\.\&\/]+\d+\.\d\d\s+\d+.\d\d
