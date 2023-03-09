from savings_tracker.models import Account, ScheduledTransfer, Transaction
import datetime

Transaction.objects.all().delete()
ScheduledTransfer.objects.all().delete()
Account.objects.all().delete()

accounts = [
    {
        'name': 'Amy',
        'balance': 0,
        'transfers': {
            'amount': 250.00,
            'day_of_month': 15,
        },
        'transactions': [{
            'description': 'Initial amount',
            'amount': 1337.00,
        }]
    },
    {
        'name': 'Bob',
        'balance': 0,
        'transfers': {
            'amount': 250.00,
            'day_of_month': 15,
        },
        'transactions': [{
            'description': 'Initial amount',
            'amount': 1234.00,
        }]
    },
    {
        'name': 'Calvin',
        'balance': 0,
        'transactions': [{
            'description': 'Initial amount',
            'amount': 250.00,
        }]
    }
]

for account in accounts:
    try:
        a = Account.objects.get(name=account['name'])
    except:
        a = Account()
        a.balance = account['balance']
        a.name = account['name']
        a.save()

    transactions = account.get('transactions', [])
    for transaction in transactions:
        t = Transaction()
        t.date = datetime.datetime.now()
        t.account = a
        t.amount = transaction['amount']
        t.description = transaction['description']
        t.save()

    transfer = account.get('transfers')
    if not transfer:
        continue
    description = account['name'] + ' Monthly Transfer'
    try:
        t = ScheduledTransfer.objects.get(description=description)
    except:
        t = ScheduledTransfer()
        t.description = description
        t.amount = transfer['amount']
        t.day_of_month = transfer['day_of_month']
        t.account = a
        t.save()
