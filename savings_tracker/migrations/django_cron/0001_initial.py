# Generated by Django 4.1.7 on 2023-03-09 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CronJobLock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("job_name", models.CharField(max_length=200, unique=True)),
                ("locked", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="CronJobLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(db_index=True, max_length=64)),
                ("start_time", models.DateTimeField(db_index=True)),
                ("end_time", models.DateTimeField(db_index=True)),
                ("is_success", models.BooleanField(default=False)),
                ("message", models.TextField(blank=True, default="")),
                (
                    "ran_at_time",
                    models.TimeField(
                        blank=True, db_index=True, editable=False, null=True
                    ),
                ),
            ],
            options={
                "index_together": {
                    ("code", "start_time", "ran_at_time"),
                    ("code", "start_time"),
                    ("code", "is_success", "ran_at_time"),
                },
            },
        ),
    ]