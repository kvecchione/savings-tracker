from django.http import HttpResponseRedirect
from django.shortcuts import render
import datetime
from savings_tracker.models import Account, Transaction, ScheduledTransfer
from savings_tracker.forms import TransferForm

def home(request):
    return render(request, "home.html", {'accounts': Account.objects.all()})

def scheduled(request):
    return render(request, "scheduled.html", {'transfer_list': ScheduledTransfer.objects.all()})

def transactions(request, account_name):
    if account_name == 'all':
        title = "All transactions"
        transaction_list = Transaction.objects.all().order_by("date")[:20]
        show_account = True
    else:
        title = f"Transactions for {account_name.title()}"
        transaction_list = Transaction.objects.filter(account__name=account_name).order_by("date")[:20]
        show_account = False

    return render(request, "transactions.html", {'transactions': transaction_list, 'show_account': show_account, 'title': title})

def transfer(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            t = Transaction()
            a = Account.objects.get(name=form.cleaned_data['account'])
            t.account = a
            if form.cleaned_data['type'] == 'withdrawal':
                t.amount = -form.cleaned_data['amount']
                a.balance -= form.cleaned_data['amount']
            elif form.cleaned_data['type'] == 'deposit':
                t.amount = form.cleaned_data['amount']
                a.balance += form.cleaned_data['amount']
            t.date = datetime.datetime.now()
            t.description = form.cleaned_data['description']
            t.save()
            a.save()

            return HttpResponseRedirect('/')
    else:
        form = TransferForm()
    return render(request, "transfer.html", {'form': form})