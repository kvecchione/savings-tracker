from django import forms
from savings_tracker.models import Account
from djmoney.models.fields import MoneyField

TYPES = [('withdrawal','withdrawal'), ('deposit','deposit')]
ACCOUNTS = [(a.name, a.name) for a in Account.objects.all()]

class TransferForm(forms.Form):
    account = forms.ChoiceField(label='Account', choices=ACCOUNTS)
    type = forms.ChoiceField(widget=forms.RadioSelect(), choices=TYPES)
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    description = forms.CharField(max_length=100)
