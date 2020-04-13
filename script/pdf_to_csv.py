import re
import pdftotext
import argparse
from os import path
import csv


year_regex = re.compile("\d\d\d\d")
two_decimal_regex = re.compile("\d+\.\d\d")
particulars_string = 'Particulars'
to_regex = re.compile("(To [A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
by_regex = re.compile("(By [A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
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
    return y


def process_row(row):
    left_row = []
    right_row = []
    numbers_in_row = two_decimal_regex.findall(row)
    if len(numbers_in_row) == 0:
        return []
    elif len(numbers_in_row) == 2:
        to_match = to_regex.findall(row)
        if len(to_match) == 0:
            by_match = by_regex.findall()
            right_row.append(by_match)
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
            left_row += to_match
            right_row += by_regex.findall(row)
        left_row += numbers_in_row[:2]
        right_row += numbers_in_row[2:]

    return left_row + right_row;


def convert_pdf_to_csv(file_path):
    if path.isfile(file_path):
        with open(args.f, "rb") as f, open("BalSheet.csv", "w") as csv_file:
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
            writer.writerow([particulars_string, years[0],years[1]]*2)
            for line in lines:
                processed_row = process_row(line)
                if len(processed_row) > 0:
                    for i in range(len(processed_row)):
                        processed_row[i] = processed_row[i].strip()
                    print(processed_row)
                    writer.writerow(processed_row)
    else:
        print("file does not exist")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='arg parser')
    parser.add_argument('-f', type=str, help="path to pdf file")
    args = parser.parse_args()
    convert_pdf_to_csv(args.f)

# To regex: To
# By regex: By [A-Za-z" "\.\&\/]+\d+\.\d\d\s+\d+.\d\d
