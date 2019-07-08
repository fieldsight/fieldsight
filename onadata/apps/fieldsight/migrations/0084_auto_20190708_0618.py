# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0083_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='gsuit_sync_day',
        ),
        migrations.AddField(
            model_name='project',
            name='gsuit_sync_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='gsuit_sync_end_of_month',
            field=models.BooleanField(default=False),
        ),
    ]
