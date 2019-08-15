# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0081_auto_20190710_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='stage',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
