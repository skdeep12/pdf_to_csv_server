import unittest
import re


class RegExTest(unittest.TestCase):
    s = " 2012.00 2013.00"
    to_regex = re.compile("To [A-Za-z\" \"\.\&\/]+\d+\.\d\d\s+\d+.\d\d")

    def test(self):
        print(self.to_regex.search(self.s))


if __name__ == '__main__':
    unittest.main()
