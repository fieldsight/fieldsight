# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0093_auto_20200107_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationformlibrary',
            name='date_range_end',
            field=models.DateField(default=datetime.date.today, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organizationformlibrary',
            name='date_range_start',
            field=models.DateField(default=datetime.date.today, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organizationformlibrary',
            name='frequency',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organizationformlibrary',
            name='month_day',
            field=models.IntegerField(default=0, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organizationformlibrary',
            name='schedule_level_id',
            field=models.IntegerField(default=0, null=True, blank=True, choices=[(0, 'Daily'), (1, 'Weekly'), (2, 'Monthly')]),
        ),
    ]
