import datetime
from django_cron import CronJobBase, Schedule
from savings_tracker.models import ScheduledTransfer, Transaction

class RunScheduledTransfers(CronJobBase):
    RUN_EVERY_MINS = 1440

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'run_scheduled_transfers'

    def do(self):
        output = ""
        transfers = False
        for scheduled_transfer in ScheduledTransfer.objects.all():
            if datetime.datetime.now().day == scheduled_transfer.day_of_month:
                account = scheduled_transfer.account
                transaction = Transaction()
                transaction.account = account
                transaction.amount = scheduled_transfer.amount
                transaction.date = datetime.datetime.now()
                transaction.description = scheduled_transfer.description
                transaction.save()
                output += f"Transferred {scheduled_transfer.amount} to {scheduled_transfer.account}\n"
                transfers = True
        if not transfers:
            output += f"No transfers scheduled for this time period\n"
        return output
