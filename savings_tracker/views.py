from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
import datetime
from savings_tracker.models import Account, Transaction, ScheduledTransfer
from savings_tracker.forms import TransactionForm, EditTransactionForm

def home(request):
    total_balance = sum([account.balance for account in Account.objects.all()])
    return render(request, "home.html", {'accounts': Account.objects.all(), 'total_balance': total_balance})

def scheduled(request):
    return render(request, "scheduled.html", {'transfer_list': ScheduledTransfer.objects.all()})

def account(request, account_id):
    account = Account.objects.get(id=account_id)
    title = f"{account.name.title()}"
    transaction_list = Transaction.objects.filter(account__id=account_id).order_by("-datetime")

    return render(request, "account.html", {'transactions': transaction_list, 'account': account})

def transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            t = Transaction()
            t.account = Account.objects.get(name=form.cleaned_data['account'])
            if form.cleaned_data['type'] == 'withdrawal':
                t.amount = -form.cleaned_data['amount']
            elif form.cleaned_data['type'] == 'deposit':
                t.amount = form.cleaned_data['amount']
            t.datetime = datetime.datetime.now()
            t.description = form.cleaned_data['description']
            t.save()

            return HttpResponseRedirect('/')
    else:
        form = TransactionForm()
    return render(request, "transaction.html", {'form': form})


def recompute_post_balances(account):
    transactions = Transaction.objects.filter(account=account).order_by('datetime')
    running = 0
    for t in transactions:
        running += t.amount
        t.post_balance = running
        t.save()
    account.balance = running
    account.save()


def edit_transaction(request, pk):
    t = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = EditTransactionForm(request.POST, instance=t)
        if form.is_valid():
            form.save()
            recompute_post_balances(t.account)
            return redirect('account', account_id=t.account.id)
    else:
        form = EditTransactionForm(instance=t)
    return render(request, "transaction.html", {'form': form, 'edit': True, 'transaction': t})


def delete_transaction(request, pk):
    t = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        account = t.account
        t.delete()
        recompute_post_balances(account)
        return redirect('account', account_id=account.id)
    return render(request, "confirm_delete.html", {'object': t})