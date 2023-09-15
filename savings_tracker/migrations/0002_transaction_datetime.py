# Generated by Django 4.2.2 on 2023-09-15 21:49

import datetime
from django.db import migrations, models


def copy_date_to_datetime(apps, schema_editor):
    Transaction = apps.get_model("savings_tracker", "Transaction")
    i=0
    for transaction in Transaction.objects.all():
        date = transaction.date
        transaction.datetime = datetime.datetime(date.year, date.month, date.day, 0, 0, i)
        i+=1
        transaction.save()

class Migration(migrations.Migration):

    dependencies = [
        ('savings_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2023, 1, 1, 0, 0, 0, 0)),
            preserve_default=False,
        ),
        migrations.RunPython(copy_date_to_datetime),
    ]