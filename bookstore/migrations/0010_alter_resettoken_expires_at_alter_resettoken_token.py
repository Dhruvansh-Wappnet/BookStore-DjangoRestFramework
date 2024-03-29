# Generated by Django 5.0.2 on 2024-02-21 05:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0009_alter_resettoken_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resettoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 22, 5, 12, 9, 786223, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resettoken',
            name='token',
            field=models.CharField(default='', editable=False, max_length=6, unique=True),
        ),
    ]
