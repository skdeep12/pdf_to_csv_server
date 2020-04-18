import re
import pdftotext
import argparse
from os import path
import csv
import logging
import sys

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

year_regex = re.compile("\d\d\d\d")
two_decimal_regex = re.compile("\d+\.\d\d")
particulars_string = 'Particulars'
to_regex = re.compile("(To\s+[A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
by_regex = re.compile("(By\s+[A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
start_till_no_digit = re.compile("[^\d]*")
particulars_regex = re.compile("Particulars\s+\d\d\d\d\s+\d\d\d\d")
total_regex = re.compile("Total.*[^\d]")


class PdfToCsvProcessor:
    @staticmethod
    def process(file_name, csv_file_path="BalSheet.csv"):
        if path.isfile(file_name):
            with open(file_name, "rb") as f:
                log.info("processing {0}".format(file_name))
                page1 = pdftotext.PDF(f)[0]
                rows = page1.split("\n")
                years, header_info, processed_rows = PdfToCsvProcessor.process_line_items_for_balance_sheet(rows,True)
        else:
            raise Exception("file does not exist" + file_name)
        with open(csv_file_path, "w+") as csv_file:
            writer = csv.writer(csv_file)
            for row in processed_rows:
                print(row)
                writer.writerow(row)
            log.info("wrote the csv data to file {0} for pdf file {1}".format(csv_file_path, file_name))
        return header_info, years, processed_rows

    @staticmethod
    def process_line_items_for_balance_sheet(rows, header_page):
        years = []
        header_info = []
        processed_rows = []
        i = 0
        for row in rows:
            i += 1
            if particulars_string in row:
                years = PdfToCsvProcessor.get_years_from_particular(row)
                break
        if header_page and i == len(rows):
            raise Exception("Particulars row not found, can not continue with parsing")
        elif header_page:
            header_info = rows[:i]
        lines = rows[i:]
        if header_page:
            processed_rows.append([particulars_string, years[0], years[1]] * 2)
        for line in lines:
            processed_row = PdfToCsvProcessor.process_row(line)
            #print(processed_row)
            if len(processed_row) > 0:
                for i in range(len(processed_row)):  # remove all trailing and leading whitespace for each entry
                    processed_row[i] = processed_row[i].strip()
                processed_rows.append(processed_row)
        return years, header_info, processed_rows

    @staticmethod
    def get_years_from_particular(row):
        particulars = particulars_regex.findall(row)
        y = []
        for token in particulars[0].split(" "):
            match = year_regex.search(token)
            if match is not None:
                y.append(token)
        y.sort()
        return y

    @staticmethod
    def process_row(row) -> list:
        left_row = []
        right_row = []
        numbers_in_row = two_decimal_regex.findall(row)
        if len(numbers_in_row) == 0:
            return []
        elif len(numbers_in_row) == 2:
            to_match = to_regex.findall(row)
            if len(to_match) == 0:
                by_match = by_regex.findall()
                right_row += by_match
                right_row += numbers_in_row
                left_row += ["", "", ""]
            else:
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
                left_row += to_match
                right_row += by_match
            left_row += numbers_in_row[:2]
            right_row += numbers_in_row[2:]

        return left_row + right_row;


class CommandLineProcessor:
    @staticmethod
    def process(filename):
        PdfToCsvProcessor.process(filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='script to parse pdf file, produces csv in current directory')
    parser.add_argument('-f', type=str, help="path to pdf file",required=True)
    args = parser.parse_args()
    CommandLineProcessor.process(args.f)


