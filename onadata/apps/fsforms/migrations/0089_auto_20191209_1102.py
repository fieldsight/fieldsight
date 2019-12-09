# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0088_auto_20191209_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsyncsettings',
            name='day',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='reportsyncsettings',
            name='schedule_type',
            field=models.CharField(default=0, max_length=50, choices=[(0, 'Manual'), (1, 'Daily'), (2, 'Weekly'), (3, 'Monthly')]),
        ),
    ]
