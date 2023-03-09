from django.contrib import admin

from .models import Account, Transaction, ScheduledTransfer

admin.site.register(Account)
admin.site.register(Transaction)
admin.site.register(ScheduledTransfer)