# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0075_syncschedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='syncschedule',
            name='day',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
