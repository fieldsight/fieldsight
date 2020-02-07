# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0100_auto_20200130_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsyncsettings',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
