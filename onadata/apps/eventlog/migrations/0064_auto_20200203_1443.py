# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventlog', '0063_auto_20200203_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldsightlog',
            name='event_url',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='fieldsightlog',
            name='extra_message',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='fieldsightlog',
            name='extra_obj_url',
            field=models.TextField(blank=True),
        ),
    ]
