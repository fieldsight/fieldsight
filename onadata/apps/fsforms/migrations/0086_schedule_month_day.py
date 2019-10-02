# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0085_schedule_frequency'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='month_day',
            field=models.IntegerField(default=0),
        ),
    ]
