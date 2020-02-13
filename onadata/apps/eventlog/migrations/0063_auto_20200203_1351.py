# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0062_auto_20191223_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldsightlog',
            name='extra_message',
            field=models.TextField(max_length=1023, null=True, blank=True),
        ),
    ]
