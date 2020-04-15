from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Company(models.Model):
    name = models.CharField('company_name', max_length=120)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name


class LineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField('entry_name', max_length=120)
    isExpense = models.BooleanField('is_expense')

    def __str__(self):
        return self.name


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


class Finances(models.Model):
    id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField('year',validators=[MinValueValidator(1960),max_value_current_year])
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    amount = models.DecimalField('amount', decimal_places=2, max_digits=20)

