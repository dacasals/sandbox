# Generated by Django 5.0.4 on 2024-05-01 04:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20221205_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, db_default=datetime.datetime(2024, 5, 1, 4, 22, 45, 673477, tzinfo=datetime.timezone.utc)),
        ),
    ]
