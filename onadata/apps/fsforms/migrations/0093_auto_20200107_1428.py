# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0092_organizationformlibrary'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationformlibrary',
            name='date_range_end',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='date_range_start',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='default_submission_status',
            field=models.IntegerField(default=0, choices=[(0, 'Pending'), (1, 'Rejected'), (2, 'Flagged'), (3, 'Approved')]),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='form_type',
            field=models.IntegerField(default=0, choices=[(0, 'General'), (1, 'Scheduled')]),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='frequency',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='month_day',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='schedule_level_id',
            field=models.IntegerField(default=0, choices=[(0, 'Daily'), (1, 'Weekly'), (2, 'Monthly')]),
        ),
        migrations.AddField(
            model_name='organizationformlibrary',
            name='selected_days',
            field=models.ManyToManyField(related_name='library_forms', to='fsforms.Days', blank=True),
        ),
    ]
