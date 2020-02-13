# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0002_auto_20191217_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportsettings',
            name='filter',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
