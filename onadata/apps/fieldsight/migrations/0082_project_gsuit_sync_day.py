# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0081_project_gsuit_sync'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='gsuit_sync_day',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
