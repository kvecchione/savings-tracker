from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from savings_tracker.models import Account, Transaction, ScheduledTransfer
from savings_tracker.forms import TransferForm

def home(request):
    return render(request, "home.html", {'accounts': Account.objects.all()})

def scheduled(request):
    return render(request, "scheduled.html", {'transfer_list': ScheduledTransfer.objects.all()})

def account(request, account_id):
    account = Account.objects.get(id=account_id)
    title = f"{account.name.title()}"
    transaction_list = Transaction.objects.filter(account__id=account_id).order_by("date")[:10]

    return render(request, "account.html", {'transactions': transaction_list, 'account': account})

def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            t = Transaction()
            t.account = Account.objects.get(name=form.cleaned_data['account'])
            if form.cleaned_data['type'] == 'withdrawal':
                t.amount = -form.cleaned_data['amount']
            elif form.cleaned_data['type'] == 'deposit':
                t.amount = form.cleaned_data['amount']
            t.date = datetime.datetime.now()
            t.description = form.cleaned_data['description']
            t.save()

            return HttpResponseRedirect('/')
    else:
        form = TransferForm()
    return render(request, "transfer.html", {'form': form})