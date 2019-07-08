# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0076_syncschedule_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='syncschedule',
            name='day',
        ),
        migrations.AddField(
            model_name='syncschedule',
            name='date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='syncschedule',
            name='end_of_month',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='syncschedule',
            name='schedule',
            field=models.CharField(default='M', max_length=2, choices=[('NA', 'Manual'), ('D', 'Daily'), ('W', 'Weekly'), ('F', 'Fortnightly'), ('M', 'Monthly')]),
        ),
    ]
