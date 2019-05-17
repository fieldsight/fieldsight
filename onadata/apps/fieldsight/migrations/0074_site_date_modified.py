# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fieldsight', '0073_auto_20190425_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='site',
            name='date_modified',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 29, 9, 55, 5, 603600, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
