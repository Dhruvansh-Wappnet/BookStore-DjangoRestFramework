# Generated by Django 5.0.2 on 2024-02-20 13:19

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_otp_resettoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='resettoken',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 2, 21, 13, 19, 14, 568236, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resettoken',
            name='token',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=40, unique=True),
        ),
    ]
