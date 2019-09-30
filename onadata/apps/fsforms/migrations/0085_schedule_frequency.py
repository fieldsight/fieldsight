# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0084_stage_regions'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='frequency',
            field=models.IntegerField(default=0),
        ),
    ]
