from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Company(models.Model):
    name = models.CharField('company_name', max_length=120, unique=True)

    def __str__(self):
        return self.name


class LineItem(models.Model):
    name = models.CharField('entry_name', max_length=120)
    isExpense = models.BooleanField('is_expense')
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Finances(models.Model):
    year = models.IntegerField('year')
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    amount = models.DecimalField('amount', decimal_places=2, max_digits=20)

    class Meta:
        unique_together = (('line_item_id', 'year'),)
