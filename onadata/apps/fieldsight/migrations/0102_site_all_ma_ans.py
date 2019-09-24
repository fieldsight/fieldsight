# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0101_auto_20190822_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='all_ma_ans',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
