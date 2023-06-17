from django import forms
from savings_tracker.models import Account
from djmoney.models.fields import MoneyField

TYPES = [('withdrawal','withdrawal'), ('deposit','deposit')]

class TransferForm(forms.Form):
    account = forms.ChoiceField(label='Account', choices=[(a.name, f"{a.name} - Balance: {a.balance}") for a in Account.objects.all()])
    type = forms.ChoiceField(widget=forms.RadioSelect(), initial=TYPES[0], choices=TYPES)
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    description = forms.CharField(max_length=100)
