# code
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from savings_tracker.models import Transaction
 
@receiver(post_save, sender=Transaction) 
def create_transaction(sender, instance, created, **kwargs):
    if created:
        print('Adjusting account balance with new transaction')
        instance.account.balance += instance.amount
        instance.account.save()
        instance.post_balance = instance.account.balance
        instance.save()
  
@receiver(post_delete, sender=Transaction) 
def delete_transaction(sender, instance, **kwargs):
    print('Adjusting account balance with deleted transaction')
    instance.account.balance -= instance.amount
    instance.account.save()
