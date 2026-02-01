from django import forms
from savings_tracker.models import Account
from djmoney.models.fields import MoneyField

TYPES = [('withdrawal','withdrawal'), ('deposit','deposit')]

class TransactionForm(forms.Form):
    account = forms.ChoiceField(label='Account', choices=[])
    type = forms.ChoiceField(widget=forms.RadioSelect(), initial=TYPES[0], choices=TYPES)
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    description = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(a.name, f"{a.name} - Balance: {a.balance}") for a in Account.objects.all()]
        self.fields['account'].choices = choices

class EditTransactionForm(forms.Form):
    amount = forms.DecimalField(max_digits=8, decimal_places=2)
    description = forms.CharField(max_length=100)
