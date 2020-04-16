from django.db import models


class Company(models.Model):
    name = models.CharField('company_name', max_length=120, unique=True)
    id = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.name


class LineItem(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField('entry_name', max_length=120)
    isExpense = models.BooleanField('is_expense')

    def __str__(self):
        return self.name


class Finances(models.Model):
    id = models.IntegerField(primary_key=True)
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    year = models.IntegerField('year')
    line_item_id = models.ForeignKey(LineItem, on_delete=models.CASCADE)
    amount = models.DecimalField('amount', decimal_places=2, max_digits=20)

