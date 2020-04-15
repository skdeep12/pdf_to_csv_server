from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

