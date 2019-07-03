# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0086_siteprogresshistory_setting'),
    ]

    operations = [
        migrations.AddField(
            model_name='progresssettings',
            name='date',
            field=models.DateTimeField(auto_now=True),
            preserve_default=False,
        ),
    ]
