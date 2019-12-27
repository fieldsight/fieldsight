# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0105_auto_20191219_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='superorganization',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
