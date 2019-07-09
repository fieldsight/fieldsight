# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0080_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='gsuit_sync',
            field=models.CharField(default='NA', max_length=2, choices=[('NA', 'Manual'), ('D', 'Daily'), ('W', 'Weekly'), ('F', 'Fortnightly'), ('M', 'Monthyl')]),
        ),
    ]
