from django.test import TestCase

# Create your tests here.


class ConversionTest(TestCase):

    def setUp(self) -> None:
        pdfLocation = '../../script/BalSheet.pdf'
