# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fsforms', '0080_auto_20190710_1524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editedsubmission',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
