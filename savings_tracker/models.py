from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
import datetime

class Account(models.Model):
    name = models.CharField(max_length=64)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    description = models.CharField(max_length=64)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    datetime = models.DateTimeField()
    post_balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    def __str__(self):
        return self.description
    
class ScheduledTransfer(models.Model):
    description = models.CharField(max_length=64)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=50, decimal_places=2)
    day_of_month = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(28)])

    def __str__(self):
        return self.description