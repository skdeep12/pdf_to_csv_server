import re

year_regex = re.compile("\d\d\d\d")
two_decimal_regex = re.compile("\d+\.\d\d")
particulars_string = 'Particulars'
to_regex = re.compile("(To\s+[A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
by_regex = re.compile("(By\s+[A-Za-z\" \"\.\&\/]+)\d+\.\d\d\s+\d+.\d\d")
start_till_no_digit = re.compile("[^\d]*")
particulars_regex = re.compile("Particulars\s+\d\d\d\d\s+\d\d\d\d")
total_regex = re.compile("Total.*[^\d]")