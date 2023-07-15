from django.contrib import admin
from .models import Account, Transaction, ScheduledTransfer

# Make Account balance a read-only field
class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('balance',)

# Make Transaction amount a read-only field
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('amount',)

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(ScheduledTransfer)