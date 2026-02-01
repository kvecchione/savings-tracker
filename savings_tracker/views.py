from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    account_id = transaction.account.id
    old_account = transaction.account
    
    if request.method == 'POST':
        form = EditTransactionForm(request.POST)
        if form.is_valid():
            # Store old values
            old_amount = transaction.amount
            
            # Reverse the old transaction from the account balance
            transaction.account.balance -= old_amount
            transaction.account.save()
            
            # Update transaction fields (keeping same account and type)
            # Determine if original was deposit or withdrawal
            is_deposit = old_amount >= 0
            
            if is_deposit:
                new_amount = form.cleaned_data['amount']
            else:
                new_amount = -form.cleaned_data['amount']
            
            transaction.amount = new_amount
            transaction.description = form.cleaned_data['description']
            
            # Apply the new transaction to the account balance
            transaction.account.balance += new_amount
            transaction.account.save()
            
            # Update post_balance for this transaction
            transaction.post_balance = transaction.account.balance
            transaction.save()
            
            # Recalculate post_balance for all transactions in the account
            recalculate_post_balances(transaction.account)
            
            return HttpResponseRedirect(f'/account/{account_id}/')
    else:
        # Pre-populate form with existing data
        initial_data = {
            'amount': abs(transaction.amount),
            'description': transaction.description
        }
        form = EditTransactionForm(initial=initial_data)
    
    return render(request, "edit_transaction.html", {
        'form': form, 
        'transaction': transaction,
        'transaction_type': 'Deposit' if transaction.amount >= 0 else 'Withdrawal'
    })

def recalculate_post_balances(account):
    """Recalculate post_balance for all transactions in an account"""
    transactions = Transaction.objects.filter(account=account).order_by('datetime')
    running_balance = 0
    
    for trans in transactions:
        running_balance += trans.amount
        trans.post_balance = running_balance
        trans.save()
    
    # Update account balance to match
    account.balance = running_balance
    account.save()

def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    account_id = transaction.account.id
    account = transaction.account
    
    if request.method == 'POST':
        transaction.delete()
        # Recalculate all post_balances after deletion
        recalculate_post_balances(account)
        
        return HttpResponseRedirect(f'/account/{account_id}/')
    
    return render(request, "account.html", {'transaction': transaction, 'confirm_delete': True})